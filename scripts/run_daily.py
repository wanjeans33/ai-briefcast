#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Briefcast — 每日全流程编排（固定下来的 workflow）

一条命令跑完：抓取/解析 → pi agent + DeepSeek 改写 → 豆包 TTS 合成音频。
设计为可被定时任务（Windows 计划任务 / cron）每天自动调用。

阶段：
  1. fetch  抓取两个来源「今天」最新一期的详情子页面并解析（Python）
  2. write   保存原始素材 samples/source-<日期>.md
  3. rewrite 用 pi（https://pi.dev）+ DeepSeek 把素材改写成简洁版 / 完整版播报稿
  4. tts     用 scripts/doubao_tts_ws.py 把每份稿子合成 MP3 到 audio_output/

凭据（仓库根 .env，见 .env.example）：
  DEEPSEEK_API_KEY                          # pi 的 deepseek provider
  VOLC_APP_ID / VOLC_API_KEY / VOLC_SPEAKER # 豆包 TTS

用法：
  python scripts/run_daily.py                 # 跑完整流程（默认 pi + 豆包）
  python scripts/run_daily.py --dry-run       # 只打印计划，不调用 pi/TTS
  python scripts/run_daily.py --llm api        # 改用 OpenAI 兼容直连（DeepSeek）
  python scripts/run_daily.py --tts none       # 只生成文稿，不合成音频
  python scripts/run_daily.py --modes concise  # 只做简洁版
"""
from __future__ import annotations

import argparse
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_broadcast as gb  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
DOUBAO = REPO_ROOT / "scripts" / "doubao_tts_ws.py"
QWEN = REPO_ROOT / "scripts" / "qwen_tts" / "broadcast_tts.py"
QWEN_REF = REPO_ROOT / "scripts" / "qwen_tts" / "my_voice3.wav"


def load_dotenv(repo_root: Path) -> None:
    env = repo_root / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class Logger:
    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = open(path, "a", encoding="utf-8")

    def __call__(self, msg: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{stamp}] {msg}"
        print(line, flush=True)
        self.fh.write(line + "\n")
        self.fh.flush()

    def close(self) -> None:
        self.fh.close()


def strip_header(md: str) -> str:
    """去掉 wrap_header 生成的元信息，返回可朗读的正文。"""
    marker = "\n---\n\n"
    return md.split(marker, 1)[1].strip() if marker in md else md.strip()


def run_tts(text: str, out_path: Path, log: Logger, speaker: str | None = None) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    if speaker:
        env["VOLC_SPEAKER"] = speaker  # 用所选音色覆盖 doubao 脚本读取的 speaker
    proc = subprocess.run(
        [sys.executable, str(DOUBAO), text, str(out_path)],
        cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8", env=env,
    )
    tail = (proc.stdout or "").strip().splitlines()[-1:] or [""]
    if proc.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
        log(f"[tts ] 合成成功 → {out_path}（{out_path.stat().st_size} bytes）")
        return True
    log(f"[tts ] 合成失败：{tail[0]} | stderr: {(proc.stderr or '')[-300:]}")
    return False


def run_qwen(md_path: Path, out_path: Path, suffix: str, log: Logger) -> bool:
    """用 qwen_tts/broadcast_tts.py（本地 GPU，克隆音色 my_voice3）合成。"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sys.executable, str(QWEN), str(md_path), suffix or "-myvoice"],
        cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8",
    )
    if proc.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0:
        log(f"[tts ] qwen 合成成功 → {out_path}（{out_path.stat().st_size} bytes）")
        return True
    log(f"[tts ] qwen 合成失败：stderr: {(proc.stderr or '')[-300:]}")
    return False


def _audio_seconds(path: Path) -> float:
    import av
    a = av.open(str(path))
    d = a.duration / 1e6
    a.close()
    return d


def concat_audio(seg_paths: list[Path], out_path: Path) -> None:
    """用 ffmpeg 把多段 mp3 顺序拼成一个 mp3（重编码，兼容不同参数）。"""
    import make_xhs_video_html as xhs
    cmd = [xhs.FFMPEG, "-y"]
    for p in seg_paths:
        cmd += ["-i", str(p)]
    n = len(seg_paths)
    filt = "".join(f"[{i}:a]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]"
    cmd += ["-filter_complex", filt, "-map", "[a]",
            "-c:a", "libmp3lame", "-b:a", "128k", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg concat 失败:\n" + r.stderr[-800:])


def synth_segmented(segments: list[str], out_mp3: Path, log: Logger,
                    speaker: str | None) -> list[float] | None:
    """逐段豆包合成 → 测每段真实时长 → 拼成整段 mp3。返回每段时长列表。

    用于精确卡点：卡片切换正好落在每段旁白结束处。失败返回 None（调用方回退）。
    """
    seg_dir = out_mp3.parent / "segs"
    seg_dir.mkdir(parents=True, exist_ok=True)
    import time
    seg_paths, durs = [], []
    for i, seg in enumerate(segments):
        sp = seg_dir / f"{out_mp3.stem}-seg{i:02d}.mp3"
        ok = False
        for attempt in range(3):  # 豆包偶发 NO AUDIO / 限流，自动重试
            if run_tts(seg, sp, log, speaker=speaker):
                ok = True
                break
            log(f"[tts ] 第 {i+1}/{len(segments)} 段失败，重试 {attempt+1}/3…")
            time.sleep(3 + 3 * attempt)
        if not ok:
            log(f"[tts ] 第 {i+1}/{len(segments)} 段三次仍失败，放弃卡点路径。")
            return None
        seg_paths.append(sp)
        durs.append(_audio_seconds(sp))
    try:
        concat_audio(seg_paths, out_mp3)
    except Exception as e:  # noqa: BLE001
        log(f"[tts ] 分段拼接失败：{str(e)[:200]}")
        return None
    log(f"[tts ] 分段合成 {len(segments)} 段 → {out_mp3}"
        f"（总长 {sum(durs):.1f}s）")
    return durs


def main() -> int:
    ap = argparse.ArgumentParser(description="AI Briefcast 每日全流程编排")
    ap.add_argument("--date", help="指定日期 YYYY-MM-DD（默认取各站最新一期）")
    ap.add_argument("--modes", default="concise,full", help="逗号分隔：concise,full")
    ap.add_argument("--llm", choices=["pi", "api"], default="pi",
                    help="改写后端：pi（pi agent + DeepSeek，默认）或 api（OpenAI 兼容直连）")
    ap.add_argument("--tts", choices=["doubao", "qwen", "none"], default="doubao",
                    help="TTS 后端：doubao（默认，网络）/ qwen（本地 GPU 克隆音色）/ none")
    ap.add_argument("--doubao-speaker",
                    help="豆包音色 ID；缺省优先用 VOLC_SPEAKER2（你的克隆音色），再回退 VOLC_SPEAKER")
    ap.add_argument("--audio-suffix", default="",
                    help="音频文件名后缀，如 -myvoice（便于和其他音色对比，不覆盖）")
    ap.add_argument("--tts-only", action="store_true",
                    help="跳过改写，直接对已存在的 broadcast-<日期>-<mode>.md 重新合成音频")
    ap.add_argument("--video", action="store_true",
                    help="基于 concise 音频额外生成一支小红书竖屏视频（需 playwright + ffmpeg）")
    ap.add_argument("--intro", default=None,
                    help="片头视频路径；缺省自动探测 片头/小猫片头_1x1_4s.mp4（视频默认带片头）")
    ap.add_argument("--no-intro", action="store_true", help="不加片头")
    ap.add_argument("--outdir", default="samples", help="文稿输出目录")
    ap.add_argument("--audio-dir", default="audio_output", help="音频输出目录")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划，不调用 pi/TTS")
    args = ap.parse_args()

    load_dotenv(REPO_ROOT)

    # api 后端：若只配了 DEEPSEEK_API_KEY，自动补上 OpenAI 兼容直连参数
    if args.llm == "api" and os.getenv("DEEPSEEK_API_KEY"):
        os.environ.setdefault("LLM_BASE_URL", "https://api.deepseek.com")
        os.environ.setdefault("LLM_MODEL", "deepseek-chat")
        os.environ.setdefault("LLM_API_KEY", os.environ["DEEPSEEK_API_KEY"])

    # 音色：优先命令行，其次 VOLC_SPEAKER2（你的克隆音色），最后回退 VOLC_SPEAKER
    speaker = args.doubao_speaker or os.getenv("VOLC_SPEAKER2") or os.getenv("VOLC_SPEAKER")

    modes = [m.strip() for m in args.modes.split(",") if m.strip() in ("concise", "full")]
    outdir = REPO_ROOT / args.outdir
    audio_dir = REPO_ROOT / args.audio_dir

    # ---- 1) 抓取 + 解析 -----------------------------------------------------
    digest_url = gb.latest_article_url(gb.DIGEST_HOME, "digest", args.date)
    brief_url = gb.latest_article_url(gb.BRIEF_HOME, "daily", args.date)
    digest = gb.parse_digest(digest_url)
    brief = gb.parse_brief(brief_url)
    date = digest.date if digest.date != "unknown" else brief.date
    source_text = gb.build_source_text(digest, brief)

    log = Logger(REPO_ROOT / "logs" / f"run-{date}.log")
    log(f"==== AI Briefcast 每日流程 · {date} | llm={args.llm} tts={args.tts}"
        f"{' tts-only' if args.tts_only else ''}"
        f"{' (dry-run)' if args.dry_run else ''} ====")
    log(f"[fetch] digest: {digest_url}")
    log(f"[fetch] brief : {brief_url}")
    log(f"[parse] {len(digest.stories)} 头条 / {len(digest.quick_news)} 快讯 / "
        f"{len(brief.papers)} 论文 / {len(brief.notable)} 延伸")

    # ---- 2) 原始素材 --------------------------------------------------------
    outdir.mkdir(parents=True, exist_ok=True)
    source_path = outdir / f"source-{date}.md"
    source_path.write_text(source_text + "\n", encoding="utf-8")
    log(f"[write] {source_path}（{len(source_text)} chars）")

    # ---- 预检 ---------------------------------------------------------------
    import shutil
    if args.llm == "pi" and not args.tts_only:
        miss = []
        if not shutil.which("pi"):
            miss.append("pi 命令（npm i -g @earendil-works/pi-coding-agent / setup_pi.ps1）")
        if not os.getenv("DEEPSEEK_API_KEY"):
            miss.append("DEEPSEEK_API_KEY")
        if miss:
            log(f"[warn] pi 改写前置条件缺失：{', '.join(miss)}。")
            if not args.dry_run:
                log("[warn] 已仅产出原始素材后退出（请运行 setup_pi.ps1 并配置 .env）。")
                log.close()
                return 2
    if args.tts == "doubao" and not (os.getenv("VOLC_APP_ID")
                                     and os.getenv("VOLC_API_KEY") and speaker):
        log("[warn] 豆包 TTS 凭据/音色缺失（VOLC_APP_ID/VOLC_API_KEY/音色）：将跳过音频合成。")
        if not args.dry_run:
            args.tts = "none"
    if args.tts == "qwen" and not QWEN_REF.exists():
        log(f"[warn] qwen 参考音色缺失：{QWEN_REF}（用 qwen_tts/make_ref.py 生成）：将跳过音频合成。")
        if not args.dry_run:
            args.tts = "none"

    rewriter = "pi agent + DeepSeek" if args.llm == "pi" else "LLM（OpenAI 兼容）"
    # qwen 默认带 -myvoice 后缀（克隆音色），doubao 用命令行后缀（默认无）
    eff_suffix = (args.audio_suffix or "-myvoice") if args.tts == "qwen" else args.audio_suffix
    voice_label = ("qwen:my_voice3" if args.tts == "qwen"
                   else (speaker or "-") if args.tts == "doubao" else "-")

    # ---- 3) 改写 + 4) TTS ---------------------------------------------------
    concise_audio = None
    sync_segments: list[str] | None = None   # 卡点用：concise 正文分段
    sync_durs: list[float] | None = None     # 卡点用：各段真实时长
    # 是否对 concise 走「分段合成→精确卡点」路径
    want_sync = args.video and args.tts == "doubao" and "concise" in modes
    for mode in modes:
        kind = "简洁版" if mode == "concise" else "完整版"
        md_path = outdir / f"broadcast-{date}-{mode}.md"
        mp3_path = audio_dir / f"broadcast-{date}-{mode}{eff_suffix}.mp3"

        if args.dry_run:
            action = "tts-only(已有稿)" if args.tts_only else f"rewrite({args.llm})"
            log(f"[plan] {kind}: {action} → {md_path}"
                + ("" if args.tts == "none" else f"  →  tts({args.tts},{voice_label}) → {mp3_path}"))
            continue

        if args.tts_only:
            if not md_path.exists():
                log(f"[err ] {kind}：未找到已有文稿 {md_path}，跳过。")
                continue
            content = md_path.read_text(encoding="utf-8")
            log(f"[skip] {kind}：复用已有文稿 {md_path}")
        else:
            log(f"[llm ] 生成{kind}（{args.llm}）…")
            try:
                script = gb.rewrite(source_text, mode, backend=args.llm)
            except SystemExit as e:
                log(f"[err ] {kind}改写失败：{e}")
                continue
            content = gb.wrap_header(kind, date, rewriter) + script + "\n"
            md_path.write_text(content, encoding="utf-8")
            log(f"[write] {md_path}（正文 {len(script)} chars）")

        ok = False
        if args.tts == "doubao" and mode == "concise" and want_sync:
            segs = gb.split_segments(strip_header(content))
            log(f"[tts ] 卡点模式：concise 切成 {len(segs)} 段逐段合成…")
            durs = synth_segmented(segs, mp3_path, log, speaker)
            if durs:
                ok = True
                sync_segments, sync_durs = segs, durs
            else:  # 分段失败 → 回退整段合成
                ok = run_tts(strip_header(content), mp3_path, log, speaker=speaker)
        elif args.tts == "doubao":
            ok = run_tts(strip_header(content), mp3_path, log, speaker=speaker)
        elif args.tts == "qwen":
            ok = run_qwen(md_path, mp3_path, eff_suffix, log)
        if ok and mode == "concise":
            concise_audio = mp3_path

    # ---- 5) 小红书竖屏视频（基于 concise 音频）------------------------------
    if concise_audio is None:  # tts=none 时回退到已存在的 concise 音频
        cand = audio_dir / f"broadcast-{date}-concise{eff_suffix}.mp3"
        concise_audio = cand if cand.exists() else None
    # 片头：默认自动探测，--no-intro 关闭
    intro_path = None
    if not args.no_intro:
        cand = Path(args.intro) if args.intro else (REPO_ROOT / "片头" / "小猫片头_1x1_4s.mp4")
        intro_path = cand if cand.exists() else None
    if args.video and not args.dry_run and concise_audio and concise_audio.exists():
        try:
            import make_xhs_video_html as xhs
            if not Path(xhs.FFMPEG).exists():
                raise RuntimeError(f"未找到 ffmpeg：{xhs.FFMPEG}")
            mp4 = audio_dir / f"xhs-{date}-concise{eff_suffix}.mp4"
            if intro_path:
                log(f"[video] 片头：{intro_path}")
            if sync_segments and sync_durs:
                log(f"[video] 卡点模式：按 {len(sync_segments)} 段生成同款卡片（LLM）…")
                cards = gb.make_cards_synced(sync_segments, backend=args.llm)
                log(f"[video] 渲染 {len(cards)} 张卡 + 精确卡点合成 → {mp4}")
                xhs.build_xhs_video(cards, concise_audio, mp4, date=date,
                                    seg_durations=sync_durs, intro_path=intro_path)
            else:
                log("[video] 生成小红书卡片文案（LLM）…")
                cards = gb.make_cards(source_text, backend=args.llm)
                log(f"[video] 渲染 {len(cards)} 张卡 + 合成 → {mp4}")
                xhs.build_xhs_video(cards, concise_audio, mp4, date=date,
                                    intro_path=intro_path)
            log(f"[video] 完成 → {mp4}（{mp4.stat().st_size/1e6:.2f} MB）")
        except Exception as e:  # noqa: BLE001
            log(f"[warn] 小红书视频生成失败（跳过）：{str(e)[:300]}")
    elif args.video and args.dry_run:
        log(f"[plan] video: make_cards({args.llm}) → 渲染卡片 → ffmpeg → "
            f"{audio_dir / f'xhs-{date}-concise{eff_suffix}.mp4'}")

    log("==== 完成 ====")
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

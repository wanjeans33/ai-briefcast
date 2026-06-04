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


def main() -> int:
    ap = argparse.ArgumentParser(description="AI Briefcast 每日全流程编排")
    ap.add_argument("--date", help="指定日期 YYYY-MM-DD（默认取各站最新一期）")
    ap.add_argument("--modes", default="concise,full", help="逗号分隔：concise,full")
    ap.add_argument("--llm", choices=["pi", "api"], default="pi",
                    help="改写后端：pi（pi agent + DeepSeek，默认）或 api（OpenAI 兼容直连）")
    ap.add_argument("--tts", choices=["doubao", "none"], default="doubao",
                    help="TTS 后端：doubao（默认）或 none（只出文稿）")
    ap.add_argument("--doubao-speaker",
                    help="豆包音色 ID；缺省优先用 VOLC_SPEAKER2（你的克隆音色），再回退 VOLC_SPEAKER")
    ap.add_argument("--audio-suffix", default="",
                    help="音频文件名后缀，如 -myvoice（便于和其他音色对比，不覆盖）")
    ap.add_argument("--tts-only", action="store_true",
                    help="跳过改写，直接对已存在的 broadcast-<日期>-<mode>.md 重新合成音频")
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
        f" voice={speaker or '-'}{' tts-only' if args.tts_only else ''}"
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

    rewriter = "pi agent + DeepSeek" if args.llm == "pi" else "LLM（OpenAI 兼容）"

    # ---- 3) 改写 + 4) TTS ---------------------------------------------------
    for mode in modes:
        kind = "简洁版" if mode == "concise" else "完整版"
        md_path = outdir / f"broadcast-{date}-{mode}.md"
        mp3_path = audio_dir / f"broadcast-{date}-{mode}{args.audio_suffix}.mp3"

        if args.dry_run:
            action = "tts-only(已有稿)" if args.tts_only else f"rewrite({args.llm})"
            log(f"[plan] {kind}: {action} → {md_path}"
                + ("" if args.tts == "none" else f"  →  tts({args.tts},{speaker}) → {mp3_path}"))
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

        if args.tts == "doubao":
            run_tts(strip_header(content), mp3_path, log, speaker=speaker)

    log("==== 完成 ====")
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日成品单一驱动：读 output/<date>/episode.yaml，跑完 校验→音频→卡片→视频→字幕→封面→publish。

用法：
    python scripts/make_episode.py --date 2026-07-11              # 全流程（音频已存在则复用）
    python scripts/make_episode.py --date 2026-07-11 --dry-run    # 只做校验（字数/emoji/结构），不产出
    python scripts/make_episode.py --date 2026-07-11 --force-audio  # 强制重新合成音频

episode.yaml 结构见 output/2026-07-11/episode.yaml（参考样例）。
内置 QA（任一失败即中止）：
  - 文稿正文 ≤ CHAR_BUDGET 字（2026-07-10 时长失控教训）
  - 卡片 icon emoji 码位白名单（U+1FA70 以上的新 emoji 渲染成空框，2026-07-07/07-10 两次踩坑）
  - GROUPS 组数 == 音频段数
  - ffprobe 成片时长 ≈ 旁白 + 片尾 1s（±0.8s）、2160×3840
  - 自动抽 QA 帧到 video/qa/
经验参数全部沿用 0705-0711 已验证值：rate 36、XFADE 逐卡补偿、circle_photo(photo,760)、
center=(1080, 0.24*3840)、片尾 1.0s。
"""
import argparse
import json
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import generate_broadcast as gb
import make_xhs_video_html as xhs
import run_daily as rd
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
CHAR_BUDGET = 820
OUTRO_SEC = 1.0
DUR_TOL = 0.8
PHOTO = REPO / "片头" / "图片_20260606072137.png"
MW = 1.5  # 内容卡组内权重（补充卡=1）

# —— emoji 白名单规则：拒绝 U+1FA70 及以上（Unicode 12+ 扩展区，渲染字体不支持）——
EMOJI_BAD_START = 0x1FA70


def die(msg: str):
    print(f"[FAIL] {msg}", flush=True)
    sys.exit(1)


def check_icons(groups):
    bad = []
    for gi, g in enumerate(groups):
        for card in g["cards"]:
            ic = card.get("icon", "")
            for ch in ic:
                if ord(ch) >= EMOJI_BAD_START:
                    bad.append(f"组{gi} 「{card.get('title', card.get('kind'))}」 icon={ic!r} "
                               f"含 U+{ord(ch):X}（≥U+1FA70，会渲染成空框）")
    if bad:
        die("emoji 白名单校验不通过：\n  " + "\n  ".join(bad))
    print("[qa] icon 码位校验通过", flush=True)


def load_script_segments(md_path: Path):
    md = md_path.read_text(encoding="utf-8")
    segs = gb.split_segments(rd.strip_header(md))
    total = sum(len(s) for s in segs)
    print(f"[qa] 文稿 {len(segs)} 段 / {total} 字（预算 {CHAR_BUDGET}）", flush=True)
    if total > CHAR_BUDGET:
        die(f"文稿 {total} 字超预算 {CHAR_BUDGET}，先删稿再出片（7/10 的 136.9s 教训）")
    return segs


def expand_cards(groups):
    cards, weights = [], []
    for g in groups:
        gc, gw = [], []
        for card in g["cards"]:
            kind = card["kind"]
            gc.append(card)
            gw.append(MW if kind == "point" else 1.0)
        if len(gc) == 1:
            gw = [1.0]
        cards.append((gc, gw))
    return cards


def ffprobe_duration(path: Path) -> tuple:
    ff = Path(xhs.FFMPEG)
    fp = ff.with_name("ffprobe.exe")
    out = subprocess.run(
        [str(fp), "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    j = json.loads(out)
    w = j["streams"][0]["width"]; h = j["streams"][0]["height"]
    dur = float(j["format"]["duration"])
    return w, h, dur


def extract_qa_frames(video: Path, total: float, qa_dir: Path):
    qa_dir.mkdir(parents=True, exist_ok=True)
    ts = [0.5, total * 0.3, total * 0.6, total * 0.9, max(total - 0.3, 0.5)]
    for t in ts:
        out = qa_dir / f"qa-{t:.1f}.png"
        subprocess.run([xhs.FFMPEG, "-v", "error", "-ss", f"{t:.2f}", "-i", str(video),
                        "-frames:v", "1", "-y", str(out)], check=True)
    print(f"[qa] 抽帧 {len(ts)} 张 → {qa_dir}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force-audio", action="store_true")
    args = ap.parse_args()

    DATE = args.date
    OUTD = REPO / "output" / DATE
    ep_path = OUTD / "episode.yaml"
    if not ep_path.exists():
        die(f"缺 {ep_path}，先按样例（output/2026-07-11/episode.yaml）写好当天数据")
    ep = yaml.safe_load(ep_path.read_text(encoding="utf-8"))

    md_path = OUTD / "scripts" / ep["script"]
    if not md_path.exists():
        die(f"缺文稿 {md_path}")

    groups = ep["groups"]
    segs = load_script_segments(md_path)
    # 组数 = 段数（封面组、每条内容组、CTA 组）
    if len(groups) != len(segs):
        die(f"GROUPS {len(groups)} 组 ≠ 音频 {len(segs)} 段，检查 episode.yaml 分组")
    check_icons(groups)
    print("[qa] 结构校验通过", flush=True)
    if args.dry_run:
        print("[done] dry-run 校验全部通过")
        return

    for sub in ("audio", "video", "cover", "cards"):
        (OUTD / sub).mkdir(parents=True, exist_ok=True)

    # —— 音频（存在则复用，不重配音）——
    AUDIO = OUTD / "audio" / f"broadcast-{DATE}-spacex.mp3"
    DJS = OUTD / "audio" / "durs.json"
    if AUDIO.exists() and DJS.exists() and not args.force_audio:
        _dj = json.loads(DJS.read_text(encoding="utf-8"))
        seg_durs = _dj["durs"] if isinstance(_dj, dict) else _dj
        print(f"[audio] 复用已有音频 {sum(seg_durs):.1f}s（--force-audio 可重合成）", flush=True)
    else:
        rd.load_dotenv(REPO)
        import os
        os.environ["VOLC_SPEECH_RATE"] = str(ep.get("rate", 36))
        spk = os.getenv("VOLC_SPEAKER2") or os.getenv("VOLC_SPEAKER")
        log = rd.Logger(REPO / "logs" / f"run-{DATE}-episode.log")
        seg_durs = rd.synth_single_synced(segs, AUDIO, log, spk)
        log.close()
        if not seg_durs:
            die("TTS 合成失败")
        DJS.write_text(json.dumps({"segments": len(segs), "durs": seg_durs,
                                   "labels": [s[:18] for s in segs]}, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        print(f"[audio] 合成完成 {sum(seg_durs):.1f}s", flush=True)

    if len(seg_durs) != len(groups):
        die(f"音频 {len(seg_durs)} 段 ≠ GROUPS {len(groups)} 组")

    # —— 展开卡片 + 逐卡时长 ——
    expanded = expand_cards(groups)
    cards, card_durs = [], []
    for (gc, gw), sd in zip(expanded, seg_durs):
        s = sum(gw)
        for cd, wi in zip(gc, gw):
            cards.append(cd)
            card_durs.append(sd * wi / s)
    print(f"[plan] {len(cards)} 卡 旁白 {sum(card_durs):.1f}s", flush=True)

    # —— 渲染 + 出片（0705-0711 已验证流程）——
    CDIR = REPO / f"assets/xhs_cards_{DATE}"
    VDIR = OUTD / "video"
    MAIN = str(VDIR / "_main.mp4"); OUTRO = str(VDIR / "_outro.mp4")
    BASE = str(VDIR / f"xhs-{DATE}-spacex.mp4")
    SUB = str(VDIR / f"xhs-{DATE}-spacex-sub.mp4")

    pngs = xhs.render_cards(cards, CDIR, "")
    cw, ch = Image.open(pngs[-1]).size
    if (cw, ch) != (2160, 3840):
        die(f"卡片尺寸 {cw}x{ch} ≠ 2160x3840")
    print(f"[cards] {len(pngs)} PNG 尺寸正常", flush=True)

    photo = xhs.circle_photo(str(PHOTO), 760)
    center = (1080, int(0.24 * 3840))
    plain = str(Path(pngs[-1]).with_suffix(".plain.png"))
    shutil.copy(pngs[-1], plain)
    xhs.place_photo_on_card(pngs[-1], photo, center)
    xhs.composite(pngs, [d + xhs.XFADE for d in card_durs], str(AUDIO), MAIN)  # 逐卡 +XFADE
    xhs.build_shrink_outro(plain, photo, center, OUTRO, dur=OUTRO_SEC)
    xhs.concat_clips([MAIN, OUTRO], BASE)
    xhs.add_subtitles(segs, seg_durs, str(AUDIO), BASE, SUB)

    # —— ffprobe 断言 + 抽帧 ——
    w, h, dur = ffprobe_duration(Path(SUB))
    want = sum(seg_durs) + OUTRO_SEC
    if (w, h) != (2160, 3840):
        die(f"成片分辨率 {w}x{h} ≠ 2160x3840")
    if abs(dur - want) > DUR_TOL:
        die(f"成片时长 {dur:.2f}s 偏离预期 {want:.2f}s 超过 {DUR_TOL}s（查 XFADE/片尾）")
    print(f"[qa] 成片 {w}x{h} {dur:.2f}s（预期 {want:.2f}±{DUR_TOL}s）通过", flush=True)
    extract_qa_frames(Path(SUB), dur, VDIR / "qa")

    # —— 归档卡片 + 清理中间件 ——
    cards_out = OUTD / "cards"
    for p in Path(CDIR).glob("card-*.png"):
        shutil.copy(p, cards_out / p.name)
    for tmp in (MAIN, OUTRO):
        Path(tmp).unlink(missing_ok=True)

    # —— 3:4 封面 ——
    cov = ep.get("cover3x4")
    if cov:
        import make_cover as mc
        mc.BRAND = cov.get("brand", "🍊 柿子树下的猫 ｜ AI 速览")
        mc.KICKER = cov["kicker"]; mc.BIG = cov["big"]; mc.ROWS = cov["rows"]
        mc.DATE = cov.get("date", f"@AI Briefcast · {DATE[5:].replace('-0', '/').replace('-', '/')}")
        cover_png = OUTD / "cover" / f"cover-{DATE}.png"
        sys.argv = ["make_cover.py", str(cover_png)]
        mc.main()

    # —— publish.json（caption.md 需已存在）——
    if (OUTD / "caption.md").exists():
        subprocess.run([sys.executable, str(REPO / "scripts" / "make_publish.py"),
                        "--date", DATE], check=True)
    else:
        print("[warn] 缺 caption.md，跳过 publish.json", flush=True)

    print(f"[done] {SUB}", flush=True)


if __name__ == "__main__":
    main()

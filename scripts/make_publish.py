#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把某天的成品汇成 publish.json —— 投稿（小红书）的单一数据源。

读取 output/<date>/caption.md（标题/正文/标签）+ 定位 video/-sub.mp4 与 cover/*.png（绝对路径），
写出 output/<date>/publish.json。投稿走 Route B（Claude-in-Chrome 驱动创作者后台），
本脚本只负责「把发什么、发哪些文件」结构化，不做任何上传动作。

用法：
  python scripts/make_publish.py --date 2026-06-19
  python scripts/make_publish.py --date 2026-06-19 --visibility public
  python scripts/make_publish.py --date 2026-06-19 --schedule "2026-06-20 08:00"
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
XHS_TITLE_MAX = 20   # 小红书标题上限（全角字符）


def _sections(md: str) -> list[tuple[str, str]]:
    """按 '## ' 切成 [(header, body)]。"""
    out, header, buf = [], None, []
    for line in md.splitlines():
        if line.startswith("## "):
            if header is not None:
                out.append((header, "\n".join(buf).strip()))
            header, buf = line[3:].strip(), []
        elif header is not None:
            buf.append(line)
    if header is not None:
        out.append((header, "\n".join(buf).strip()))
    return out


def parse_caption(md: str) -> dict:
    """从 caption.md 抽出 title / body / tags / chapters。"""
    secs = _sections(md)
    title, body, tags, chapters = "", "", [], []
    for header, content in secs:
        if header.startswith("标题") and not header.startswith("备选"):
            # 取第一行非空内容作为标题
            title = next((l.strip() for l in content.splitlines() if l.strip()), "")
        elif header.startswith("正文"):
            body = content.strip()
        elif "标签" in header and "备选" not in header:
            tags = re.findall(r"#[^\s#]+", content)
        elif header.startswith("章节"):
            # 每行 "MM:SS 标题"，平台章节栏可逐行粘贴
            for line in content.splitlines():
                m = re.match(r"\s*((?:\d{1,2}:)?\d{1,2}:\d{2})\s+(.+)", line)
                if m:
                    chapters.append({"time": m.group(1), "title": m.group(2).strip()})
    return {"title": title, "body": body, "tags": tags, "chapters": chapters}


def _abspath(p: Path) -> str:
    return str(p.resolve())


def build_publish(date: str, visibility: str, schedule_at: str | None) -> dict:
    day = REPO_ROOT / "output" / date
    cap = day / "caption.md"
    if not cap.exists():
        raise SystemExit(f"找不到 {cap}（先做完文案步骤再生成 publish.json）")
    parsed = parse_caption(cap.read_text(encoding="utf-8"))

    # 视频：优先带字幕的发布版 *-sub.mp4
    vids = sorted((day / "video").glob("*-sub.mp4"))
    if not vids:
        vids = [p for p in sorted((day / "video").glob("*.mp4")) if not p.name.startswith("_")]
    if not vids:
        raise SystemExit(f"找不到视频：{day/'video'}/*-sub.mp4")
    video = vids[0]

    # 封面：小红书用 3:4 竖版（排除抖音的 -4x3 横版，否则字符序会让它排在前面被选中）
    covers = sorted(p for p in (day / "cover").glob("*.png") if not p.stem.endswith("-4x3"))
    if not covers:
        raise SystemExit(f"找不到 3:4 封面：{day/'cover'}/cover-{date}.png")
    cover = covers[0]
    # 抖音横版封面（可选）
    land = day / "cover" / f"cover-{date}-4x3.png"
    cover_landscape = _abspath(land) if land.exists() else None

    content = parsed["body"]
    if parsed["tags"]:
        content = (content + "\n\n" + " ".join(parsed["tags"])).strip()

    return {
        "date": date,
        "title": parsed["title"],
        "title_len": len(parsed["title"]),
        "body": parsed["body"],
        "tags": parsed["tags"],
        "content": content,            # 正文 + 标签，可直接粘进正文框
        "chapters": parsed["chapters"],  # [{time, title}]，小红书/抖音章节栏用
        "video": _abspath(video),
        "cover": _abspath(cover),                  # 3:4 竖版（小红书）
        "cover_landscape": cover_landscape,        # 4:3 横版（抖音），无则 None
        "visibility": visibility,      # self=仅自己可见 / friends / public
        "schedule_at": schedule_at,    # None=不定时；"YYYY-MM-DD HH:MM"
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 output/<date>/publish.json")
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--visibility", choices=["self", "friends", "public"], default="self",
                    help="可见性：self=仅自己可见（首条默认）/ friends / public")
    ap.add_argument("--schedule", dest="schedule_at", default=None,
                    help='定时发布时间 "YYYY-MM-DD HH:MM"（缺省＝不定时）')
    args = ap.parse_args()

    data = build_publish(args.date, args.visibility, args.schedule_at)
    out = REPO_ROOT / "output" / args.date / "publish.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[done] {out}")
    print(f"  标题（{data['title_len']}字）：{data['title']}")
    if data["title_len"] > XHS_TITLE_MAX:
        print(f"  ⚠ 标题超过小红书 {XHS_TITLE_MAX} 字上限，投稿时需精简")
    print(f"  视频：{data['video']}")
    print(f"  封面 3:4：{data['cover']}")
    if data.get("cover_landscape"):
        print(f"  封面 4:3：{data['cover_landscape']}")
    if data["chapters"]:
        print(f"  章节 {len(data['chapters'])} 个：" +
              " / ".join(f"{c['time']} {c['title']}" for c in data["chapters"]))
    print(f"  可见性：{data['visibility']}  定时：{data['schedule_at'] or '否'}")
    print(f"  标签 {len(data['tags'])} 个：{' '.join(data['tags'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

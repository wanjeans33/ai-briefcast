#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小红书笔记数据复盘：读创作者后台导出的 笔记列表明细表.xlsx，出选题/钩子复盘。

用法：python scripts/analyze_notes.py [xlsx路径]（默认仓库根 笔记列表明细表.xlsx）
输出：终端排行 + output/analytics-summary.md（供选题环节参考）
"""
import sys
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parent.parent
XLSX = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "笔记列表明细表.xlsx"

df = pd.read_excel(XLSX, header=1)
df["发布时间"] = pd.to_datetime(df["首次发布时间"], format="%Y年%m月%d日%H时%M分%S秒")
df["日期"] = df["发布时间"].dt.date
df["小时"] = df["发布时间"].dt.hour
df = df[df["曝光"] > 0].copy()          # 剔除刚发布还没跑量的

# 派生指标
df["互动"] = df[["点赞", "评论", "收藏", "分享"]].sum(axis=1)
df["互动率"] = (df["互动"] / df["观看量"]).round(3)          # 每次观看带来的互动
df["涨粉每千曝光"] = (df["涨粉"] / df["曝光"] * 1000).round(2)
df["观看转化"] = (df["观看量"] / df["曝光"]).round(3)

cols = ["笔记标题", "日期", "体裁", "曝光", "观看量", "封面点击率", "互动率", "涨粉", "涨粉每千曝光", "人均观看时长", "小时"]

def top(d, by, n=8):
    return d.sort_values(by, ascending=False).head(n)[cols].to_string(index=False, max_colwidth=24)

lines = []
def sec(title, body):
    lines.append(f"\n## {title}\n\n```\n{body}\n```")

lines.append(f"# 笔记数据复盘（{df['日期'].min()} ~ {df['日期'].max()}，{len(df)} 条）")

sec("曝光 Top8（算法给了多少量）", top(df, "曝光"))
sec("封面点击率 Top8（钩子有没有人点）", top(df, "封面点击率"))
sec("涨粉 Top8（真正的转化）", top(df, "涨粉"))
sec("互动率 Top8（看了之后动没动手）", top(df, "互动率"))

vid = df[df["体裁"] == "视频"]
tuw = df[df["体裁"] == "图文"]
comp = pd.DataFrame({
    "视频": [len(vid), vid["曝光"].median(), vid["封面点击率"].median(), vid["涨粉"].sum(), vid["互动率"].median()],
    "图文": [len(tuw), tuw["曝光"].median(), tuw["封面点击率"].median(), tuw["涨粉"].sum(), tuw["互动率"].median()],
}, index=["条数", "曝光中位数", "点击率中位数", "涨粉合计", "互动率中位数"]).round(3)
sec("体裁对比（视频 vs 图文）", comp.to_string())

df["旬"] = df["发布时间"].dt.strftime("%m月") + (df["发布时间"].dt.day <= 15).map({True: "上半", False: "下半"})
trend = df[df["体裁"] == "视频"].groupby("旬").agg(
    条数=("曝光", "size"), 曝光中位=("曝光", "median"), 点击率中位=("封面点击率", "median"),
    涨粉合计=("涨粉", "sum"), 人均观看中位=("人均观看时长", "median")).round(3)
sec("视频分期趋势（按半月）", trend.to_string())

hour = df[df["体裁"] == "视频"].copy()
hour["时段"] = pd.cut(hour["小时"], [0, 6, 12, 24], labels=["凌晨0-6", "早间6-12", "午后12-24"], right=False)
hb = hour.groupby("时段", observed=True).agg(条数=("曝光", "size"), 曝光中位=("曝光", "median"),
                                             点击率中位=("封面点击率", "median"), 涨粉合计=("涨粉", "sum")).round(3)
sec("发布时段对比（视频）", hb.to_string())

out = REPO / "output" / "analytics-summary.md"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print(f"\n[done] 已写入 {out}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Briefcast - 每日播报稿生成器 / Daily broadcast script generator

职责分工：
  1) 抓取 + 解析（Python）：从两个来源抓取「今天」最新一期的新闻**详情子页面**，
     解析出干净的原始素材（标题 / 正文 / 论文 / 快讯 / 观察）。
  2) 改写（LLM）：把原始素材交给 OpenAI 兼容的大模型，改写成自然、适合朗读的
     TTS 播报稿，分别生成简洁版与完整版。

来源：
  - AI 资讯速览  https://ai-digest.liziran.com/zh/
  - AI 论文简报  https://ai-brief.liziran.com/zh/

LLM 配置（环境变量，OpenAI 兼容接口）：
  LLM_BASE_URL   例如 https://dashscope.aliyuncs.com/compatible-mode/v1
                      https://api.deepseek.com
                      https://ark.cn-beijing.volces.com/api/v3
                      https://api.openai.com/v1
  LLM_API_KEY    （缺省回退到 OPENAI_API_KEY）
  LLM_MODEL      例如 qwen-plus / deepseek-chat / doubao-pro-32k / gpt-4o-mini

用法:
  python scripts/generate_broadcast.py                  # 抓最新一期，LLM 生成两版
  python scripts/generate_broadcast.py --date 2026-06-02
  python scripts/generate_broadcast.py --dump-raw       # 只抓取解析，输出原始素材
  python scripts/generate_broadcast.py --modes concise  # 只生成简洁版
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

DIGEST_HOME = "https://ai-digest.liziran.com/zh/"
BRIEF_HOME = "https://ai-brief.liziran.com/zh/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AI-Briefcast/0.1)"}
TIMEOUT = 30


# --------------------------------------------------------------------------- #
# 数据结构
# --------------------------------------------------------------------------- #
@dataclass
class Story:
    index: str
    title: str
    paragraphs: list[str] = field(default_factory=list)


@dataclass
class QuickNews:
    index: str
    title: str
    body: str
    source: str = ""


@dataclass
class Digest:
    date: str
    headline: str
    url: str
    stories: list[Story] = field(default_factory=list)
    quick_news: list[QuickNews] = field(default_factory=list)


@dataclass
class Paper:
    index: str
    tag: str
    title: str
    body: str = ""
    original: str = ""


@dataclass
class Notable:
    index: str
    title: str
    tag: str
    desc: str


@dataclass
class Brief:
    date: str
    headline: str
    url: str
    overview: list[str] = field(default_factory=list)
    papers: list[Paper] = field(default_factory=list)
    notable: list[Notable] = field(default_factory=list)
    observation: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# 抓取与解析
# --------------------------------------------------------------------------- #
def fetch(url: str) -> BeautifulSoup:
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "lxml")


def latest_article_url(home: str, segment: str, date: str | None) -> str:
    """从首页找到指定日期(或最新一期)的正文页 URL，排除 *-sources 页。"""
    soup = fetch(home)
    candidates: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if f"/{segment}/" not in href or href.endswith("-sources.html"):
            continue
        candidates.append(href)
    if date:
        candidates = [h for h in candidates if date in h] or candidates
    if not candidates:
        raise RuntimeError(f"未在 {home} 找到 /{segment}/ 正文链接")
    return urljoin(home, candidates[0])


def _txt(el) -> str:
    return el.get_text(" ", strip=True) if el else ""


def _strip_num(text: str) -> str:
    return re.sub(r"^\s*\d{1,2}\s*", "", text).strip()


def parse_digest(url: str) -> Digest:
    soup = fetch(url)
    main = soup.find("main") or soup.body
    headline = _txt(soup.title).split("|")[0].strip()
    date = _extract_date(soup, url)

    stories: list[Story] = []
    for sec in main.find_all("div", class_="article-section"):
        h2 = sec.find("h2")
        if not h2:
            continue
        title = _strip_num(_txt(h2))
        paras = [
            _txt(p)
            for p in sec.find_all("p")
            if not p.find_parent(class_=["key-tags", "sources-list"]) and _txt(p)
        ]
        stories.append(Story(index=f"{len(stories) + 1:02d}", title=title, paragraphs=paras))

    quick: list[QuickNews] = []
    for item in main.find_all("div", class_="quick-news-item"):
        num = _txt(item.find("span", class_="paper-num"))
        body_div = item.find("div", class_="quick-news-body")
        strong = body_div.find("strong") if body_div else None
        title = _txt(strong)
        source = _txt(item.find("span", class_="source-domain"))
        full = _txt(body_div)
        body = full.replace(title, "", 1).replace(source, "").strip()
        quick.append(QuickNews(index=num or f"{len(quick) + 1:02d}",
                               title=title, body=body, source=source))

    return Digest(date=date, headline=headline, url=url, stories=stories, quick_news=quick)


def parse_brief(url: str) -> Brief:
    soup = fetch(url)
    main = soup.find("main") or soup.body
    headline = _txt(soup.title).split("|")[0].strip()
    date = _extract_date(soup, url)

    brief = Brief(date=date, headline=headline, url=url)

    ov = main.find("section", class_="section-overview")
    if ov:
        brief.overview = [_txt(li) for li in ov.find_all("li") if _txt(li)]

    feat = main.find("section", class_="section-featured")
    if feat:
        cur: Paper | None = None
        for el in feat.find_all(["h3", "p"]):
            if el.name == "h3":
                num = _txt(el.find("span", class_="paper-num"))
                rest = _strip_num(_txt(el))
                parts = rest.split(" ", 1)
                tag = parts[0] if len(parts) == 2 else ""
                title = parts[1] if len(parts) == 2 else rest
                cur = Paper(index=num, tag=tag, title=title)
                brief.papers.append(cur)
            elif cur is not None:
                t = _txt(el)
                if t.startswith("原文"):
                    cur.original = re.sub(r"^原文[:：]\s*", "", t).strip()
                elif t:
                    cur.body = (cur.body + " " + t).strip() if cur.body else t

    notable_sec = main.find("section", class_="section-notable")
    if notable_sec:
        for item in notable_sec.find_all("div", class_="notable-item"):
            num = _txt(item.find("span", class_="paper-num"))
            strong = item.find("strong")
            tag = _txt(item.find("a", class_="paper-tag"))
            desc = _txt(item.find("span", class_="notable-desc"))
            desc = re.sub(r"\s*链接\s*$", "", desc).strip()
            brief.notable.append(Notable(index=num, title=_txt(strong), tag=tag, desc=desc))

    obs = main.find("section", class_="section-observation")
    if obs:
        brief.observation = [_txt(p) for p in obs.find_all("p") if _txt(p)]

    return brief


def _extract_date(soup: BeautifulSoup, url: str) -> str:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", url)
    if m:
        return m.group(1)
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", soup.get_text())
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
    return "unknown"


# --------------------------------------------------------------------------- #
# 原始素材序列化（喂给 LLM）
# --------------------------------------------------------------------------- #
def build_source_text(digest: Digest, brief: Brief) -> str:
    """把解析结果拼成结构清晰的纯文本，作为 LLM 的输入素材。"""
    out: list[str] = []
    date = digest.date if digest.date != "unknown" else brief.date
    out.append(f"# 日期：{date}")

    out.append("\n## 一、行业新闻（AI 资讯速览）")
    out.append(f"来源页：{digest.url}")
    for s in digest.stories:
        out.append(f"\n### 头条 {s.index}：{s.title}")
        out.extend(s.paragraphs)
    if digest.quick_news:
        out.append("\n### 今日快讯")
        for q in digest.quick_news:
            src = f"（来源 {q.source}）" if q.source else ""
            out.append(f"- {q.title}：{q.body}{src}")

    out.append("\n## 二、论文简报（AI 论文简报）")
    out.append(f"来源页：{brief.url}")
    if brief.overview:
        out.append("\n### 今日概览")
        out.extend(f"- {x}" for x in brief.overview)
    out.append("\n### 重点论文")
    for p in brief.papers:
        tag = f"[{p.tag}] " if p.tag else ""
        out.append(f"\n#### 论文 {p.index}：{tag}{p.title}")
        if p.body:
            out.append(p.body)
        if p.original:
            out.append(f"原始论文标题：{p.original}")
    if brief.notable:
        out.append("\n### 也值得关注")
        for n in brief.notable:
            tag = f"（{n.tag}）" if n.tag else ""
            out.append(f"- {n.title}{tag}：{n.desc}")
    if brief.observation:
        out.append("\n### 今日观察")
        out.extend(brief.observation)

    return "\n".join(out)


# --------------------------------------------------------------------------- #
# LLM 改写
# --------------------------------------------------------------------------- #
SYSTEM_PROMPT = (
    "你是一档中文 AI 新闻播客《AI Briefcast》的稿件撰写人。"
    "你会拿到当天结构化的原始新闻素材，需要把它改写成一篇自然、口语化、"
    "适合主播朗读、也适合直接送入 TTS 合成的播报稿。要求：\n"
    "1. 只使用素材中提供的事实，不要杜撰、不要添加素材里没有的数据或观点；\n"
    "2. 语言自然流畅，像在对听众讲话，段落之间有合理的过渡；\n"
    "3. 为方便 TTS 朗读：数字、年份、日期、百分比尽量写成口语化的中文读法"
    "（如「二零二六年六月二号」「百分之四十一点九」）；\n"
    "4. 公司名、产品名、模型名、论文等专有名词可保留英文原文（如 Anthropic、MoE、"
    "RTX Spark），其余尽量中文；\n"
    "5. 不要写开场白／自我介绍／日期问候（这部分由固定模板提供），"
    "直接从第一条要闻讲起；结尾保留一句简短收尾语；\n"
    "6. 直接输出可朗读的正文纯文本，不要使用 Markdown 标题、列表符号或表格。"
)

# 固定开场白：每天自动套用，仅替换日期（{date_cn} 为口语化中文日期）。
FIXED_INTRO = (
    "大家好，这里是柿子树下的猫wanjeans，三分钟带你了解AI圈的新鲜事。"
    "今天是{date_cn}，欢迎收听《AI Briefcast》。来看今天的 AI 要闻。"
)

_CN_DIGITS = "零一二三四五六七八九"


def _cn_num(n: int) -> str:
    """1–99 的口语化中文（如 6→六，16→十六，26→二十六）。"""
    if n < 10:
        return _CN_DIGITS[n]
    if n < 20:
        return "十" + (_CN_DIGITS[n % 10] if n % 10 else "")
    tens, ones = divmod(n, 10)
    return _CN_DIGITS[tens] + "十" + (_CN_DIGITS[ones] if ones else "")


def spoken_date(date: str) -> str:
    """'2026-06-06' → '二零二六年六月六号'。"""
    try:
        y, m, d = date.split("-")
        ynum = "".join(_CN_DIGITS[int(c)] for c in y)
        return f"{ynum}年{_cn_num(int(m))}月{_cn_num(int(d))}号"
    except Exception:  # noqa: BLE001
        return date


def fixed_intro(date: str) -> str:
    return FIXED_INTRO.format(date_cn=spoken_date(date))

CONCISE_INSTRUCTION = (
    "请生成【简洁版】播报稿，控制在大约 400–600 字、朗读约 3 分钟：\n"
    "- 只覆盖最重要的内容：三条行业头条各用一两句话点出核心，"
    "再用几句话概括今天值得一提的论文方向；\n"
    "- 快讯、延伸阅读可省略或一笔带过；\n"
    "- 节奏明快，适合通勤快速收听。"
)

FULL_INSTRUCTION = (
    "请生成【完整版】播报稿，内容详尽：\n"
    "- 行业部分：三条头条逐条展开，讲清来龙去脉；今日快讯逐条简述；\n"
    "- 论文部分：五篇重点论文逐篇讲清「做了什么、发现了什么、对谁有用」，"
    "可顺带念出原始论文标题；延伸阅读简要带过；最后呈现今日观察；\n"
    "- 分「行业动态」和「论文速递」两大板块，板块之间有过渡语。"
)


def build_user_prompt(source_text: str, mode: str) -> str:
    instruction = CONCISE_INSTRUCTION if mode == "concise" else FULL_INSTRUCTION
    return f"{instruction}\n\n以下是今天的原始新闻素材：\n\n{source_text}"


def rewrite(source_text: str, mode: str, *, backend: str = "api",
            model: str | None = None) -> str:
    """改写分发：backend = 'pi'（pi agent + DeepSeek）或 'api'（OpenAI 兼容直连）。"""
    if backend == "pi":
        return rewrite_via_pi(source_text, mode)
    return rewrite_with_llm(source_text, mode, model=model)


def rewrite_with_llm(source_text: str, mode: str, *, model: str | None = None) -> str:
    """调用 OpenAI 兼容接口，把原始素材改写成播报稿。"""
    try:
        from openai import OpenAI
    except ImportError as e:  # noqa: BLE001
        raise SystemExit("缺少依赖 openai，请先 `pip install -r requirements.txt`") from e

    base_url = os.getenv("LLM_BASE_URL")
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    model = model or os.getenv("LLM_MODEL")
    if not api_key:
        raise SystemExit("未设置 LLM_API_KEY（或 OPENAI_API_KEY）。")
    if not model:
        raise SystemExit("未设置 LLM_MODEL，例如 qwen-plus / deepseek-chat / gpt-4o-mini。")

    client = OpenAI(base_url=base_url, api_key=api_key)  # base_url=None 时走官方 OpenAI
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(source_text, mode)},
        ],
        temperature=0.6,
    )
    return resp.choices[0].message.content.strip()


# pi agent 的工作目录：含 .pi/settings.json（默认 provider/model 指向 deepseek）
PI_WORKSPACE = Path(__file__).resolve().parent.parent / "automation"


def _pi_command() -> list[str]:
    """返回调用 pi 的命令前缀。

    优先直接用 `node dist/cli.js` 绕过 Windows 的 pi.cmd 批处理封装——经由 cmd.exe
    传多行参数会在第一个换行处被截断，导致 pi 收不到完整 prompt。
    """
    pi_bin = shutil.which("pi")
    if not pi_bin:
        raise SystemExit("未找到 pi 命令，请先安装：npm i -g @earendil-works/pi-coding-agent "
                         "（或运行 scripts/setup_pi.ps1）。")
    node = shutil.which("node")
    cli = (Path(pi_bin).resolve().parent / "node_modules" / "@earendil-works"
           / "pi-coding-agent" / "dist" / "cli.js")
    if node and cli.exists():
        return [node, str(cli)]
    return [pi_bin]  # 退化：直接用 shim（注意多行 prompt 在 Windows 上可能被截断）


def rewrite_via_pi(source_text: str, mode: str, *, workspace: Path | None = None) -> str:
    """通过 pi（https://pi.dev）+ DeepSeek 改写。

    需要：已安装 pi（npm i -g @earendil-works/pi-coding-agent）、已安装 deepseek
    provider 扩展、且环境变量含 DEEPSEEK_API_KEY。模型在 automation/.pi/settings.json
    里通过 defaultProvider/defaultModel 选定。
    """
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise SystemExit("未设置 DEEPSEEK_API_KEY（pi 的 deepseek provider 需要它）。")

    ws = workspace or PI_WORKSPACE
    # 一次性、纯文本改写任务：系统说明 + 指令 + 素材，全部塞进单条 prompt。
    prompt = (f"{SYSTEM_PROMPT}\n\n{build_user_prompt(source_text, mode)}\n\n"
              "（只输出可朗读的播报稿正文本身，不要任何解释、前后缀或 Markdown 代码块。）")
    proc = subprocess.run(
        _pi_command() + ["-p", prompt],
        cwd=str(ws), capture_output=True, text=True, encoding="utf-8",
    )
    if proc.returncode != 0:
        raise SystemExit(f"pi 调用失败（exit {proc.returncode}）：\n{proc.stderr[-800:]}")
    out = (proc.stdout or "").strip()
    if not out:
        raise SystemExit(f"pi 没有返回内容。stderr：\n{proc.stderr[-800:]}")
    return out


# --------------------------------------------------------------------------- #
# 小红书卡片文案（供 make_xhs_video 用）
# --------------------------------------------------------------------------- #
CARDS_SYSTEM = (
    "你是小红书图文卡片文案。把当天的 AI 播报素材改写成一组用于制作 9:16 竖屏卡片的内容，"
    "严格只输出 JSON（不要任何解释、不要 Markdown 代码块）。"
)
CARDS_INSTRUCTION = (
    "输出 JSON，结构为 {\"cards\":[...]}，共 6 张卡，顺序为：\n"
    "1 张 cover + 4 张 point（对应 3 条行业头条 + 1 条论文）+ 1 张 cta。\n"
    "字段：\n"
    "- cover: {\"kind\":\"cover\",\"badge\":\"如 建议收藏 · 每日AI速览\",\"subtitle\":\"如 6月X日 · AI Briefcast\","
    "\"count\":4,\"toc\":[\"逐条列出 4 张 point 的一句话标题，≤14字\"]}\n"
    "- point: {\"kind\":\"point\",\"tag\":\"如 头条 01 · 行业 / 论文 · 搜索Agent\","
    "\"icon\":\"贴切 emoji 如 📱📈🛡️🧪\",\"title\":\"≤10字\","
    "\"body\":\"≤55字，口语化，用 **加粗** 标出关键数字/词\","
    "\"punch\":\"≤16字金句/一句话观点，可 **加粗**\"}\n"
    "- cta:  {\"kind\":\"cta\",\"title\":\"如 明天见\",\"subtitle\":\"一句话\",\"tags\":[\"关注\",\"收藏\",\"分享\"]}\n"
    "要求：只用素材中的事实，不杜撰；公司/产品/模型等英文专有名词保留英文；"
    "卡片是用来看的，数字可用阿拉伯数字；语言精炼、有网感。"
)


def _extract_json(text: str) -> dict:
    import json
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"未从模型输出解析出 JSON：{text[:200]}")
    return json.loads(m.group(0))


def split_segments(script: str) -> list[str]:
    """把播报正文按空行切成段落（用于卡点：一段 ↔ 一张卡 ↔ 一段音频）。"""
    return [p.strip() for p in re.split(r"\n\s*\n", script.strip()) if p.strip()]


def _llm_json(prompt_or_msgs, *, backend: str, model: str | None) -> str:
    """统一调用：backend='pi' 走 pi agent，否则走 OpenAI 兼容。返回原始文本。"""
    if backend == "pi":
        proc = subprocess.run(_pi_command() + ["-p", prompt_or_msgs],
                              cwd=str(PI_WORKSPACE), capture_output=True,
                              text=True, encoding="utf-8")
        if proc.returncode != 0:
            raise SystemExit(f"pi 调用失败：{proc.stderr[-600:]}")
        return (proc.stdout or "").strip()
    from openai import OpenAI
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    model = model or os.getenv("LLM_MODEL")
    if not (api_key and model):
        raise SystemExit("未设置 LLM_API_KEY / LLM_MODEL")
    client = OpenAI(base_url=os.getenv("LLM_BASE_URL"), api_key=api_key)
    r = client.chat.completions.create(
        model=model, temperature=0.5,
        messages=[{"role": "system", "content": CARDS_SYSTEM},
                  {"role": "user", "content": prompt_or_msgs}])
    return r.choices[0].message.content.strip()


CARDS_SYNCED_INSTRUCTION = (
    "下面是一篇 AI 播报稿，已按播读顺序切成若干段落（编号从 1 开始）。"
    "请为【每一段】生成恰好一张竖屏卡片，输出 JSON：{\"cards\":[...]}，"
    "卡片数量必须与段落数量完全相同、顺序一致。\n"
    "- 第 1 段（开场白）→ cover：{\"kind\":\"cover\",\"badge\":\"建议收藏 · 每日AI速览\","
    "\"subtitle\":\"如 6月X日 · AI Briefcast\",\"count\":中间内容卡的数量(整数),"
    "\"toc\":[\"逐条列出每张中间卡的一句话标题，≤14字\"]}\n"
    "- 最后一段（收尾）→ cta：{\"kind\":\"cta\",\"title\":\"如 明天见\",\"subtitle\":\"一句话\",\"tags\":[\"关注\",\"收藏\",\"分享\"]}\n"
    "- 中间每段 → point：{\"kind\":\"point\",\"tag\":\"如 头条 01 · 行业 / 论文 · 全模态\","
    "\"icon\":\"一个贴切的 emoji，如 📱📈🛡️🧪🤖⚡\",\"title\":\"≤10字\","
    "\"body\":\"≤55字，口语化，用 **加粗** 标出 1–2 个关键数字/词\","
    "\"punch\":\"≤16字的金句/一句话观点，可用 **加粗** 强调，放在卡片底部\"}\n"
    "要求：每张卡只浓缩它对应那一段的内容，不要跨段；cover 的 toc 要与中间各卡标题对应；"
    "只用稿中事实不杜撰；公司/产品/模型等英文专有名词保留英文；数字可用阿拉伯数字；语言精炼有网感。"
)


def make_cards_synced(segments: list[str], *, backend: str = "api",
                      model: str | None = None) -> list[dict]:
    """按段落一一对应生成卡片（数量 == 段落数），用于精确卡点。"""
    numbered = "\n\n".join(f"【第{i+1}段】{s}" for i, s in enumerate(segments))
    user = f"{CARDS_SYNCED_INSTRUCTION}\n\n以下是分段后的播报稿：\n\n{numbered}"
    prompt = f"{CARDS_SYSTEM}\n\n{user}" if backend == "pi" else user
    out = _llm_json(prompt, backend=backend, model=model)
    cards = _extract_json(out).get("cards", [])
    if len(cards) != len(segments):
        raise SystemExit(
            f"make_cards_synced: 卡片数({len(cards)}) != 段落数({len(segments)})")
    return cards


def make_cards(source_text: str, *, backend: str = "api", model: str | None = None) -> list[dict]:
    """用 LLM 把当天素材转成小红书卡片内容列表。"""
    user = f"{CARDS_INSTRUCTION}\n\n以下是今天的原始新闻素材：\n\n{source_text}"
    if backend == "pi":
        prompt = f"{CARDS_SYSTEM}\n\n{user}"
        proc = subprocess.run(_pi_command() + ["-p", prompt],
                              cwd=str(PI_WORKSPACE), capture_output=True,
                              text=True, encoding="utf-8")
        if proc.returncode != 0:
            raise SystemExit(f"pi 调用失败：{proc.stderr[-600:]}")
        out = (proc.stdout or "").strip()
    else:
        try:
            from openai import OpenAI
        except ImportError as e:
            raise SystemExit("缺少依赖 openai") from e
        api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        model = model or os.getenv("LLM_MODEL")
        if not (api_key and model):
            raise SystemExit("未设置 LLM_API_KEY / LLM_MODEL")
        client = OpenAI(base_url=os.getenv("LLM_BASE_URL"), api_key=api_key)
        r = client.chat.completions.create(
            model=model, temperature=0.5,
            messages=[{"role": "system", "content": CARDS_SYSTEM},
                      {"role": "user", "content": user}])
        out = r.choices[0].message.content.strip()
    cards = _extract_json(out).get("cards", [])
    if not cards:
        raise SystemExit("make_cards: 模型没有返回 cards")
    return cards


def wrap_header(kind: str, date: str, rewriter: str) -> str:
    return (
        f"# AI Briefcast 播报稿（{kind}）· {date}\n\n"
        f"> 抓取：Python + BeautifulSoup；改写：{rewriter}。\n"
        f"> 来源：AI 资讯速览 <{DIGEST_HOME}>，AI 论文简报 <{BRIEF_HOME}>。\n"
        f"> 文稿为 TTS 输入草稿，建议合成前人工快速校对。\n\n---\n\n"
    )


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="抓取每日 AI 新闻并用 LLM 生成播报稿")
    ap.add_argument("--date", help="指定日期 YYYY-MM-DD（默认取最新一期）")
    ap.add_argument("--outdir", default="samples", help="输出目录（默认 samples）")
    ap.add_argument("--modes", default="concise,full",
                    help="要生成的版本，逗号分隔：concise,full（默认两者）")
    ap.add_argument("--llm", choices=["pi", "api"], default="api",
                    help="改写后端：pi（pi agent + DeepSeek）或 api（OpenAI 兼容直连）")
    ap.add_argument("--model", help="覆盖 LLM_MODEL（仅 --llm api 生效）")
    ap.add_argument("--dump-raw", action="store_true",
                    help="只抓取+解析，输出原始素材（不调用 LLM）")
    args = ap.parse_args()

    digest_url = latest_article_url(DIGEST_HOME, "digest", args.date)
    brief_url = latest_article_url(BRIEF_HOME, "daily", args.date)
    print(f"[fetch] digest: {digest_url}")
    print(f"[fetch] brief : {brief_url}")

    digest = parse_digest(digest_url)
    brief = parse_brief(brief_url)
    print(f"[parse] digest: {len(digest.stories)} 篇主新闻, {len(digest.quick_news)} 条快讯")
    print(f"[parse] brief : {len(brief.papers)} 篇重点论文, {len(brief.notable)} 篇延伸阅读")

    date = digest.date if digest.date != "unknown" else brief.date
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    source_text = build_source_text(digest, brief)

    if args.dump_raw:
        raw_path = outdir / f"source-{date}.md"
        raw_path.write_text(source_text + "\n", encoding="utf-8")
        print(f"[write] {raw_path}  ({len(source_text)} chars) —— 原始素材")
        return 0

    model = args.model or os.getenv("LLM_MODEL")
    rewriter = ("pi agent + DeepSeek" if args.llm == "pi"
                else f"LLM（OpenAI 兼容{('，模型 ' + model) if model else ''}）")
    modes = [m.strip() for m in args.modes.split(",") if m.strip()]
    for mode in modes:
        if mode not in ("concise", "full"):
            print(f"[skip] 未知版本：{mode}")
            continue
        print(f"[llm ] 生成{mode}版（{args.llm}）…")
        script = rewrite(source_text, mode, backend=args.llm, model=model)
        script = fixed_intro(date) + "\n\n" + script.lstrip()
        kind = "简洁版" if mode == "concise" else "完整版"
        content = wrap_header(kind, date, rewriter) + script + "\n"
        path = outdir / f"broadcast-{date}-{mode}.md"
        path.write_text(content, encoding="utf-8")
        print(f"[write] {path}  ({len(content)} chars)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

# AI Briefcast — Claude 记忆合集（跨机同步用）

> 从 Windows 机器 `~\.claude\projects\E--Github-project-ai-briefcast\memory\` 导出，2026-07-25。
> 供 Mac 上的 Claude 阅读；路径类信息（盘符、exe 路径）为 Windows 本机专属，Mac 上需换算。

## 索引

- [写稿必须正式跑 ai-news-podcast](#写稿必须正式跑-ai-news-podcast) — 用户否过"只参照纪律"的稿子
- [7月稿件/封面新偏好](#7月稿件封面新偏好) — 不念限制句、说 token、封面钩子查重、比喻不许绕、一碗水端平
- [视频默认带字幕](#视频默认带字幕) — 6/17 起每条默认烧字幕
- [小红书投稿自动化](#小红书投稿自动化) — Route B（Chrome 驱动），发布需逐条确认
- [codex 生图](#codex-生图) — codex CLI `exec` 调 imagegen 生图（Windows 专属）

---

## 写稿必须正式跑 ai-news-podcast

`type: feedback`

写 briefcast 播报稿（步骤 1b）时，用户要求**正式调用 ai-news-podcast skill**（读全 4 份 references、建事实卡、E1-E5 分级、按 quality-checklist 验收），而不是凭记忆"按它的纪律写"。

**Why:** 2026-07-09 期用户否掉了未走完整流程的初稿（"很蠢"），点名"一定要用我的 AI News Podcast skill"。完整流程当场抓出一处真实错误（把"服务商拿开源权重提供低价服务"写成"个人在家免费自建"，GLM 5.2 是 744B 个人跑不动）和漏报的预印本披露。

**How to apply:** 每期写稿前 Skill 调用（或已加载时逐份读 references 走流程）；重点＝数字归因到估算人、E2 预印本必须口播点明、比喻不得压过事实；语言仍按 ai-briefcast-daily 的★文风铁律收口。另：用户口播稿时长敏感度不高（126s 也接受），但内容错误零容忍。

---

## 7月稿件/封面新偏好

`type: feedback`（2026-07-13 至 07-18 沉淀）

1. **稿中不念"预印本，还没同行评审"和"作者承认全在仿真、真机没验证"这类限制句**（7/13 用户点名删）。限制仍写进 MD header 备注留档；例外＝公司自述型爆点（如 GPT-5.6 证明猜想），"未同行评审"要保留在正文。真正过了评审的（如 ECCV 接收）可以正着写"过了同行评审"当卖点。
2. **说 "token" 不说 "字块/字"**（7/14 用户纠正）。
3. **封面 hook 用前先查历史期数**：同一对主角的冲突连续剧（如 Musk vs Altman，6/11 已当过头条）不连着当封面 hook；新闻本身可保留，hook 换当期其他大牌条目（7/15 用户要求）。
4. **比喻别绕**：IdeaGene"科研想法有家谱"被用户看不懂打回，重写成"考它说清沿用谁的方法、修补哪个缺陷"。写完自查：比喻若需要再解释一层，直接改成平铺直叙。
5. 跑分类表述：对手已换代时别写错代际（"Opus 已不是旗舰"），互有胜负用"几项测试上赢了"兜边界，不写"全面赶超"也不啰嗦对冲。
6. **归因一次就够，禁止追加怀疑句**（2026-07-17 用户点名，永久）：写了"官方说/官方自家跑分"就够了，**永远不要再补"要提醒的是跑分都是自家测的、还没人独立复现、权重还没放"**；卡片不做"为什么说还没人复现"这类专门证伪卡，金句不写"要等复现"。
7. **论文段不写"还得翻全文/要看全文"提醒句**（2026-07-18 用户点名"很废话"删掉）：摘要缺数字这类限制记进 MD header 留档即可，正文只讲论文做了什么；限制类补充句一律不上稿。
8. **怀疑要一碗水端平**（2026-07-17 用户当场抓出偏见，已核实属实）：同为 E1 厂商自评，国产模型（Kimi/GLM/Qwen）和 Claude/GPT/Gemini 必须同一套措辞。事故记录：7/17 给 Kimi K3 加了整张「为什么说还没人复现」卡+提醒句+"第三名要等复现"金句；而 7/13 给 Fable 5 写的是「连 Musk 都公开夸它市面最好」吹捧卡，7/11 对 GPT-5.6 自测的"省一半字"零怀疑。自查法：把公司名换成 Anthropic/OpenAI 再读，不会对它们这么写就删掉。补充卡也不许转述名人吹捧当软文。

**How to apply**：写稿 checklist 里过一遍以上各条；封面 hook 定稿前 grep output/ 查主角是否近期当过头条；交稿前做"换公司名"自查。证据分级只管归因，不等于加怀疑层。

---

## 视频默认带字幕

`type: feedback`

用户要求 briefcast 竖屏视频**默认带烧录字幕**（从 2026-06-17 起）。

**Why:** 便于无声观看/完播；之前几期没字幕，用户明确要求"以后每条默认带字幕"。

**How to apply:** 用 `make_xhs_video_html.add_subtitles(segments, durs, audio, video_in, video_out)`：
- 取**脚本原文**（`gb.split_segments(rd.strip_header(md))`，与卡点同一份 segments），不用 ASR 文本——避免 Nex/Qwen/CODA-BENCH/AVA-VLA 等专有名词被转错。
- 时间轴：`faster-whisper(base)` 词级时间戳 → 按有声字比例映射到字幕行；whisper 不可用自动回退 `durs` 按段比例。
- 样式：ASS、微软雅黑 82、半透明黑底(BorderStyle=3)、底部居中、**MarginV=820**（约 78% 高度，落在正文与金句之间的空白带——MarginV=300 贴底会压住内容卡金句，用户已否决）。
- ffmpeg 烧录用 **cwd 下相对路径**（`ass=_burn_xxx.ass`）避开 Windows 盘符冒号转义。
- 在**片尾 concat 出基底视频之后**再烧字幕；发布用 `video/xhs-<date>-spacex-sub.mp4`，字幕源留 `video/subs.ass`。

---

## 小红书投稿自动化

`type: project`（2026-06-13 敲定，06-19 落地）

**实现状态：** `scripts/make_publish.py` 生成 `output/<date>/publish.json`；ai-briefcast-daily skill 已加「第 8 步：投稿」。投稿动作本身是半自动（Claude-in-Chrome 填表 + 用户点发布）。

**走 Route B：用 Claude-in-Chrome 驱动 `creator.xiaohongshu.com` 网页上传表单**，不用 xiaohongshu-mcp。

**Why：** 社区最佳 MCP `xpzouying/xiaohongshu-mcp` 的 `publish_with_video` 没有封面参数，自动发会丢掉流水线专门做的 3:4 设计封面。小红书无官方 MCP/API。只有浏览器自动化能传自定义封面。

**⚠️ 上传只能半自动（2026-06-20 实测，两条全自动路都堵死）：**
- 插件 `file_upload`：沙箱只认分享给会话的文件，且单次上限 10MB（视频 ~18MB 超限）。不行。
- computer-use 操作系统文件框：那是 Chrome 进程弹的对话框，computer-use 对浏览器一律"只读"档 → 打不进路径。不行。
- 结论：**选视频、选封面这两下只能用户手动点**；其余（自定义封面套用、标题、正文、标签、可见性、停在发布键）全自动。别再尝试全自动上传那两步。

**How to apply：**
- 先 `python scripts/make_publish.py --date <date>`（默认 `--visibility self`＝仅自己可见；可 `--visibility public` / `--schedule "YYYY-MM-DD HH:MM"`）出 publish.json。**标题 >20 字会告警**，投稿前精简到 ≤20。
- 投稿＝skill 第 8 步：导航 `creator.xiaohongshu.com/publish/publish` → 传 video → **自定义封面传 cover**（别用自动截帧）→ 填 title/content → 设可见性 → **停在发布键前等用户点**。
- 账号姿态：**主号**（@柿子树下的猫wanjeans），**首条用「仅自己可见」或定时**；低频（一天最多 1 条）、人工过内容。
- **发布动作必须每次让用户逐条确认**，不得自动点「发布」。
- 前置：Claude-in-Chrome 扩展已连接 + 该 Chrome 已登录创作者后台。

---

## codex 生图

`type: reference`（Windows 本机专属；Mac 上路径需另查）

已沉淀为项目 skill：`.claude/skills/codex-imagegen/SKILL.md`（2026-07-22 验证通过，含比例控制），生图需求直接走该 skill。原始笔记：

用户已登录 ChatGPT 的 codex 有内置 `imagegen` 技能，可命令行生图：

```
& 'C:\Users\WANG-\AppData\Local\OpenAI\Codex\bin\5dee10576ec7a5b8\codex.exe' exec --cd <输出目录> --sandbox workspace-write --skip-git-repo-check "生成一张图：<描述>，保存为 xxx.png"
```

坑：
- npm 版已于 2026-07-22 升级到 0.145.0，直接用 `codex` 命令即可；若又报 "requires a newer version"，先 `npm i -g @openai/codex@latest`，不行再用桌面版 exe。
- config.toml 里 `service_tier = "default"` 会让旧 CLI 解析失败，已删。
- 必须 `--skip-git-repo-check`，否则非 trusted 目录直接退出。

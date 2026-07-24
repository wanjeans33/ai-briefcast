---
name: codex-imagegen
description: >
  用本机 codex CLI（已登录 ChatGPT 账号）的内置 imagegen 技能生成 AI 图片（照片、插画、卡通、
  封面素材、贴图等位图）。只要用户说"用 codex 生图 / 让 GPT 画一张图 / 用 ChatGPT 生成图片"，
  或需要 AI 生成位图而明确点名 codex/GPT 时，就用本技能。不要用于:豆包/其他生图服务、
  SVG/代码绘图、ChatCut 项目内的 image-gen(那走 chatcut:image-gen)。
---

# 用 codex CLI 生图

本机 codex 登录了 ChatGPT 账号,自带 `imagegen` 技能(GPT 生图模型)。通过 `codex exec` 一条命令驱动,不需要 API key、不需要 plugin。

## 找到可用的 codex

直接用 `codex` 命令(npm 版,2026-07-22 已升到 0.145.0)。如果它报模型不支持("requires a newer version of Codex"),说明 npm 版又落后了——先试 `npm install -g @openai/codex@latest`,不行再回退到桌面版自带的 exe(随桌面 App 自动更新):

```powershell
$codex = Get-ChildItem 'C:\Users\WANG-\AppData\Local\OpenAI\Codex\bin' -Recurse -Filter codex.exe |
  Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object FullName
```

若想确认登录状态:`codex login status` 应输出 "Logged in using ChatGPT"。

## 生图命令

```powershell
& $codex exec --cd <输出目录> --sandbox workspace-write --skip-git-repo-check "<提示词>"
```

- `--cd`:图片落盘目录。临时图用 scratchpad,项目产物直接指向目标目录(如 output/日期/)。
- `--skip-git-repo-check`:必须带,否则非 trusted 目录直接退出。
- 耗时约 1-3 分钟,timeout 给 300000 以上。

提示词模板(三个要素都要有:画什么、文件名、禁止代码画图兜底):

```
请用你的图片生成能力生成一张图:<内容描述,含风格/比例,如"3:4 竖版""横版 16:9">。
把图片保存到当前目录,文件名 <name>.png。
如果你没有图片生成工具,直接明确说"无图片生成工具",不要用代码画图代替。
```

最后一句是防守:不写的话 codex 可能在工具不可用时用 matplotlib/SVG 画个替代品糊弄过去。

## 质量:CLI 出图不如桌面版?

引擎相同(同模型、同内置 image_gen),差在用法。CLI 一次性调用时要主动补齐桌面版对话里自带的三样东西:

1. **提示词写成结构化规格**,别只给一句话。至少覆盖:场景/主体/风格媒介/构图框架/光线氛围/色板/禁止项(无水印、无多余文字等)。用户给的描述瘦,就替他扩写(加构图和打磨程度提示,不加没暗示过的元素)。
2. **明确分辨率**。不写默认偏小(1024~1600 级)。成品图直接在提示里要:4K 横版 3840x2160、4K 竖版 2160x3840、2K 方图 2048x2048;草稿才用默认。
3. **要求它自检迭代一轮**。在提示里加一句:"生成后自己检查主体、构图、文字是否符合要求,不满意就改一处重生成,把最好的一张存为最终文件。"桌面版好图多是第二三轮的产物。

## 生成后

1. `Get-ChildItem <输出目录>` 确认文件存在且体积正常(正常一两 MB 级;几 KB 的很可能是代码画的兜底图)。
2. 用 Read 工具看一眼图片内容是否符合描述,再交付。

## 已知坑

- 内置生图工具分辨率有上限(实测长边 ~1500px,提示词里要 2048/4K 也不给)。要真高分辨率:超分后处理,或走 imagegen 的 CLI fallback(需 OPENAI_API_KEY)。
- codex 沙箱可能在"复制成品到输出目录"一步报拒绝访问(CreateProcessAsUserW error 5),但图已经生成——去 `C:\Users\WANG-\.codex\generated_images\<session-id>\` 里直接取(session id 在 exec 输出头部)。
- 多行提示词别当命令行参数传(收不到),用管道:`$prompt | & $codex exec ... -`(结尾加 `-` 表示读 stdin)。

- config.toml 里若有 `service_tier = "default"` 会让旧 CLI 解析失败(只认 fast/flex),删掉即可——它就是默认值,不影响桌面版。
- 改图/参考图:codex exec 支持 `-i <文件>` 附图,可用于"照这张改"类需求。

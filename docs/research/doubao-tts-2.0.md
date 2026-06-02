# 豆包语音合成大模型 2.0（Doubao-Seed-TTS 2.0）调研

> 调研日期：2026-06-02 · 分支：`research/doubao-tts-2.0`
> 目的：评估在 **ai-briefcast** 中用豆包 TTS 2.0 生成播报音频（替代 / 增强当前 `audio_output` 链路）。

## 1. 概览

火山引擎（字节跳动）于 2025 年 10 月发布**语音合成大模型 2.0（Doubao-Seed-TTS 2.0）**与**声音复刻大模型 2.0（Doubao-Seed-ICL 2.0）**。
核心定位：从 1.0 的「把字念对」升级到 2.0 的「**理解语义 + 演绎情感**」——基于豆包大模型架构，具备上下文理解与推理能力。

### 1.0 → 2.0 主要变化
| 能力 | 1.0 | 2.0 |
|------|-----|-----|
| 文本理解 | 逐字朗读 | 多轮对话上下文理解，自动判断语气/停顿/情感 |
| 情感控制 | 预设 style 枚举 | **指令式（自然语言）情感与风格控制**（语速、音高、风格可用自然语言描述微调） |
| 公式/学科符号 | 弱 | 全学科复杂公式平均准确率 **~90%**（教育场景专项优化） |
| 声音复刻 | ICL 1.0 | ICL 2.0，**5 秒样本**即可秒级复刻，相似度极高，支持情感演绎与多角色 |
| 多语种 | 中英为主 | 中英高准确率 + 日/西/葡等多语种（复刻 2.0 当前仅中/英） |

## 2. API 接入要点

> 官方文档入口：<https://www.volcengine.com/docs/6561/1096680>（豆包语音 API 总览）

### 2.1 合成端点（大模型 TTS）
| 模式 | 协议 | 端点 |
|------|------|------|
| 双向流式（推荐，低延迟） | WebSocket | `wss://openspeech.bytedance.com/api/v3/tts/bidirectional` |
| 单向流式 | HTTP Chunked | `https://openspeech.bytedance.com/api/v3/tts/unidirectional` |
| 非流式 HTTP V1 | HTTP | 见 docs/6561/1257584 |
| 异步长文本（≤10 万字） | HTTP 提交+查询 | `/api/v1/tts_async/submit` + `/query` |

### 2.2 鉴权与关键 Header
```
Authorization: Bearer;${AccessToken}
X-Api-Resource-Id: <见下表>
```
请求体内需带 `appid`。

| 场景 | X-Api-Resource-Id |
|------|-------------------|
| 豆包 TTS 2.0（预置音色） | `seed-tts-2.0` |
| 声音复刻 2.0（复刻音色，speaker 以 `S_` 开头） | `seed-icl-2.0` |
| 复刻 1.0（字符版/并发版） | `seed-icl-1.0` / `seed-icl-1.0-concurr` |

### 2.3 声音复刻训练流程（ICL 2.0）
1. 上传样本音频：`POST https://openspeech.bytedance.com/api/v1/mega_tts/audio/upload`
   - 格式：wav / mp3 / ogg / m4a / aac / pcm，≤10MB，base64 编码，需指定语种（2.0 限中/英）
   - `model_type=4` → ICL V2 效果（`model_type=5` 为 V3，2026.10.16 起）
2. 轮询训练状态：返回 Training / Success / Failed + demo 音频 URL
3. 用返回的 speaker id（`S_xxx`）调合成端点，`X-Api-Resource-Id: seed-icl-2.0`

### 2.4 常用合成参数（非流式/异步接口字段，可参考）
- `text`（≤10 万字，支持 SSML）、`voice_type`/`speaker`、`format`（pcm/wav/mp3/ogg_opus）
- `sample_rate`（默认 24000）、`speed` 0.2–3、`volume` 0.1–3、`pitch` 0.1–3
- `style`（情感）、`enable_subtitle`（时间戳/字幕，0–3 级）
- 2.0 的情感/风格主推**自然语言指令**控制

## 3. 计费
- 企业路线：约 **150 元/音色/年**（声音复刻）
- 新用户有免费额度，字符包起步 **10 万字符**
- 合成按字符计费（具体以控制台为准）

## 4. 对 ai-briefcast 的适配建议
本项目是「AI 播报」生成器，输出落在 `audio_output/`。TTS 2.0 适配点：
1. **播报口播**：用 `seed-tts-2.0` 预置音色 + 自然语言指令（如「用沉稳的新闻主播语气」）生成简报旁白。
2. **多角色/对话播客**：用指令式情感控制做不同角色音色与情绪切换。
3. **品牌音色**：用 ICL 2.0 复刻固定主播音色（5 秒样本），保证多期一致性。
4. **长文本**：单篇简报较长时走异步长文本接口（≤10 万字），短段落实时播放走双向流式。
5. **字幕对齐**：开 `enable_subtitle` 拿时间戳，便于做带字幕的视频版播报。

### 待验证（下一步）
- [ ] 申请火山引擎 appid + AccessToken，跑通 `seed-tts-2.0` 双向流式最小 demo
- [ ] 确认 2.0 预置音色清单与对应 `voice_type` 取值
- [ ] 实测情感指令对播报语气的可控程度与延迟
- [ ] 对比当前 `audio_output` 链路的成本/音质

## 来源
- [火山引擎发布豆包语音模型2.0（品玩）](https://www.pingwest.com/w/308310)
- [豆包语音2.0 模型介绍（AI工具集）](https://ai-bot.cn/doubao-seed-tts-2-0/)
- [豆包语音 API 接口文档总览（火山引擎）](https://www.volcengine.com/docs/6561/1096680)
- [声音复刻 API 文档（火山引擎）](https://www.volcengine.com/docs/6561/1305191)
- [大模型 HTTP 非流式接口 V1（火山引擎）](https://www.volcengine.com/docs/6561/1257584)
- [异步长文本接口文档（火山引擎）](https://www.volcengine.com/docs/6561/1829010)
- [IT之家：豆包发布语音合成/声音复刻等大模型](https://www.ithome.com/0/889/888.htm)

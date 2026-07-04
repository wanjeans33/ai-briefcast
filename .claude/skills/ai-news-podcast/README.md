# AI 新闻播客 Claude Code Skill

## 安装

### 项目级
把 `ai-news-podcast` 整个目录复制到项目的 `.claude/skills/` 下。

最终路径：
```text
你的项目/
└── .claude/
    └── skills/
        └── ai-news-podcast/
            ├── SKILL.md
            ├── references/
            ├── examples/
            └── evals/
```

### 个人级
把 `ai-news-podcast` 目录复制到：
```text
~/.claude/skills/ai-news-podcast/
```

## 使用

在 Claude Code 中手动调用：
```text
/ai-news-podcast
```

也可以直接描述任务，例如：
```text
请把这周的 4 条 AI 新闻和 2 篇论文整理成 8 分钟中文播客稿。
听众是产品经理。每条都要说明来源等级和限制。
```

## 推荐输入模板

```markdown
## 任务类型
周报 / 论文快报 / 改写 / 单条新闻

## 资料
- 链接、文件路径或粘贴内容

## 目标听众
普通科技听众 / 开发者 / 产品经理 / 投资人 / 学术听众

## 目标时长
5 分钟

## 风格强度
70

## 输出要求
- 需要时间戳
- 需要资料说明
- 预印本必须显著提示
```

## 设计说明

这个 Skill 把三件事分开：
1. 事实与证据
2. 技术解释
3. 主持人口吻

先生成准确的基础稿，再应用口播风格，最后质检。这样能降低“为了像某种文风而改坏事实”的风险。

## 可选 Output Style

项目根目录 `.claude/output-styles/podcast-anchor.md` 是可选主持人口吻文件（已随本次调整放到该位置）。不同 Claude Code 版本对 Output Style 的加载方式可能变化，请以本机 `/output-style` 帮助和官方文档为准。Skill 本身不依赖它，也可以单独工作。

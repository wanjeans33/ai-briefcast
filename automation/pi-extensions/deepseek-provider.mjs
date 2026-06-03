// pi 自定义 provider：DeepSeek（OpenAI 兼容接口）
// 安装：复制到 ~/.pi/extensions/ （或运行 scripts/setup_pi.ps1）
// 依赖环境变量 DEEPSEEK_API_KEY。
// 文档：https://pi.dev/docs/latest/custom-provider

/** @param {import("@earendil-works/pi-coding-agent").ExtensionAPI} pi */
export default function (pi) {
  pi.registerProvider("deepseek", {
    baseUrl: "https://api.deepseek.com",
    apiKey: "$DEEPSEEK_API_KEY",
    api: "openai-completions",
    models: [
      {
        id: "deepseek-chat",
        name: "DeepSeek Chat",
        reasoning: false,
        input: ["text"],
        cost: { input: 0.14, output: 0.28, cacheRead: 0, cacheWrite: 0 },
        contextWindow: 128000,
        maxTokens: 8192,
      },
      {
        id: "deepseek-reasoner",
        name: "DeepSeek Reasoner",
        reasoning: true,
        input: ["text"],
        cost: { input: 0.55, output: 2.19, cacheRead: 0, cacheWrite: 0 },
        contextWindow: 128000,
        maxTokens: 8192,
      },
    ],
  });
}

# 一次性安装 pi（https://pi.dev）并注册 DeepSeek provider 扩展。
# 用法：  powershell -ExecutionPolicy Bypass -File scripts\setup_pi.ps1

$ErrorActionPreference = "Stop"
$repo = Split-Path $PSScriptRoot -Parent

Write-Host "==> 安装 pi coding agent (npm -g) ..."
npm install -g "@earendil-works/pi-coding-agent"

$extDir = Join-Path $env:USERPROFILE ".pi\extensions"
New-Item -ItemType Directory -Force -Path $extDir | Out-Null
$src = Join-Path $repo "automation\pi-extensions\deepseek-provider.mjs"
Copy-Item $src $extDir -Force
Write-Host "==> 已安装 DeepSeek provider 扩展到 $extDir"

if (-not $env:DEEPSEEK_API_KEY) {
    $dotenv = Join-Path $repo ".env"
    $hasKey = (Test-Path $dotenv) -and (Select-String -Path $dotenv -Pattern "^DEEPSEEK_API_KEY=" -Quiet)
    if (-not $hasKey) {
        Write-Warning "未检测到 DEEPSEEK_API_KEY。请在 $repo\.env 里填入 DEEPSEEK_API_KEY=sk-...（参考 .env.example）。"
    }
}

Write-Host "==> 验证：" (Get-Command pi -ErrorAction SilentlyContinue).Source
Write-Host "完成。可运行：python scripts\run_daily.py --dry-run 检查流程。"

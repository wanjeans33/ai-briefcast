# 注册 Windows 计划任务：每天定时跑完整 AI Briefcast 流程。
# 用法：
#   powershell -ExecutionPolicy Bypass -File scripts\register_daily_task.ps1 -Time 08:00
#   powershell -ExecutionPolicy Bypass -File scripts\register_daily_task.ps1 -Remove
param(
    [string]$Time = "08:00",
    [string]$TaskName = "AI-Briefcast-Daily",
    [switch]$Remove
)

$ErrorActionPreference = "Stop"
$repo = Split-Path $PSScriptRoot -Parent

if ($Remove) {
    schtasks /delete /tn $TaskName /f
    Write-Host "已删除计划任务 $TaskName"
    return
}

$wrapper = Join-Path $repo "scripts\run_daily.cmd"
$tr = "`"$wrapper`""

Write-Host "注册计划任务：$TaskName  每天 $Time"
Write-Host "  执行：$tr"
schtasks /create /tn $TaskName /sc DAILY /st $Time /tr $tr /f /rl LIMITED

Write-Host ""
Write-Host "已注册。手动触发一次测试： schtasks /run /tn $TaskName"
Write-Host "查看： schtasks /query /tn $TaskName /v /fo LIST"
Write-Host "删除： powershell -File scripts\register_daily_task.ps1 -Remove"

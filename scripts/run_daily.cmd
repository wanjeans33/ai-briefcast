@echo off
rem AI Briefcast 每日流程的计划任务入口（被 register_daily_task.ps1 调用）。
rem 切到仓库根，跑 run_daily.py，输出追加到 logs\task.log。
rem 默认只做 concise（可被传入参数覆盖，如 --modes full）。
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "REPO=%~dp0.."
cd /d "%REPO%"
if not exist "logs" mkdir "logs"
python "%REPO%\scripts\run_daily.py" --modes concise --video %* >> "%REPO%\logs\task.log" 2>&1

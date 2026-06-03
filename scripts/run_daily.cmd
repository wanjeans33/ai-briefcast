@echo off
rem AI Briefcast 每日流程的计划任务入口（被 register_daily_task.ps1 调用）。
rem 切到仓库根，跑 run_daily.py，输出追加到 logs\task.log。
setlocal
set "REPO=%~dp0.."
cd /d "%REPO%"
if not exist "logs" mkdir "logs"
python "%REPO%\scripts\run_daily.py" %* >> "%REPO%\logs\task.log" 2>&1

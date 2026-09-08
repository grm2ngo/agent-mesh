@echo off
rem mesh-init.cmd <target-project-dir> — install agent-mesh starter set
rem (kept deliberately simple: separate plain calls, no if/else+& chains)
setlocal
set TARGET=%~1

if "%TARGET%"=="" (
  echo usage: mesh-init.cmd ^<path-to-your-project^>
  exit /b 1
)

if not exist "%TARGET%" mkdir "%TARGET%"

copy /y "%~dp0..\templates\AGENTS.md" "%TARGET%\AGENTS.md"
copy /y "%~dp0..\templates\STATE.md" "%TARGET%\STATE.md"
copy /y "%~dp0..\templates\AGENT_FRICTION.md" "%TARGET%\AGENT_FRICTION.md"
copy /y "%~dp0..\templates\AGENT_VERDICTS.md" "%TARGET%\AGENT_VERDICTS.md"
copy /y "%~dp0..\templates\VARIABLES.md" "%TARGET%\VARIABLES.md"
copy /y "%~dp0..\templates\SENTINEL.md" "%TARGET%\SENTINEL.md"

if not exist "%TARGET%\tools" mkdir "%TARGET%\tools"
copy /y "%~dp0..\tools\run_task.cmd" "%TARGET%\tools\"
copy /y "%~dp0..\tools\_run_task.py" "%TARGET%\tools\"
copy /y "%~dp0..\tools\spin_watch.py" "%TARGET%\tools\"
copy /y "%~dp0..\tools\check_tiers.py" "%TARGET%\tools\"
copy /y "%~dp0..\tools\fix_mojibake.py" "%TARGET%\tools\"
copy /y "%~dp0..\tools\token_report.py" "%TARGET%\tools\"

copy /y "%~dp0..\PLAYBOOK.md" "%TARGET%\DISPATCH.md"

echo.
echo agent-mesh installed into %TARGET%
echo NEXT:
echo  1. Edit %TARGET%\AGENTS.md  (project name + project law)
echo  2. Copy agents\*.md into your harness agent-definitions folder
echo  3. Read DISPATCH.md and dispatch your first task
endlocal

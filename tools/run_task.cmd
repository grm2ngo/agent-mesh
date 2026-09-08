@echo off
rem tmp\architect\run_task.cmd - PROTOTYPE front for P-001 (architect 2026-09-08).
rem agent-mesh task runner (PROTOCOL section 10 rule 1)
rem Usage: run_task NAME [ENV=VAL ...] -- command [args...]
rem Options via env: RUN_TASK_LOGDIR / RUN_TASK_KILL_AFTER / RUN_TASK_TAIL / RUN_TASK_BENIGN_RE
python -X utf8 "%~dp0_run_task.py" %*
exit /b %errorlevel%

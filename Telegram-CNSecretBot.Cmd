@Echo off
SetLocal EnableDelayedExpansion
Title %~n0
CD /D "%~dp0"

Python secret.py
Set ExitCode=!ErrorLevel!
Echo.
If Not "!ExitCode!"=="0" (
    Echo ExitCode: !ExitCode!  1>&2
)
Pause
Exit !ExitCode!
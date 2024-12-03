@Echo Off
Title Reg Converter v1.2 & Color 1A
cd %systemroot%\system32

cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && REG QUERY "HKU\S-1-5-19" 1>nul 2>nul || (  cmd /u /c echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && ""%~s0"" %Apply%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

call :IsAdmin

Reg.exe add "HKCU\SOFTWARE\Classes\*\shell\EasyHash" /v "MUIVerb" /t REG_SZ /d "EasyHash" /f
Reg.exe add "HKCU\SOFTWARE\Classes\*\shell\EasyHash" /v "Subcommands" /t REG_SZ /d "" /f
Reg.exe add "HKCU\SOFTWARE\Classes\*\shell\EasyHash\shell" /f
Exit

:IsAdmin
Reg.exe query "HKU\S-1-5-19\Environment"
If Not %ERRORLEVEL% EQU 0 (
 Cls & Echo You must have administrator rights to continue ... 
 Pause & Exit
)
Cls
goto:eof

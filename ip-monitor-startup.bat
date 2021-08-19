@Reg Add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /V "IP monitor" /T REG_SZ /D "\"%CD%\ip-monitor.exe\"" /F >Nul

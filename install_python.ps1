$ErrorActionPreference = "Stop"
Write-Host "Downloading Python 3.11 for Windows..."
$url = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
$installerPath = "$env:TEMP\python-3.11.8-amd64.exe"
Invoke-WebRequest -Uri $url -OutFile $installerPath

Write-Host "Instaling Python..."
# Chạy cài đặt ngầm ngầm, cài cho mọi user, tự động add vào PATH
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait -NoNewWindow
Write-Host "Python installation complete!"

# Remove installer
Remove-Item $installerPath

# Refreshes environment variables in the current session
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
Write-Host "System PATH updated in current session."

python --version

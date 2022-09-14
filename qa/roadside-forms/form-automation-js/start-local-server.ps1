# PowerShell script to start a local web server using WebServer:
# https://github.com/MScholtes/WebServer
#
# Install with:
# > Install-Module WebServer

# Start server with:
# > Start-Webserver

Write-Output "Access content with local URL:"
Write-Output " - http://localhost:8080/rsf-model.js"
Write-Output ""

Write-Output "Stop server by accessing /quit URI:"
Write-Output " - http://localhost:8080/quit"
Write-Output ""

Start-Webserver
# PowerShell script to run Robot Framework tests
# Start-Transcript run.log

Import-Module ".\lib\RobotSupport.psm1" -Force

# Requirements to run Robot Framework script
Test-Installed robot "Install with 'pip install robotframework'."
Test-Installed oc "Install oc executable and ensure it is on the path."
Test-FilePresent .\lib\keywords.resource "Check it out from git before running."
Test-FilePresent .\lib\kw-requests.resource "Check it out from git before running."
Test-FilePresent .\lib\kw-responses.resource "Check it out from git before running."
Test-FilePresent .\env.py "Copy env.py-template to env.py and configure it."
Test-LoggedInToOpenShift

# Recursively execute all suites with *.robot name
robot --outputdir results --debugfile debug.txt --name "DF VI-IRP API test suite" --variablefile env.py .
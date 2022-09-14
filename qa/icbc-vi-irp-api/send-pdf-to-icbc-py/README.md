# Send 12/24 PDF to ICBC

Jonathan Longe wrote this script as a test tool, so he could verify that the ICBC API in the DEV environment was working.

He sent it to me to use as part of my testing with Brenda. See DF-2153.

Planning to test with Brenda on Monday, 29th August.

Steps to run this script:
 
1. Create venv folder:
   - python -m venv venv
   - .\venv\scripts\Activate.ps1
2. Install packages: 
   - python-dotenv (for environment files)
   - requests (for REST API requests)
   - Faker (to generate test data)
3. Connect to office Ethernet, wifi, or IDIR VPN.
4. Find a suitable PDF file. 
   - Preferably one with a 12- or 24-hour prohibition.
   - Call script with PDF file as a parameter:

         > python .\send_to_ICBC.py --filename .\GAUDRY_J-100039_all.pdf 

5. Example output:
```
response status code: 200
payload: {                  
    "birthdate": "20110819",
    "dlJurisdiction": "BC", 
    "dlNumber": "0377118",  
    "firstName": "Joy",     
    "lastName": "Olson",
    "noticeNumber": "VA320723",
    "nscNumber": "045148",
    "officerDetachment": "VANCOUVER",
    "officerName": "Frederick",
    "officerNumber": "MB28566",
    "pdf": "[BASE64......]",
    "plateJurisdiction": "BC",
    "plateNumber": "QB 0701",
    "pujCode": "",
    "section": "215.2",
    "violationDate": "20220825",
    "violationLocation": "PORT HEATHERPORT",
    "violationTime": "12:08"
}
response: Contravention successfully stored.
```
# =======================================================================================
#      _       _       _       _  __                                _           _       _       _
#   /\| |/\ /\| |/\ /\| |/\   | |/ /                               | |       /\| |/\ /\| |/\ /\| |/\
#   \ ` ' / \ ` ' / \ ` ' /   | ' / ___ _   ___      _____  _ __ __| |___    \ ` ' / \ ` ' / \ ` ' /
#  |_     _|_     _|_     _|  |  < / _ \ | | \ \ /\ / / _ \| '__/ _` / __|  |_     _|_     _|_     _|
#   / , . \ / , . \ / , . \   | . \  __/ |_| |\ V  V / (_) | | | (_| \__ \   / , . \ / , . \ / , . \
#   \/|_|\/ \/|_|\/ \/|_|\/   |_|\_\___|\__, | \_/\_/ \___/|_|  \__,_|___/   \/|_|\/ \/|_|\/ \/|_|\/
#                                        __/ |
#                                       |___/
#
# =======================================================================================
*** Keywords ***

Create DFAPI session
    [Documentation]  Creates suite variables for sessions: ${DFAPI_SESSION} and ${DFAPI_UNAUTHENTICATED_SESSION}.
    ${auth} =    Create List  ${DFAPI_AUTH_USER}  ${DFAPI_AUTH_PASS}
    ${headers}=  Create dictionary  Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8
    Create Session 	session 	${DFAPI_SERVER_HOST}  verify=False
    Set suite variable  ${DFAPI_UNAUTHENTICATED_SESSION}  session
    Create Session      authenticated_session    url=${DFAPI_SERVER_HOST}  auth=${auth}  verify=False  headers=${headers}
    Set suite variable  ${DFAPI_SESSION}  authenticated_session
    ${random1} =  Evaluate  random.randint(90000000, 99999999)
    ${random2} =  Evaluate  random.randint(90000000, 99999999)
    ${random3} =  Evaluate  random.randint(90000000, 99999999)
    ${random4} =  Evaluate  random.randint(90000000, 99999999)
    Set suite variable  ${ADP_PAYMENT_RECEIPT}   ${random1}
    Set suite variable  ${IRP_PAYMENT_RECEIPT}   ${random2}
    Set suite variable  ${UL_PAYMENT_RECEIPT}    ${random3}
    Set suite variable  ${UL_SECOND_PAYMENT_RECEIPT}    ${random4}

Swagger HTML page is available
    [Tags]  Swagger
    ${response} =  Get On Session 	${DFAPI_UNAUTHENTICATED_SESSION} 	/${DFAPI_SERVER_PATH}/swagger-ui.html
    Set test variable  ${test_response}  ${response}

Open API specification is available
    [Tags]  Swagger
    ${response} =  Get On Session 	${DFAPI_UNAUTHENTICATED_SESSION} 	/${DFAPI_SERVER_PATH}/v2/api-docs
    Set test variable  ${test_response}  ${response}

Response content type is
    [Arguments]  ${header_value}
    ${content_type} =  Get from Dictionary  ${test_response.headers}  content-type
    Should Contain  ${content_type}  ${header_value}

Response code is
    [Arguments]  ${response_status_code}
    Should be equal as strings  ${test_response.status_code}  ${response_status_code}

Response code is not
    [Arguments]  ${response_status_code}
    Should not be equal as strings  ${test_response.status_code}  ${response_status_code}

Response body contains
    [Arguments]  ${substring}
    Log  ${substring}
    Should contain  ${test_response.text}  ${substring}

Response body does not contain
    [Arguments]  ${substring}
    Log  ${substring}
    Should not contain  ${test_response.text}  ${substring}

Utility ping with no authentication
    [Tags]  Authorisation
    ${response} =  Get On Session 	${DFAPI_UNAUTHENTICATED_SESSION} 	/${DFAPI_SERVER_PATH}/api/utility/ping  expected_status=any
    Set test variable  ${test_response}  ${response}

Utility ping
    [Tags]  Authorisation
    ${response} =  Get On Session 	${DFAPI_SESSION} 	/${DFAPI_SERVER_PATH}/api/utility/ping
    Set test variable  ${test_response}  ${response}

Start VPN
    # Run process blocks until command has finished.
    # Start process spawns the process and continues.
    # https://robotframework.org/robotframework/latest/libraries/Process.html#Specifying%20command%20and%20arguments
    Create File  vpnstart  content=${VPN_CONNECT_CMD}  encoding=UTF-8
    Run process  cat vpnstart | ${VPN_FOLDER}/${VPN_COMMAND}  shell=true  stdout=vpn-start-stdout.log  stderr=vpn-start-stderr.log

Stop VPN
    # Run process blocks until command has finished.
    # Start process spawns the process and continues.
    # https://robotframework.org/robotframework/latest/libraries/Process.html#Specifying%20command%20and%20arguments
    Create File  vpnstop   content=${VPN_DISCONNECT_CMD}  encoding=UTF-8
    #Run process  echo "${VPN_SCRIPT}"  shell=true  stdout=vpn-stdout.log  stderr=vpn-stderr.log
    #Run process  /usr/bin/sleep  1  stdout=vpn-stdout.log  stderr=vpn-stderr.log
    Run process  cat vpnstop | ${VPN_FOLDER}/${VPN_COMMAND}  shell=true  stdout=vpn-stop-stdout.log  stderr=vpn-stop-stderr.log


ORDS delete application
    [Documentation]  Calls the ORDS endpoints to delete the application.
    [Tags]  ORDS
    [Arguments]  ${prohibition_id}  ${correlation_id}
    #${auth} =    Create List  ${ORDS_USER}  ${ORDS_PASS}
    #Create session  ords_session  ${ORDS_HOST}  verify=True  auth=${auth}
    # DELETE https://{ORDS_DELETE_REVIEW_TIME_URL}/{NOTICE_NUMBER}/review/schedule/{FORM_TYPE}/{application_id}
    # Example session delete URL: https://dev.jag.gov.bc.ca/ords/deva/rsdfrmords/web/digitalForm/prohibition/182/333
    Create session  ords_session_application  ${ORDS_APPLICATION_ENDPOINT}  verify=False
    ${response} =  DELETE On Session 	ords_session_application  ${ORDS_APPLICATION_ENDPOINT}/${prohibition_id}/12345  expected_status=any
    Set test variable  ${test_response}  ${response}

ORDS delete reviews
    [Documentation]  Calls the ORDS endpoints to delete any scheduled reviews for an application.
    [Tags]  ORDS
    [Arguments]  ${notice_number}  ${form_type}  ${application_id}
    # Example: DELETE https://dev.jag.gov.bc.ca/ords/deva/vipsords/web/prohibition/21900104/review/schedule/ADP/1234
    Create session  ords_session_reviews  ${ORDS_REVIEW_TIME_ENDPOINT}  verify=False
    ${response} =  DELETE On Session 	ords_session_reviews  ${ORDS_REVIEW_TIME_ENDPOINT}/${notice_number}/review/schedule/${form_type}/${application_id}  expected_status=any
    Set test variable  ${test_response}  ${response}

POST new application
    [Arguments]  ${APPLICATION_TYPE}  ${PROHIBITION_NUM}  ${CORRELATION}  ${PAYLOAD}
    # NOTE: An HTTP 400 "Request could not be processed" usually means that the record already exists
    ${response} =  POST On Session 	${DFAPI_SESSION} 	/${DFAPI_SERVER_PATH}/${APPLICATION_TYPE}/${PROHIBITION_NUM}/application/${CORRELATION}  data=${PAYLOAD}  expected_status=any
    Set test variable  ${test_response}  ${response}

GET application
    [Arguments]  ${application_id}  ${CORRELATION}
    ${response} =  GET On Session 	${DFAPI_SESSION} 	/${DFAPI_SERVER_PATH}/${application_id}/application/${CORRELATION}
    set test variable  ${test_response}  ${response}

Application GET response matches expected ADP record
    [Documentation]  Compares the payload sent in the application with the reply.
    ${appInfo} =  Set Variable  ${test_response.json()['data']['applicationInfo']}
    Log  ${appInfo['prohibitionNoticeNo']}
    Should be equal  ${appInfo['prohibitionNoticeNo']}  ${ADP_REC_PROHIBITION_NUM}
    Should be equal  ${appInfo['email']}  ${ADP_REC_EMAIL}
    Should be equal  ${appInfo['faxNo']}  ${ADP_REC_FAXNO}
    Should be equal  ${appInfo['firstGivenNm']}  ${ADP_REC_FIRSTNAME}
    Should be equal  ${appInfo['formData']}  ${ADP_REC_FORMDATA}
    Should be equal  ${appInfo['manualEntryYN']}  ${ADP_REC_MANUAL_ENTRY}
    Should be equal  ${appInfo['noticeSubjectCd']}  ${ADP_REC_NOTICE_SUBJECT}
    Should be equal  ${appInfo['phoneNo']}  ${ADP_REC_PHONENO}
    Should be equal  ${appInfo['presentationTypeCd']}  ${ADP_REC_PRESENT_TYPE}
    Should be equal  ${appInfo['reviewRoleTypeCd']}  ${ADP_REC_ROLE_TYPE}
    Should be equal  ${appInfo['secondGivenNm']}  ${ADP_REC_MIDDLENAME}
    Should be equal  ${appInfo['surnameNm']}  ${ADP_REC_LASTNAME}

Application GET response matches expected IRP record
    [Documentation]  Compares the payload sent in the application with the reply.
    ${appInfo} =  Set Variable  ${test_response.json()['data']['applicationInfo']}
    Log  ${appInfo['prohibitionNoticeNo']}
    Should be equal  ${appInfo['prohibitionNoticeNo']}  ${IRP_REC_PROHIBITION_NUM}
    Should be equal  ${appInfo['email']}  ${IRP_REC_EMAIL}
    Should be equal  ${appInfo['faxNo']}  ${IRP_REC_FAXNO}
    Should be equal  ${appInfo['firstGivenNm']}  ${IRP_REC_FIRSTNAME}
    Should be equal  ${appInfo['formData']}  ${IRP_REC_FORMDATA}
    Should be equal  ${appInfo['manualEntryYN']}  ${IRP_REC_MANUAL_ENTRY}
    Should be equal  ${appInfo['noticeSubjectCd']}  ${IRP_REC_NOTICE_SUBJECT}
    Should be equal  ${appInfo['phoneNo']}  ${IRP_REC_PHONENO}
    Should be equal  ${appInfo['presentationTypeCd']}  ${IRP_REC_PRESENT_TYPE}
    Should be equal  ${appInfo['reviewRoleTypeCd']}  ${IRP_REC_ROLE_TYPE}
    Should be equal  ${appInfo['secondGivenNm']}  ${IRP_REC_MIDDLENAME}
    Should be equal  ${appInfo['surnameNm']}  ${IRP_REC_LASTNAME}

Application GET response matches expected UL record
    [Documentation]  Compares the payload sent in the application with the reply.
    ${appInfo} =  Set Variable  ${test_response.json()['data']['applicationInfo']}
    Log  ${appInfo['prohibitionNoticeNo']}
    Should be equal  ${appInfo['prohibitionNoticeNo']}  ${UL_REC_PROHIBITION_NUM}
    Should be equal  ${appInfo['email']}  ${UL_REC_EMAIL}
    Should be equal  ${appInfo['faxNo']}  ${UL_REC_FAXNO}
    Should be equal  ${appInfo['firstGivenNm']}  ${UL_REC_FIRSTNAME}
    Should be equal  ${appInfo['formData']}  ${UL_REC_FORMDATA}
    Should be equal  ${appInfo['manualEntryYN']}  ${UL_REC_MANUAL_ENTRY}
    Should be equal  ${appInfo['noticeSubjectCd']}  ${UL_REC_NOTICE_SUBJECT}
    Should be equal  ${appInfo['phoneNo']}  ${UL_REC_PHONENO}
    Should be equal  ${appInfo['presentationTypeCd']}  ${UL_REC_PRESENT_TYPE}
    Should be equal  ${appInfo['reviewRoleTypeCd']}  ${UL_REC_ROLE_TYPE}
    Should be equal  ${appInfo['secondGivenNm']}  ${UL_REC_MIDDLENAME}
    Should be equal  ${appInfo['surnameNm']}  ${UL_REC_LASTNAME}

Application GET response matches updated ADP record
    [Documentation]  Compares the payload sent in the application with the reply.
    ${appInfo} =  Set Variable  ${test_response.json()['data']['applicationInfo']}
    Log  ${appInfo['prohibitionNoticeNo']}
    Should be equal  ${appInfo['prohibitionNoticeNo']}  ${ADP_REC_PROHIBITION_NUM}
    Should be equal  ${appInfo['email']}  ${ADP_REC_EMAIL2}
    Should be equal  ${appInfo['faxNo']}  ${ADP_REC_FAXNO2}
    Should be equal  ${appInfo['firstGivenNm']}  ${ADP_REC_FIRSTNAME2}
    Should be equal  ${appInfo['formData']}  ${ADP_REC_FORMDATA2}
    Should be equal  ${appInfo['manualEntryYN']}  ${ADP_REC_MANUAL_ENTRY2}
    Should be equal  ${appInfo['noticeSubjectCd']}  ${ADP_REC_NOTICE_SUBJECT2}
    Should be equal  ${appInfo['phoneNo']}  ${ADP_REC_PHONENO2}
    Should be equal  ${appInfo['presentationTypeCd']}  ${ADP_REC_PRESENT_TYPE2}
    Should be equal  ${appInfo['reviewRoleTypeCd']}  ${ADP_REC_ROLE_TYPE2}
    Should be equal  ${appInfo['secondGivenNm']}  ${ADP_REC_MIDDLENAME2}
    Should be equal  ${appInfo['surnameNm']}  ${ADP_REC_LASTNAME2}

Application GET response matches updated IRP record
    [Documentation]  Compares the payload sent in the application with the reply.
    ${appInfo} =  Set Variable  ${test_response.json()['data']['applicationInfo']}
    Log  ${appInfo['prohibitionNoticeNo']}
    Should be equal  ${appInfo['prohibitionNoticeNo']}  ${IRP_REC_PROHIBITION_NUM}
    Should be equal  ${appInfo['email']}  ${IRP_REC_EMAIL2}
    Should be equal  ${appInfo['faxNo']}  ${IRP_REC_FAXNO2}
    Should be equal  ${appInfo['firstGivenNm']}  ${IRP_REC_FIRSTNAME2}
    Should be equal  ${appInfo['formData']}  ${IRP_REC_FORMDATA2}
    Should be equal  ${appInfo['manualEntryYN']}  ${IRP_REC_MANUAL_ENTRY2}
    Should be equal  ${appInfo['noticeSubjectCd']}  ${IRP_REC_NOTICE_SUBJECT2}
    Should be equal  ${appInfo['phoneNo']}  ${IRP_REC_PHONENO2}
    Should be equal  ${appInfo['presentationTypeCd']}  ${IRP_REC_PRESENT_TYPE2}
    Should be equal  ${appInfo['reviewRoleTypeCd']}  ${IRP_REC_ROLE_TYPE2}
    Should be equal  ${appInfo['secondGivenNm']}  ${IRP_REC_MIDDLENAME2}
    Should be equal  ${appInfo['surnameNm']}  ${IRP_REC_LASTNAME2}

Application GET response matches updated UL record
    [Documentation]  Compares the payload sent in the application with the reply.
    ${appInfo} =  Set Variable  ${test_response.json()['data']['applicationInfo']}
    Log  ${appInfo['prohibitionNoticeNo']}
    Should be equal  ${appInfo['prohibitionNoticeNo']}  ${UL_REC_PROHIBITION_NUM}
    Should be equal  ${appInfo['email']}  ${UL_REC_EMAIL2}
    Should be equal  ${appInfo['faxNo']}  ${UL_REC_FAXNO2}
    Should be equal  ${appInfo['firstGivenNm']}  ${UL_REC_FIRSTNAME2}
    Should be equal  ${appInfo['formData']}  ${UL_REC_FORMDATA2}
    Should be equal  ${appInfo['manualEntryYN']}  ${UL_REC_MANUAL_ENTRY2}
    Should be equal  ${appInfo['noticeSubjectCd']}  ${UL_REC_NOTICE_SUBJECT2}
    Should be equal  ${appInfo['phoneNo']}  ${UL_REC_PHONENO2}
    Should be equal  ${appInfo['presentationTypeCd']}  ${UL_REC_PRESENT_TYPE2}
    Should be equal  ${appInfo['reviewRoleTypeCd']}  ${UL_REC_ROLE_TYPE2}
    Should be equal  ${appInfo['secondGivenNm']}  ${UL_REC_MIDDLENAME2}
    Should be equal  ${appInfo['surnameNm']}  ${UL_REC_LASTNAME2}

PATCH application
    [Arguments]  ${APPLICATION_TYPE}  ${GUID}  ${CORRELATION}  ${PAYLOAD}
    ${response} =  PATCH On Session  ${DFAPI_SESSION}     /${DFAPI_SERVER_PATH}/${APPLICATION_TYPE}/${GUID}/application/${CORRELATION}  data=${PAYLOAD}
    Set test variable  ${test_response}  ${response}

Query status for application
    [Arguments]  ${NOTICE_NUMBER}  ${CORRELATION}
    ${response} =  GET On Session  ${DFAPI_SESSION}     /${DFAPI_SERVER_PATH}/${NOTICE_NUMBER}/status/${CORRELATION}
    Set test variable  ${test_response}  ${response}

Query response matches ADP record
    [Documentation]  Compares the payload sent in the application with the query reply.
    ${status} =  Set Variable  ${test_response.json()['data']['status']}
    Should be equal  ${status['noticeTypeCd']}  ADP
    #Should be equal  ${status['reviewFormSubmittedYn']}  Y
    #Should be equal  ${status['reviewCreatedYn']}  N
    Should be equal  ${status['originalCause']}  ADP09412
    Should be equal  ${status['surnameNm']}  Gordon
    #Should be equal  ${status['driverLicenceSeizedYn']}  Y
    #Should be empty  ${status['disclosure']}
    #Should be equal  ${reviews['status']}  unknown
    #${application} =  Set Variable  ${test_response.json()['data']['status']['reviews'][1]}
    #Should be equal  ${application['applicationId']}  ${ADP_APPLICATION_GUID}
    #${reviews} =  Set Variable  ${test_response.json()['data']['status']['reviews'][0]}

Query response matches IRP record
    [Documentation]  Compares the payload sent in the application with the query reply.
    ${status} =  Set Variable  ${test_response.json()['data']['status']}
    Should be equal  ${status['noticeTypeCd']}  IRP
    #Should be equal  ${status['reviewFormSubmittedYn']}  Y
    #Should be equal  ${status['reviewCreatedYn']}  N
    Should be equal  ${status['originalCause']}  IRP90FAIL
    Should be equal  ${status['surnameNm']}  Gordon
    #Should be equal  ${status['driverLicenceSeizedYn']}  N
    #Should be empty  ${status['disclosure']}
    #Should be equal  ${reviews['status']}  unknown
    #${application} =  Set Variable  ${test_response.json()['data']['status']['reviews'][1]}
    #Should be equal  ${application['applicationId']}  ${IRP_APPLICATION_GUID}
    #${reviews} =  Set Variable  ${test_response.json()['data']['status']['reviews'][0]}

Query response matches UL record
    [Documentation]  Compares the payload sent in the application with the query reply.
    ${status} =  Set Variable  ${test_response.json()['data']['status']}
    Should be equal  ${status['noticeTypeCd']}  UL
    #Should be equal  ${status['reviewFormSubmittedYn']}  Y
    #Should be equal  ${status['reviewCreatedYn']}  N
    Should be equal  ${status['originalCause']}  IRPINDEF
    Should be equal  ${status['surnameNm']}  Gordon
    #Should be equal  ${status['driverLicenceSeizedYn']}  N
    Should be empty  ${status['disclosure']}
    #Should be equal  ${reviews['status']}  unknown
    #${application} =  Set Variable  ${test_response.json()['data']['status']['reviews'][1]}
    #Should be equal  ${application['applicationId']}  ${UL_APPLICATION_GUID}
    #${reviews} =  Set Variable  ${test_response.json()['data']['status']['reviews'][0]}

Get disclosure document
    [Documentation]  Download evidence document file.
    [Arguments]  ${document_id}  ${CORRELATION}
    ${response} =  GET On Session 	${DFAPI_SESSION} 	/${DFAPI_SERVER_PATH}/${document_id}/disclosure/${CORRELATION}
    set test variable  ${test_response}  ${response}

Disclosure document should be a PDF file
   ${document} =  Set Variable  ${test_response.json()['data']['document']}
   Should be equal  ${document['mimeType']}  application/pdf
   Should not be empty  ${document['mimeType']}  document

PATCH disclosure status as sent
    [Arguments]  ${PAYLOAD}  ${CORRELATION}
    ${response} =  PATCH On Session 	${DFAPI_SESSION} 	/digitalforms/disclosure/${CORRELATION}  data=${PAYLOAD}
    set test variable  ${test_response}  ${response}

GET payment information
    [Arguments]  ${guid}  ${CORRELATION}
    ${response} =  GET On Session 	${DFAPI_SESSION} 	/digitalforms/${guid}/payment/status/${CORRELATION}
    set test variable  ${test_response}  ${response}

PATCH payment
    [Documentation]  Creates a JSON payment payload and submits it to the payment PATCH endpoint.
    [Arguments]  ${guid}  ${payment_amount}  ${payment_date}  ${card_type}  ${receipt_number}  ${CORRELATION}
    ${payment_payload} =  Set variable  {"transactionInfo":{"paymentAmount":"${payment_amount}","paymentCardType":"${card_type}","paymentDate":"${payment_date}","receiptNumberTxt":"${receipt_number}"}}
    # PATCH http://{{DFAPI_URL}}/{{application_id}}/payment/{{correlation_id}}
    ${response} =  PATCH On Session  ${DFAPI_SESSION}  /digitalforms/${guid}/payment/${CORRELATION}  data=${payment_payload}  expected_status=any
    set test variable  ${test_response}  ${response}

GET review schedule
    [Arguments]  ${form_type}  ${presentation_type}  ${days_from_today}  ${CORRELATION}
    ${todays_date} =	Get Current Date	UTC  -7 hours  result_format=%Y-%m-%d
    ${future_date} =  Add time to date  ${todays_date} 12:00:00.001  ${days_from_today}  result_format=%Y-%m-%d
    ${response} =  GET On Session 	${DFAPI_SESSION} 	/digitalforms/${form_type}/${presentation_type}/${future_date}/review/availableTimeSlot/${CORRELATION}
    set test variable  ${test_response}  ${response}
    Log  Time slots: ${test_response.json()['data']['timeSlots']}

POST review time
    [Arguments]  ${guid}  ${start_time}  ${stop_time}  ${correlation}
    ${appointment_payload} =  Set variable  {"timeSlot":{"reviewStartDtm":"${start_time}","reviewEndDtm":"${stop_time}"}}
    ${response} =  POST On Session  ${DFAPI_SESSION}  /digitalforms/${guid}/review/schedule/${correlation}  data=${appointment_payload}
    set test variable  ${test_response}  ${response}

There are two reviews found
    ${reviews_json} =      ${test_response.json()['data']['status']['reviews']}
    @{reviews_array}=         Get Value From Json     ${reviews_json}
    ${number_of_reviews}         Get length          ${reviews_array}
    Should be equal as integers  ${number_of_reviews}  2

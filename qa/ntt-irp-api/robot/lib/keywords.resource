*** Settings ***
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html


*** Keywords ***

Create DF VI-IRP API sessions
    [Documentation]  Set up authenticated and unauthenticated sessions for suite tests.

    # UNauthenticated session
    ${headers}=  Create dictionary   Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8
    Create Session 	unauthenticated_session 	${API_URL}  verify=True  headers=${headers}
    Set suite variable  ${UNAUTHENTICATED_SESSION}  unauthenticated_session    children=true

    # Authenticated session with credentials
    ${auth} =    Create List  ${API_USERNAME}  ${API_PASSWORD}
    ${headers}=  Create dictionary  Content-Type=application/json; charset=utf-8  Accept-Charset=utf-8
    Create Session      authenticated_session    url=${API_URL}  auth=${auth}  verify=True  headers=${headers}
    Set suite variable  ${AUTHENTICATED_SESSION}  authenticated_session    children=true

    ${date} =    Get Current Date    result_format=robot-%Y-%m-%d-%H:%M:%S
    Set suite variable    ${CORRELATION}    ${date}    children=true


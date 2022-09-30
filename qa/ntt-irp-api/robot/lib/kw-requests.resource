*** Settings ***


*** Keywords ***

# GET expecting success
An ${authentication_type} GET request to ${uri}
    [Documentation]  Generic HTTP GET method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  GET On Session 	${UNAUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_unauthenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  GET On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# GET expecting error
An ${authentication_type} GET request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP GET method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  GET On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  GET On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# POST expecting success
An ${authentication_type} POST request to ${uri} with payload ${payload}
    [Documentation]  Generic HTTP POST method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  POST On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_unauthenticated_response}  ${response}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  POST On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# POST expecting error
An ${authentication_type} POST request expecting HTTP ${expected_status_code} from ${uri} with payload ${payload}
    [Documentation]  Generic HTTP POST method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  POST On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  POST On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# PATCH expecting success
An ${authentication_type} PATCH request to ${uri} with payload ${payload}
    [Documentation]  Generic PATCH method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PATCH On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  ${payload}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PATCH On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${payload}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# PATCH expecting error
An ${authentication_type} PATCH request expecting HTTP ${expected_status_code} from ${uri} with payload ${payload}
    [Documentation]  Generic HTTP PATCH method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PATCH On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PATCH On Session 	${AUTHENTICATED_SESSION} 	${uri}  ${payload}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# DELETE expecting success
An ${authentication_type} HTTP DELETE request to ${uri}
    [Documentation]  Generic DELETE method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  DELETE On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  DELETE On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# DELETE expecting error
An ${authentication_type} DELETE request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP DELETE method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  DELETE On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  DELETE On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# DELETE expecting error
An unauthenticated HTTP DELETE request, expecting an error, to
    [Arguments]  ${URI}
    ${response} =  DELETE On Session 	${UNAUTHENTICATED_SESSION} 	${URI}  expected_status=405
    Set test variable  ${test_response}  ${response}


# HEAD expecting success
An ${authentication_type} HEAD request to ${uri}
    [Documentation]  Generic PATCH method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  HEAD On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  HEAD On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# HEAD, expecting error response
An ${authentication_type} HEAD request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP POST method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  HEAD On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  HEAD On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}


# OPTIONS expecting success
An ${authentication_type} OPTIONS request to ${uri}
    [Documentation]  Generic OPTIONS method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  OPTIONS On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  OPTIONS On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# OPTIONS expecting error
An ${authentication_type} OPTIONS request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP OPTIONS method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  OPTIONS On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  OPTIONS On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# PUT expecting success
An ${authentication_type} PUT request to ${uri}
    [Documentation]  Generic PUT method, authenticated or unauthenticated, expected to succeed.
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PUT On Session 	${UNAUTHENTICATED_SESSION} 	${uri}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PUT On Session 	${AUTHENTICATED_SESSION} 	${uri}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}

# PUT expecting error
An ${authentication_type} PUT request expecting HTTP ${expected_status_code} from ${uri}
    [Documentation]  Generic HTTP PUT method, used to get endpoints not yet implemented
    IF    "${authentication_type}" == "unauthenticated"
        ${response} =  PUT On Session 	${UNAUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
    ELSE IF     "${authentication_type}" == "authenticated"
        ${response} =  PUT On Session 	${AUTHENTICATED_SESSION} 	${uri}  expected_status=${expected_status_code}
        Set suite variable  ${last_authenticated_response}  ${response}
    ELSE
        Fail  msg=Unknown authentication type '${authentication_type}'.
    END
    Set test variable  ${test_response}  ${response}
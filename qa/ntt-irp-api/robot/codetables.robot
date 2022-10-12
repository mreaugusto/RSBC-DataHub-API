# Robot Framework

*** Settings ***
Documentation    Codetables GET endpoint
Library    JSONLibrary
Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # Used to check header response from RequestsLibrary
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

# Settings for the DEV environment
#Variables   dev.Variables              # Environment settings

Resource   lib/keywords.resource        # Keywords
Resource   lib/kw-requests.resource     # Keywords for server requests
Resource   lib/kw-responses.resource    # Keywords for server responses

*** Variables ***
# See env.py

*** Keywords ***
# See lib/*.robot

*** Test Cases ***
Codetables GET authenticated
    [Tags]           codetables  authenticated    GET    happy    grr
    [Documentation]  Should return code table
    ...
    ...              Example: ``$ https ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth "user:$PASSWORD"``
    Given An authenticated GET request to /v1/codetables/${CORRELATION}
    Then Response code is HTTP  200
    And Response content type is  application/json
#    And JSON payload includes respMsg section
    And JSON payload includes addresses section
    And JSON payload includes contactMethods section
    And JSON payload includes countries section
    And JSON payload includes data_sources section
    And JSON payload includes decisionOutcomes section
    And JSON payload includes disposalActs section
    And JSON payload includes disposalDecisions section
    And JSON payload includes documentNotices section
    And JSON payload includes documents section
    And JSON payload includes dreEvaluations section
    And JSON payload includes driverLicenceOffices section
    And JSON payload includes groundsDecisions section
    And JSON payload includes impoundLotOperators section
    And JSON payload includes jurisdictions section
    And JSON payload includes noticePrefixNos section
    And JSON payload includes noticeTypes section
    And JSON payload includes originalCauses section
    And JSON payload includes policeDetachments section
    And JSON payload includes provinces section
    And JSON payload includes registration_roles section
    And JSON payload includes releaseReasons section
    And JSON payload includes reviewApplications section
    And JSON payload includes reviewRoles section
    And JSON payload includes reviewStatuses section
    And JSON payload includes reviewTypes section
    And JSON payload includes scheduleAppTypes section
    And JSON payload includes unavailabilityReasons section
    And JSON payload includes vehicleTypes section
    And JSON structure addresses should have at least 3 records

    

Codetables GET not logged in
    [Tags]           codetables  unauthenticated    GET    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated GET request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response content type is  application/json
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}


Codetables OPTIONS authenticated
    [Tags]           codetables    authenticated    OPTIONS    happy
    [Documentation]  Should show supported headers
    ...
    ...              Example: ``$ https OPTIONS ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated OPTIONS request to /v1/codetables/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response allow header should contain value GET,HEAD,OPTIONS

Codetables OPTIONS not logged in
    [Tags]           codetables    unauthenticated    OPTIONS    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated OPTIONS request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables HEAD authenticated
    [Tags]           codetables    authenticated    HEAD    happy
    [Documentation]  Should return headers, content
    ...
    ...              Example: ``$ https HEAD ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated HEAD request to /v1/codetables/${CORRELATION}
    Then Response code is HTTP  200
    And Response body is empty
    And Response content type is  application/json
    And Response pragma header should contain value no-cache
    And Response cache-control header should contain value no-cache, no-store, max-age=0, must-revalidate
    And Response x-content-type-options header should contain value nosniff
    And Response x-frame-options header should contain value DENY
    And Response x-xss-protection header should contain value 1; mode=block

Codetables HEAD not logged in
    [Tags]           codetables    unauthenticated    HEAD    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https OPTIONS ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated HEAD request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is empty

Codetables DELETE authenticated
    [Tags]           codetables    authenticated    DELETE    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https DELETE ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated DELETE request expecting HTTP 500 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'DELETE' not supported"}

Codetables DELETE not logged in
    [Tags]           codetables    unauthenticated    DELETE    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https DELETE ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated DELETE request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables PUT authenticated
    [Tags]           codetables    authenticated  PUT    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PUT ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PUT request expecting HTTP 500 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PUT' not supported"}

Codetables PUT not logged in
    [Tags]           codetables    unauthenticated    PUT    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PUT ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated PUT request expecting HTTP 401 from /v1/codetables/${CORRELATION}
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables POST authenticated
    [Tags]           codetables    authenticated    POST    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https POST ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated POST request expecting HTTP 500 from /v1/codetables/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'POST' not supported"}

Codetables POST not logged in
    [Tags]           codetables    unauthenticated    POST    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https POST ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated POST request expecting HTTP 401 from /v1/codetables/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}

Codetables PATCH authenticated
    [Tags]           codetables    authenticated    PATCH    unhappy
    [Documentation]  Should return unsupported
    ...
    ...              Example: ``$ https PATCH ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION} --auth user:$PASSWORD``
    Given An authenticated PATCH request expecting HTTP 500 from /v1/codetables/${CORRELATION} with payload ""
    Then Response code is HTTP  500
    And Response body is  {"status_message":"Request method 'PATCH' not supported"}

Codetables PATCH not logged in
    [Tags]           codetables    unauthenticated    PATCH    unhappy
    [Documentation]  Should return HTTP 401
    ...
    ...              Example: ``$ https PATCH ://digitalforms-viirp-api-c220ad-dev.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/codetables/${CORRELATION}``
    Given An unauthenticated PATCH request expecting HTTP 401 from /v1/codetables/${CORRELATION} with payload ""
    Then Response code is HTTP  401
    And Response body is  {"status_message":"401 - Unauthorized entry, please authenticate"}
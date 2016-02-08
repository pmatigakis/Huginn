*** Settings ***
Library    Process
Library    String

*** Variables ***
${HUGINN_URL}    http://localhost:8090

*** Keywords ***
Start Huginn
    ${huginn_process_id} =    Start Process    huginn_start.py --aircraft Rascal    shell=true
    Process Should Be Running    ${huginn_process_id}
    Create Session    huginn_web_server    ${HUGINN_URL}
    Wait Until Keyword Succeeds    1 min    5 sec    Get Request    huginn_web_server    /
    
Stop Huginn
    Terminate All Processes

Value Close To
    [Arguments]    ${value}    ${expected_value}    ${tolerance}
    Should Be True    ${value} >= ${expected_value} - ${tolerance} 
    Should Be True    ${value} <= ${expected_value} + ${tolerance}    

Simulator Command Executed Successfully
    [Arguments]    ${response}    ${command}
    Should be Equal As Strings    ${response.status_code}    200
    Dictionary Should Contain Key    ${response.json()}    command
    Dictionary Should Contain Key    ${response.json()}    result
    Should be Equal As Strings    ${response.json()['command']}    ${command}
    Should be Equal As Strings    ${response.json()['result']}    ok

Execute Simulator Control Command
    [Arguments]    ${session}    ${command}
    ${command} =    Create Dictionary  command  ${command}
    ${resp} =    Post Request    huginn_web_server    /simulator    ${command}
    [Return]    ${resp}

JSON Response Should Contain item
    [Arguments]    ${response}  ${item}
    Dictionary Should Contain Key    ${response.json()}  ${item}

Response Content Type Should Be JSON
    [Arguments]    ${response}
    ${content_type} =    Get Substring    ${response.headers['content-type']}  0  16
    Should Be Equal    ${content_type}    application/json

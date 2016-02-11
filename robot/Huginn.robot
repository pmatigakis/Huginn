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
    Simulator Is Paused
    Simulator DT Should Be    0.00625
    Simulation Time Should Be Close To    1.0  0.1
    
Stop Huginn
    Terminate All Processes

Value Close To
    [Arguments]    ${value}    ${expected_value}    ${tolerance}
    Should Be True    ${value} >= ${expected_value} - ${tolerance} 
    Should Be True    ${value} <= ${expected_value} + ${tolerance}    

Simulator Command Executed Successfully
    [Arguments]    ${response}    ${command}
    Response Status Code Should Be    ${response}  200
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

Simulator Is Running
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  running
    ${running} =    Convert To Boolean    ${resp.json()['running']}
    Should Be True    ${running}

Simulator Is Paused
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  running
    ${running} =    Convert To Boolean    ${resp.json()['running']}
    Should Not Be True    ${running}

Simulator DT Should Be
    [Arguments]    ${dt}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  dt
    Should Be Equal As Numbers    ${resp.json()['dt']}  0.00625

Simulation Time Should Be Close To
    [Arguments]    ${time}  ${difference}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  time
    ${min_value} =    Set Variable    ${time} - ${difference}
    Should Be True    ${resp.json()['time']} >= ${min_value}
    ${max_value} =    Set Variable    ${time} + ${difference}
    Should Be True    ${resp.json()['time']} <= ${max_value}

Simulation Time Should Be Greater Than
    [Arguments]    ${time}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  time
    Should Be True    ${resp.json()['time']} > ${time}

Response Status Code Should Be
    [Arguments]    ${response}  ${status_code}
    Should be Equal As Integers    ${response.status_code}  ${status_code}

Send Get HTTP Command
    [Arguments]    ${command_url}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  ${command_url}
    [Return]    ${resp}

Resume Simulation
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Execute Simulator Control Command    huginn_web_server  resume
    Simulator Command Executed Successfully    ${resp}  resume

Reset Simulator
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Execute Simulator Control Command    huginn_web_server  reset
    Simulator Command Executed Successfully    ${resp}  reset

Pause Simulator
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Execute Simulator Control Command    huginn_web_server  pause
    Simulator Command Executed Successfully    ${resp}  pause

Get Simulator Time
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /simulator
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  time
    ${simulator_time} =    Convert To Number    ${resp.json()['time']}
    [Return]    ${simulator_time}

Execute Single Simulation Step
    ${resp} =    Execute Simulator Control Command    huginn_web_server  step
    Simulator Command Executed Successfully    ${resp}  step

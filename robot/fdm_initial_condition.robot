*** Settings ***
Test Setup    Start Huginn
Test Teardown    Stop Huginn
Library    Collections
Library    RequestsLibrary
Resource    Huginn.robot

*** Test Cases ***
Change The Simulator Initial Condition
    [Documentation]    This test checks if the initial conditions are changed
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Initial Condition Data
    Is Valid FDM Initial Condition Data Response    ${resp}
    Is FDM Initial Condition Data Response With Aircraft In The Start Location    ${resp}
    ${new_latitude} =    Set variable  10.0
    ${new_longitude} =    Set variable  20.0
    ${new_airspeed} =    Set variable  60.0
    ${new_altitude} =    Set variable  150.0
    ${new_heading} =    Set variable  90.0
    Change initial Condition    ${new_latitude}  ${new_longitude}  ${new_airspeed}  ${new_altitude}  ${new_heading}
    ${resp} =    Get FDM Initial Condition Data
    Is Valid FDM Initial Condition Data Response    ${resp}
    Should Be Equal As Numbers    ${resp.json()['latitude']}  ${new_latitude}  precision=1
    Should Be Equal As Numbers    ${resp.json()['longitude']}  ${new_longitude}  precision=1
    Should Be Equal As Numbers    ${resp.json()['airspeed']}  ${new_airspeed}  precision=3
    Should Be Equal As Numbers    ${resp.json()['altitude']}  ${new_altitude}  precision=3
    Should Be Equal As Numbers    ${resp.json()['heading']}  ${new_heading}  precision=3

Change The initial Condition And Reset The Simulator    
    [Documentation]    This test checks if the simulator loads the new initial conditions after a reset
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Initial Condition Data
    Is Valid FDM Initial Condition Data Response    ${resp}
    Is FDM Initial Condition Data Response With Aircraft In The Start Location    ${resp}
    ${new_latitude} =    Set variable  35.513645
    ${new_longitude} =    Set variable  24.020655
    ${new_airspeed} =    Set variable  40.0
    ${new_altitude} =    Set variable  400.0
    ${new_heading} =    Set variable  90.0
    Change initial Condition    ${new_latitude}  ${new_longitude}  ${new_airspeed}  ${new_altitude}  ${new_heading}
    ${resp} =    Get FDM Initial Condition Data
    Is Valid FDM Initial Condition Data Response    ${resp}
    Should Be Equal As Numbers    ${resp.json()['latitude']}  ${new_latitude}  precision=1
    Should Be Equal As Numbers    ${resp.json()['longitude']}  ${new_longitude}  precision=1
    Should Be Equal As Numbers    ${resp.json()['airspeed']}  ${new_airspeed}  precision=3
    Should Be Equal As Numbers    ${resp.json()['altitude']}  ${new_altitude}  precision=3
    Should Be Equal As Numbers    ${resp.json()['heading']}  ${new_heading}  precision=3
    Reset Simulator
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /fdm/position
    Should be Equal As Strings    ${resp.status_code}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  latitude
    JSON Response Should Contain item    ${resp}  longitude
    JSON Response Should Contain item    ${resp}  altitude
    JSON Response Should Contain item    ${resp}  heading
    Should Be Equal As Numbers    ${resp.json()['latitude']}  ${new_latitude}  precision=1
    Should Be Equal As Numbers    ${resp.json()['longitude']}  ${new_longitude}  precision=1
    Value Close To    ${resp.json()['altitude']}  ${new_altitude}  10
    Value Close To    ${resp.json()['heading']}  ${new_heading}  5
    ${resp} =    Get Request    huginn_web_server  /fdm/velocities
    Should be Equal As Strings    ${resp.status_code}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  true_airspeed
    Value Close To    ${resp.json()['true_airspeed']}  ${new_airspeed}  5

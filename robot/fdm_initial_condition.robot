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
    Is FDM Initial Condition Data Response With Aircraft At Location    ${resp}  ${new_latitude}  ${new_longitude}  ${new_altitude}  ${new_heading}  ${new_airspeed}

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
    Is FDM Initial Condition Data Response With Aircraft At Location    ${resp}  ${new_latitude}  ${new_longitude}  ${new_altitude}  ${new_heading}  ${new_airspeed}
    Reset Simulator
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /fdm/position
    Is Valid FDM Position Data Response    ${resp}
    Is FDM Position Data Response With Aircraft At Location    ${resp}  ${new_latitude}  ${new_longitude}  ${new_altitude}  ${new_heading}
    ${resp} =    Get Request    huginn_web_server  /fdm/velocities
    Is Valid FDM Velocity Data Response    ${resp}
    True Airspeed From Velocities Response Is    ${resp}  ${new_airspeed}

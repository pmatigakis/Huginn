*** Settings ***
Suite Setup    Start Huginn
Suite Teardown    Stop Huginn
Library    Collections
Library    RequestsLibrary
Resource    Huginn.robot

*** Test Cases ***
FDM API returns the fdm data
    [Documentation]    This test checks if the fdm endpoint returns fdm data
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Data
    Is Valid FDM Data Response    ${resp}
    Is FDM Data Response With Aircraft In The Start Location    ${resp}

FDM Accelerations endpoint returns the accelerations data
    [Documentation]    This test checks if the fdm accelerations endpoint return the accelerations data
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Accelerations Data
    Is Valid FDM Accelerations Data Response    ${resp}
    Is FDM Accelerations Data Response With Aircraft In The Start Location    ${resp}

FDM Velocities endpoint returns the velocity data
    [Documentation]    This test checks if the fdm velocities endpoint return the velocity data
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Velocity Data
    Is Valid FDM Velocity Data Response    ${resp}
    Is FDM Velocity Data Response With Aircraft In The Start Location    ${resp}

FDM Orientation endpoint returns the orientation data
    [Documentation]    This test checks if the fdm orientation endpoint return the orientation data
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Orientation Data
    Is Valid FDM Orientation Data Response    ${resp}
    Is FDM Orientation Data Response With Aircraft In The Start Location    ${resp}

FDM Atmosphere endpoint returns the atmosphere data
    [Documentation]    This test checks if the fdm atmosphere endpoint return the atmosphere data
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Atmosphere Data
    Is Valid FDM Atmosphere Data Response    ${resp}
    Is FDM Atmosphere Data Response With Aircraft In The Start Location    ${resp}

FDM Forces endpoint returns the aerodynamic forces data
    [Documentation]    This test checks if the fdm forces endpoint returns the aerodynamic forces data
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Forces Data
    Is Valid FDM Forces Data Response    ${resp}
    Is FDM Forces Data Response With Aircraft In The Start Location    ${resp}

FDM Initial Condition endpoint returns the initial condition data
    [Documentation]    This test checks if the fdm initial condition endpoint returns the initial condition data
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Initial Condition Data
    Is Valid FDM Initial Condition Data Response    ${resp}
    Is FDM Initial Condition Data Response With Aircraft In The Start Location    ${resp}    

FDM Position endpoint returns the position data
    [Documentation]    This test checks if the fdm position returns the position data
    [Tags]    api    fdm
    Simulator Is Paused
    Aircraft Should Be In The Start Location
    ${resp} =    Get FDM Position Data
    Is Valid FDM Position Data Response    ${resp}
    Is FDM Position Data Response With Aircraft In The Start Location    ${resp}

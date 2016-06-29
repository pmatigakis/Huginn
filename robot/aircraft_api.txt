*** Settings ***
Suite Setup    Start Huginn
Suite Teardown    Stop Huginn
Library    Collections
Library    RequestsLibrary
Resource    Huginn.robot

*** Test Cases ***
GPS endpoint returns the gps data
    [Documentation]    This test checks if the gps endpoint returns the gps data
    [Tags]    api    fdm    sensors
    ${response} =    Get GPS Data
    Should Be valid GPS Response    ${response}
    SHould Be GPS Response When Aircraft Is In The Start Location    ${response}
 
Accelerometer endpoint returns the accelerometer data
    [Documentation]    This test checks if the accelerometer endpoint returns the accelerometer data
    [Tags]    api    fdm    sensors
    ${response} =    Get Accelerometer Data
    Should Be Valid Accelerometer Response    ${response}
    Should Be Accelerometer Response With Aircraft Almost Level    ${response}

Gyroscope endpoint returns the gyroscope data
    [Documentation]    This test checks if the gyroscope endpoint returns the gyroscope data
    [Tags]    api    fdm    sensors
    ${response} =    Get Gyroscope Data
    Should Be Valid Gyroscope Response    ${response}
    Should Be Gyroscope Response With Minimal Aircraft Rotation    ${response}

Thermometer endpoint returns the thermometer data
    [Documentation]    This test checks if the thermometer endpoint returns the thermometer data
    [Tags]    api    fdm    sensors
    ${response} =    Get Thermometer Data
    Should Be Valid Thermometer Response    ${response}
    Should Be Valid Thermometer Response When Aircraft At 300 Meters Above Sea Level    ${response}

Pressure sensor endpoint returns the thermometer data
    [Documentation]    This test checks if the pressure sensor endpoint returns the pressure sensor data
    [Tags]    api    fdm    sensors
    ${response} =    Get Pressure Sensor Data
    Should Be Valid Pressure Sensor Response    ${response}
    Should Be Pressure Sensor Response When Aircraft At 300 Meters Above Sea Level    ${response}

Pitot tube sensor endpoint returns the pitot tube data
    [Documentation]    This test checks if the pitot tube sensor endpoint returns the pitot tube data
    [Tags]    api    fdm    sensors
    ${response} =    Get Pitot Tube Data
    Should Be Valid Pitot Tube Response    ${response}
    Should Be Pitot Tube Response When Airspeed At 30 Meters Per Second    ${response}

Inertial navigation system endpoint returns the inertial navigation system data
    [Documentation]    This test checks if the inertial navigation system endpoint returns the inertial navigation system data
    [Tags]    api    fdm    sensors
    ${response} =    Get INS Data
    Should Be Valid INS Response    ${response}
    Should Be Valid INS Response When Aircraft In The Start Location    ${response}

Engine endpoint returns the engine data
    [Documentation]    This test checks if the engine endpoint returns the engine data
    [Tags]    api    fdm    engines
    ${response} =    Get Engine Data
    Should Be Valid Engine Response    ${response}
    Should Be Valid Engine Response With Engine On Idle    ${response}

Flight controls endpoint returns the flight controls data
    [Documentation]    This test checks if the flight controls endpoint returns the flight controls data
    [Tags]    api    fdm    controls
    ${response} =    Get The Flight Controls Data
    Should Be Valid Flight Control Response    ${response}
    Should be Valid Flight Controls Response With Flight Controls Idle    ${response}

Airspeed Indicator endpoint returns the airspeed indicator data
    [Documentation]    This test checks if the airspeed indicator  endpoint returns the airspeed indicator data
    [Tags]    api    fdm    instruments
    ${response} =    Get Airspeed Indicator Data
    Should Be Valid Airspeed Indicator Response    ${response}
    Should Be Airspeed Indicator Response When Aircraft Is In The Start Location    ${response}

Altimeter endpoint returns the altimeter data
    [Documentation]    This test checks if the altimeter  endpoint returns the altimeter data
    [Tags]    api    fdm    instruments
    ${response} =    Get Altimeter Data
    Should Be Valid Altimeter Response    ${response}
    Should Be Altimeter Response When Aircraft Is In The Start Location    ${response}

Attitude Indicator endpoint returns the Attitude Indicator data
    [Documentation]    This test checks if the attitude indicator endpoint returns the attitude indicator data
    [Tags]    api    fdm    instruments
    ${response} =    Get Attitude Indicator Data
    Should Be Valid Attitude Indicator Response    ${response}
    Should Be Attitude Indicator Response When Aircraft Is In The Start Location    ${response}

Heading Indicator endpoint returns the Heading Indicator data
    [Documentation]    This test checks if the heading indicator endpoint returns the heading indicator data
    [Tags]    api    fdm    instruments
    ${response} =    Get Heading Indicator Data
    Should Be Valid Heading Indicator Response    ${response}
    Should Be Heading Indicator Response When Aircraft Is In The Start Location    ${response}

Vertical Speed Indicator endpoint returns the Vertical Speed Indicator data
    [Documentation]    This test checks if the vertical speed indicator endpoint returns the vertical speed indicator data
    [Tags]    api    fdm    instruments
    ${response} =    Get Vertical Speed Indicator Data
    Should Be Valid Vertical Speed Indicator Response    ${response}
    Should Be Vertical Speed Indicator Response When Aircraft Is In The Start Location    ${response}

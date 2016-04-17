*** Settings ***
Library    Process
Library    String
Library    RequestsLibrary
Library    Collections

*** Variables ***
${HUGINN_URL}    http://localhost:8090
${IC_X_ACCELERATION}    -2.3863054128
${IC_Y_ACCELERATION}    0.300261528
${IC_Z_ACCELERATION}    -8.0968135752
${IC_ROLL_RATE}    1.153077531
${IC_PITCH_RATE}    -3.2386438479
${IC_YAW_RATE}    1.04547606
${IC_PRESSURE}    97771.68
${IC_TOTAL_PRESSURE}    98224.25

*** Keywords ***
Start Huginn
    ${huginn_process_id} =    Start Process    huginn_start.py --aircraft Rascal    shell=true
    Process Should Be Running    ${huginn_process_id}
    Create Session    huginn_web_server    ${HUGINN_URL}
    Wait Until Keyword Succeeds    1 min    1 sec    Get Request    huginn_web_server    /
    Simulator Is Paused
    Simulator DT Should Be    0.003333
    Simulation Time Should Be Close To    1.0  0.1
    
Stop Huginn
    Terminate All Processes

Resume Simulation Using The CLI
    ${result} =    Run Process    huginn_control.py resume  shell=true
    Should Be Equal As Integers    ${result.rc}  0

Pause the Simulation Using The CLI
    ${result} =    Run Process    huginn_control.py pause  shell=true
    Should Be Equal As Integers    ${result.rc}  0

Reset the Simulation Using The CLI
    ${result} =    Run Process    huginn_control.py reset  shell=true
    Should Be Equal As Integers    ${result.rc}  0

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
    [Arguments]    ${session}    ${command}    ${params}={}
    #${command_data} =    Create Dictionary  command=${command}
    ${resp} =    Post Request    huginn_web_server  /simulator/${command}  params=${params}
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
    Should Be Equal As Numbers    ${resp.json()['dt']}  ${dt}

Simulation Time Should Be Close To
    [Arguments]    ${time}  ${difference}=0.1
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

Run The Simulation For The Given Time
    [Arguments]    ${time_to_run}
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${params} =    Create Dictionary  time_to_run=${time_to_run}
    ${resp} =    Execute Simulator Control Command    huginn_web_server  run_for  ${params}
    Simulator Command Executed Successfully    ${resp}  run_for

Aircraft Should Be In The Start Location
    ${resp} =    Get Request    huginn_web_server  /aircraft/gps
    Response Status Code Should Be    ${resp}  200
    Response Content Type Should Be JSON    ${resp}
    JSON Response Should Contain item    ${resp}  latitude
    JSON Response Should Contain item    ${resp}  longitude
    JSON Response Should Contain item    ${resp}  altitude
    JSON Response Should Contain item    ${resp}  airspeed
    JSON Response Should Contain item    ${resp}  heading
    Value Close To    ${resp.json()['latitude']}  37.923255  0.001
    Value Close To    ${resp.json()['longitude']}  23.921773  0.001
    Value Close To    ${resp.json()['altitude']}  300.00000  10.0
    Value Close To    ${resp.json()['airspeed']}  30.00000  5.0
    Value Close To    ${resp.json()['heading']}  45.00000  5.0

Get FDM Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /fdm
    [Return]    ${resp}

Is Valid FDM Data Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  time
    JSON Response Should Contain item    ${response}  dt
    JSON Response Should Contain item    ${response}  latitude
    JSON Response Should Contain item    ${response}  longitude
    JSON Response Should Contain item    ${response}  altitude
    JSON Response Should Contain item    ${response}  airspeed
    JSON Response Should Contain item    ${response}  heading
    JSON Response Should Contain item    ${response}  aileron
    JSON Response Should Contain item    ${response}  elevator
    JSON Response Should Contain item    ${response}  rudder
    JSON Response Should Contain item    ${response}  throttle
    JSON Response Should Contain item    ${response}  x_acceleration
    JSON Response Should Contain item    ${response}  y_acceleration
    JSON Response Should Contain item    ${response}  z_acceleration
    JSON Response Should Contain item    ${response}  roll_rate
    JSON Response Should Contain item    ${response}  pitch_rate
    JSON Response Should Contain item    ${response}  yaw_rate
    JSON Response Should Contain item    ${response}  temperature
    JSON Response Should Contain item    ${response}  static_pressure
    JSON Response Should Contain item    ${response}  total_pressure
    JSON Response Should Contain item    ${response}  roll
    JSON Response Should Contain item    ${response}  pitch
    JSON Response Should Contain item    ${response}  thrust

Is FDM Data Response With Aircraft In The Start Location
    [Arguments]    ${response}
    Value Close To    ${response.json()['latitude']}  37.923255  0.001
    Value Close To    ${response.json()['longitude']}  23.921773  0.001
    Value Close To    ${response.json()['altitude']}  300.00000  10.0
    Value Close To    ${response.json()['airspeed']}  30.00000  5.0
    Value Close To    ${response.json()['heading']}  45.00000  5.0
    Should Be Equal As Numbers    ${response.json()['aileron']}  0.00000  precision=4
    Should Be Equal As Numbers    ${response.json()['elevator']}  0.00000  precision=4
    Should Be Equal As Numbers    ${response.json()['rudder']}  0.00000  precision=4
    Should Be Equal As Numbers    ${response.json()['throttle']}  0.00000  precision=4
    Value Close To    ${response.json()['roll']}  0.00000  5.0
    Value Close To    ${response.json()['pitch']}  0.00000  5.0
    Should Be Equal As Numbers    ${response.json()['x_acceleration']}  ${IC_X_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['y_acceleration']}  ${IC_Y_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['z_acceleration']}  ${IC_Z_ACCELERATION}  precision=4
    Should Be Equal As Numbers    ${response.json()['roll_rate']}  ${IC_ROLL_RATE}  precision=4
    Should Be Equal As Numbers    ${response.json()['pitch_rate']}  ${IC_PITCH_RATE}  precision=4
    Should Be Equal As Numbers    ${response.json()['yaw_rate']}  ${IC_YAW_RATE}  precision=4
    Value Close To    ${response.json()['total_pressure']}  ${IC_TOTAL_PRESSURE}  1.0
    Value Close To    ${response.json()['static_pressure']}  ${IC_PRESSURE}  1.0

Get GPS Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${response} =    Get Request    huginn_web_server  /aircraft/gps
    [Return]    ${response}

Should Be Valid GPS Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  latitude
    JSON Response Should Contain item    ${response}  longitude
    JSON Response Should Contain item    ${response}  altitude
    JSON Response Should Contain item    ${response}  airspeed
    JSON Response Should Contain item    ${response}  heading

Should Be GPS Response When Aircraft Is In The Start Location
    [Arguments]    ${response}
    Value Close To    ${response.json()['latitude']}  37.923255  0.001
    Value Close To    ${response.json()['longitude']}  23.921773  0.001
    Value Close To    ${response.json()['altitude']}  300.00000  10.0
    Value Close To    ${response.json()['airspeed']}  30.00000  5.0
    Value Close To    ${response.json()['heading']}  45.00000  5.0

Get Accelerometer Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${response} =    Get Request    huginn_web_server  /aircraft/accelerometer
    [Return]    ${response}

Should Be Valid Accelerometer Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  x_acceleration
    JSON Response Should Contain item    ${response}  y_acceleration
    JSON Response Should Contain item    ${response}  z_acceleration

Should Be Accelerometer Response With Aircraft Almost Level
    [Arguments]    ${response}
    Value Close To    ${response.json()['x_acceleration']}  0.0  3.0
    Value Close To    ${response.json()['y_acceleration']}  0.0  3.0
    Value Close To    ${response.json()['z_acceleration']}  -9.8  3.0

Get Gyroscope Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/gyroscope
    [Return]    ${resp}

Should Be Valid Gyroscope Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  roll_rate
    JSON Response Should Contain item    ${response}  pitch_rate
    JSON Response Should Contain item    ${response}  yaw_rate

Should Be Gyroscope Response With Minimal Aircraft Rotation
    [Arguments]    ${response}
    Value Close To    ${response.json()['roll_rate']}  0.0  5.0
    Value Close To    ${response.json()['pitch_rate']}  0.0  5.0
    Value Close To    ${response.json()['yaw_rate']}  0.0  5.0

Get Thermometer Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/thermometer
    [Return]    ${resp}

Should Be Valid Thermometer Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  temperature

Should Be Valid Thermometer Response When Aircraft At 300 Meters Above Sea Level
    [Arguments]    ${response}
    Value Close To    ${response.json()['temperature']}  280.0  10.0

Get Pressure Sensor Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/pressure_sensor
    [Return]    ${resp}

Should Be Valid Pressure Sensor Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  static_pressure

Should Be Pressure Sensor Response When Aircraft At 300 Meters Above Sea Level
    [Arguments]    ${response}
    Value Close To    ${response.json()['static_pressure']}  97000.0  5000.0

Get Pitot Tube Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/pitot_tube
    [Return]    ${resp}

Should Be Valid Pitot Tube Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  total_pressure

Should Be Pitot Tube Response When Airspeed At 30 Meters Per Second
    [Arguments]    ${response}
    Value Close To    ${response.json()['total_pressure']}  97000.0  5000.0

Get INS Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/ins
    [Return]    ${resp}

Should Be Valid INS Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  latitude
    JSON Response Should Contain item    ${response}  longitude
    JSON Response Should Contain item    ${response}  altitude
    JSON Response Should Contain item    ${response}  airspeed
    JSON Response Should Contain item    ${response}  heading
    JSON Response Should Contain item    ${response}  pitch
    JSON Response Should Contain item    ${response}  roll

Should Be Valid INS Response When Aircraft In The Start Location
    [Arguments]    ${response}
    Value Close To    ${response.json()['latitude']}  37.923255  0.001
    Value Close To    ${response.json()['longitude']}  23.921773  0.001
    Value Close To    ${response.json()['altitude']}  300.00000  10.0
    Value Close To    ${response.json()['airspeed']}  30.00000  5.0
    Value Close To    ${response.json()['heading']}   45.00000  5.0
    Value Close To    ${response.json()['roll']}  0.0  3.0
    Value Close To    ${response.json()['pitch']}  0.0  3.0

Get Engine Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/engine
    [Return]    ${resp}

Should Be Valid Engine Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  thrust
    JSON Response Should Contain item    ${response}  throttle

Should Be Valid Engine Response With Engine On Idle
    [Arguments]    ${response}
    Should Be Equal As Numbers    ${response.json()['throttle']}  0.0

Get The Flight Controls Data
    Create Session    huginn_web_server  ${HUGINN_URL}
    ${resp} =    Get Request    huginn_web_server  /aircraft/flight_controls
    [Return]    ${resp}

Should Be Valid Flight Control Response
    [Arguments]    ${response}
    Should be Equal As Strings    ${response.status_code}  200
    Response Content Type Should Be JSON    ${response}
    JSON Response Should Contain item    ${response}  aileron
    JSON Response Should Contain item    ${response}  elevator
    JSON Response Should Contain item    ${response}  rudder
    JSON Response Should Contain item    ${response}  throttle

Should be Valid Flight Controls Response With Flight Controls Idle
    [Arguments]    ${response}
    Should Be Equal As Numbers    ${response.json()['aileron']}  0.0
    Should Be Equal As Numbers    ${response.json()['elevator']}  0.0
    Should Be Equal As Numbers    ${response.json()['rudder']}  0.0
    Should Be Equal As Numbers    ${response.json()['throttle']}  0.0

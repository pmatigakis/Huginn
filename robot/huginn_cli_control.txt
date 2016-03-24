*** Settings ***
Suite Setup    Start Huginn
Suite Teardown    Stop Huginn
Test Teardown    Reset Simulator
Resource    Huginn.robot

*** Test Cases ***
Resume the simulator using the control script
    [Documentation]    Resume the simulator using the control script
    [Tags]    cli
    Simulator is Paused
    Resume Simulation Using The CLI
    Simulator is Running

Pause the simulator using the control script
    [Documentation]    Pause the simulator using the control script
    [Tags]    cli
    Simulator is Paused
    Resume Simulation Using The CLI
    Simulator is Running
    Pause The Simulation Using The CLI
    Simulator is Paused

Reset the simulator using the control script
    [Documentation]    Reset the simulator using the control script
    [Tags]    cli
    Simulator is Paused
    Simulation Time Should Be Close To    1.0
    Resume Simulation Using The CLI
    Simulator is Running
    Sleep    3.0
    Simulation Time Should Be Greater Than    3.0
    Reset The Simulation Using The CLI
    Simulator is Paused
    Simulation Time Should Be Close To    1.0

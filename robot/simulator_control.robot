*** Settings ***
Suite Setup    Start Huginn
Suite Teardown    Stop Huginn
Test Teardown    Reset Simulator
Library    Collections
Library    RequestsLibrary
Resource    Huginn.robot

*** Test Cases ***
Simulator endpoint returns the simulator status
    [Documentation]    This test checks if the simulator endpoint returns the simulator status
    [Tags]    api    simulator
    Simulator is Paused
    Simulator DT Should Be    0.003333
    Simulation Time Should Be    0.003333

Resume the simulation after the simulator has started
    [Documentation]    This test checks if the simulator will respond to the resume command
    [Tags]    api    simulator
    Simulator is Paused
    Resume Simulation
    Sleep    2 seconds
    Simulator Is Running

Check if the simulator is reset properly
    [Documentation]    This test checks if the simulator will reset properly
    [Tags]    api    simulator
    Simulator Is Paused
    Simulation Time Should Be    0.003333
    Aircraft Should Be In The Start Location
    Resume Simulation
    Sleep    3 seconds
    Simulator Is Running
    Simulation Time Should Be Greater Than    2.0
    Reset Simulator
    Simulator Is Paused
    Simulation Time Should Be    0.003333
    Aircraft Should Be In The Start Location

Pause the simulator
    [Documentation]    This test checks if the simulator can be paused
    [Tags]    api    simulator
    Create Session    huginn_web_server  ${HUGINN_URL}
    Simulator is Paused
    Simulation Time Should Be    0.003333
    Resume Simulation
    Sleep    3 seconds
    Simulator Is Running
    Simulation Time Should Be Greater Than    2.0
    Pause Simulator
    Simulator Is Paused
    ${time_1}    Get Simulator Time
    Sleep    1 seconds
    ${time_2}    Get Simulator Time
    Should Be Equal As Numbers    ${time_1}    ${time_2}

Run a single simulation step
    [Documentation]    This test checks if the simulator can run a single step
    [Tags]    api    simulator
    Simulator is Paused
    Simulator DT Should Be    0.003333
    Simulation Time Should Be    0.003333
    ${starting_time} =    Get Simulator Time
    Execute Single Simulation Step
    Simulator is Paused
    ${current_time} =    Get Simulator Time
    Should Be Equal As Numbers    ${current_time}  ${starting_time + 0.003333}  precision=5

Run the simulator for 100 milliseconds
    [Documentation]    This test checks if the simulator can be run for 100 milliseconds
    [Tags]    api    simulator
    Simulator is Paused
    Simulator DT Should Be    0.003333
    Simulation Time Should Be    0.003333
    ${starting_time} =    Get Simulator Time
    Run The Simulation For The Given Time    0.1
    Simulator is Paused
    ${current_time} =    Get Simulator Time
    Value Close To    ${current_time}  ${starting_time + 0.1}  0.1

Start Huginn With Simulator Running
    Stop Huginn
    ${huginn_process_id} =    Start Process    huginn_start    shell=true
    Process Should Be Running    ${huginn_process_id}
    Create Session    huginn_web_server    ${HUGINN_URL}
    Wait Until Keyword Succeeds    1 min    1 sec    Get Request    huginn_web_server    /
    Simulator Is Running
    Simulator DT Should Be    0.003333

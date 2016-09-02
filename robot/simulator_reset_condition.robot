*** Settings ***
Test Setup    Start Huginn Running
Test Teardown    Stop Huginn
Library    Collections
Library    RequestsLibrary
Resource    Huginn.robot

*** Test Cases ***
Simulator Wil Start Paused After Reset
    [Documentation]    This test checks if the simulator will start paused after a reset if the start_paused command was executed
    [Tags]    api    simulator
    Simulator is Running
    Start Paused After Reset
    Reset Simulator
    Simulator Is Paused

Simulator Wil Start Running After Reset
    [Documentation]    This test checks if the simulator will start paused after a reset if the start_paused command was executed
    [Tags]    api    simulator
    Pause Simulator
    Simulator is Paused
    Start Running After Reset
    Reset Simulator
    Simulator Is Running

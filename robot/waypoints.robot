*** Settings ***
Test Setup    Start Huginn
Test Teardown    Stop Huginn
Library    Collections
Library    RequestsLibrary
Resource    Huginn.robot

*** Test Cases ***
Add A Waypoint
    [Documentation]    Add a waypoint using the REST API
    Add A Waypoint Using An API Call    waypoint_1  10.0  20.0  30.0
    ${resp} =    Get Waypoint    waypoint_1
    Is A Waypoint Retrieval Response    ${resp}
    retrieve Waypoint Response Equal    ${resp}  waypoint_1  10.0  20.0  30.0

Delete A Waypoint
    [Documentation]    Add a waypoint using the REST API
    Add A Waypoint Using An API Call    waypoint_1  10.0  20.0  30.0
    ${resp} =    Get Waypoint    waypoint_1
    Is A Waypoint Retrieval Response    ${resp}
    Retrieve Waypoint Response Equal    ${resp}  waypoint_1  10.0  20.0  30.0
    ${resp} =    Delete Waypoint    waypoint_1
    Is A Waypoint Delete Response    ${resp}
    Delete Waypoint Response Equal    ${resp}  waypoint_1  10.0  20.0  30.0
    ${resp} =    Get Waypoint    waypoint_1
    Should Be Equal As Numbers   ${resp.status_code}  404

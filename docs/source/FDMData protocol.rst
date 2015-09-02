FDMData protocol
================

The simulator uses 2 UDP ports to transmit FDM data and to receive aircraft control commands.
The FDM data are accesses from port 10300 and the aircraft controls are accessed from port 10301.

The current FDM data can be requested by sending a UDP datagram with a command code to the FDM data port. 
At the moment only one command that simply returns the data from the aircraft sensors is supported.

============   ===========
Command code   Description
============   ===========
0x01           Return the sensor data
============   ===========

The response from the simulator will be a datagram with the response code and the data. The data are float 
values in network byte order.

===============  ===========
Datagram offset  Description 
===============  ===========
0                Will be 0x01 (response ok)
1-4              Temperature
5-8              Dynamic pressure
8-12             Static pressure
13-16            Latitude
17-20            Longitude
21-24            Altitude
25-28            Airspeed
29-32            Heading
33-36            X acceleration
37-40            Y acceleration
41-44            Z acceleration
45-48            Roll rate
48-52            Pitch rate
53-56            Yaw rate
===============  ===========

The aircraft can be controlled by sending 4 float values to the controls UDP port.
These values must be in the range -1.0 to 1.0. The datagram must have the following format.

===============  ===========
Datagram offset  Description
===============  ===========
0-3              aileron
4-7              elevator
8-11             rudder
12-16            throttle
===============  ===========
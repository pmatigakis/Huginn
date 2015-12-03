FDMData protocol
================

Huginn can transmit data from the flight dynamics model to an external application
that can be used to test an autopilot and any other application that can process
flight data. By default Huginn will attempt to send data to UPD port 10302 at the localhost.

The flight data that Huginn will transmit are float values in network byte order.
The following table describes the data that are transmitted.

=====  ================  =================
Index  Variable          Unit
=====  ================  =================
0      time              seconds
1      latitude          degrees
2      longitude         degrees
3      altitude          meters
4      airspeed          meters/sec
5      heading           degrees
6      x acceleration    meters/sec^2
7      y acceleration    meters/sec^2
8      z acceleration    meters/sec^2
9      roll rate         degrees/sec
10     pitch rate        degrees/sec
11     yaw rate          degrees/sec
12     temperature       kelvin
13     static pressure   pascal
14     dynamic pressure  pascal
15     roll              degrees
16     pitch             degrees
17     engine thrust     newton
18     aileron           -1.0 to 1.0
19     elevator          -1.0 to 1.0
20     rudder            -1.0 to 1.0
21     throttle          0.0 to 1.0
=====  ================  =================
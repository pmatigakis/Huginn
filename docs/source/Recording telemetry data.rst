Recording telemetry data
========================
Huginn has a utility script that you can use to capture telemetry data that
you can use for analysis.

The huginn_telemetry.py script can be called from the console in the following way.

.. code-block:: bash

  huginn_telemetry.py telemetry.csv

The telemetry data will be saved in csv format in *telemetry.csv*. This file
will contain the following data.

=====  ================  =================
Index  Variable          Unit
=====  ================  =================
0      time              seconds
1      dt                seconds
2      running           bool
3      latitude          degrees
4      longitude         degrees
5      altitude          meters
6      airspeed          meters/sec
7      heading           degrees
8      x acceleration    meters/sec^2
9      y acceleration    meters/sec^2
10     z acceleration    meters/sec^2
11     roll rate         degrees/sec
12     pitch rate        degrees/sec
13     yaw rate          degrees/sec
14     temperature       kelvin
15     static pressure   pascal
16     dynamic pressure  pascal
17     roll              degrees
18     pitch             degrees
19     engine rpm        rounds per minute
20     engine thrust     newton
21     engine power      hp
22     aileron           float
23     elevator          float
24     rudder            float
25     throttle          float
=====  ================  =================
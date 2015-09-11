FDMData protocol
================

The simulator uses 2 UDP ports to transmit FDM data and to receive aircraft control commands.
The FDM data are accesses from port 10300 and the aircraft controls are accessed from port 10301.

The FDM data can be requested by sending a UDP datagram with a command code to the FDM data port. 
At the moment the simulator supports 8 command codes.

============   ==========================================
Command code   Description
============   ==========================================
0x00           Return the GPS data
0x01           Return the accelerometer data
0x02           Return the gyroscope data
0x03           Return the magnetometer data
0x04           Return the thermometer data
0x05           Return the pitot tube data
0x06           Return the static pressure sensor data
0x07           Return the inertial navigation system data
============   ==========================================

The response from the simulator will be a datagram with the response code, the command code
and the data. The data are float values in network byte order.

the results for the supported command codes are the following.

For the command code 0x00 the following response will be transmitted.

.. table:: GPS data

  ===============  ===================  ==========
  Datagram offset  Description          Unit
  ===============  ===================  ==========
  0                0x00 (response ok)
  1                0x00 (command code)
  2-5              Latitude             Degrees
  6-9              Longitude            Degrees
  10-13            Altitude             Meters
  14-17            Airspeed             Meters/Sec
  18-21            Heading              Degrees
  ===============  ===================  ==========

For the command code 0x01 the following response will be transmitted.

.. table:: Accelerometer data

  ===============  ===================  ============
  Datagram offset  Description          Unit
  ===============  ===================  ============
  0                0x00 (response ok)
  1                0x01 (command code)
  2-5              x axis acceleration  Meters/Sec^2
  6-9              y axis acceleration  Meters/Sec^2
  10-13            z axis acceleration  Meters/Sec^2
  ===============  ===================  ============

For the command code 0x02 the following response will be transmitted.

.. table:: Gyroscope data

  ===============  ===================  ===========
  Datagram offset  Description          Unit
  ===============  ===================  ===========
  0                0x00 (response ok)
  1                0x02 (command code)
  2-5              roll rate            Degrees/Sec 
  6-9              pitch rate           Degrees/Sec
  10-13            yaw rate             Degrees/Sec
  ===============  ===================  ===========

For the command code 0x03 the following response will be transmitted.

.. table:: Magnetometer data

  ===============  ================================
  Datagram offset  Description 
  ===============  ================================
  0                0x00 (response ok)
  1                0x03 (command code)
  2-5              not implemented yet, will be 0.0
  6-9              not implemented yet, will be 0.0
  10-13            not implemented yet, will be 0.0
  ===============  ================================

For the command code 0x04 the following response will be transmitted.

.. table:: Thermometer data

  ===============  ===================  =======
  Datagram offset  Description          Unit
  ===============  ===================  =======
  0                0x00 (response ok)
  1                0x04 (command code)
  2-5              Temperature          Celsius
  ===============  ===================  =======

For the command code 0x05 the following response will be transmitted.

.. table:: Pitot tube data

  ===============  ===================  ======
  Datagram offset  Description          Unit
  ===============  ===================  ======
  0                0x00 (response ok)
  1                0x05 (command code)
  2-5              Pressure             Pascal
  ===============  ===================  ======

For the command code 0x06 the following response will be transmitted.

.. table:: Static pressure data

  ===============  ===================  ======
  Datagram offset  Description          Unit
  ===============  ===================  ======
  0                0x00 (response ok)
  1                0x06 (command code)
  2-5              Pressure             Pascal
  ===============  ===================  ======

For the command code 0x07 the following response will be transmitted.

.. table:: Inertial navigation system data

  ===============  ===================  ===========
  Datagram offset  Description          Unit
  ===============  ===================  ===========
  0                0x00 (response ok)
  1                0x07 (command code)
  2-5              Climb rate           Meters/Sec
  6-9              Roll                 Degrees
  10-13            Pitch                Degrees
  14-17            Heading              Degrees
  18-21            Latitude             Degress
  22-25            Longitude            Degrees
  26-29            Airspeed             Meters/Sec
  30-33            Altitude             Meters
  34-37            Turn rate            Degrees/Sec
  ===============  ===================  ===========

The aircraft can be controlled by sending 4 float values to the controls UDP port.
These values must be in the range -1.0 to 1.0. The datagram must have the following format.

.. table:: Aircraft controls

  ===============  ===========
  Datagram offset  Description
  ===============  ===========
  0-3              aileron
  4-7              elevator
  8-11             rudder
  12-16            throttle
  ===============  ===========
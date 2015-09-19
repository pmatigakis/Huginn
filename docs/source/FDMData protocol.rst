FDMData protocol
================

The simulator uses 2 UDP ports to transmit FDM data and to receive aircraft control commands.
The FDM data are accessed from port 10300 and the aircraft controls are accessed from port 10301.

The FDM data can be requested by sending a UDP datagram with a request code to the FDM data port. 
At the moment the simulator supports 8 request codes.

============   ==========================================
Request code   Description
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

The response from the simulator will be a datagram with the operation result, the request code
and the data. The data are float values in network byte order.

the results for the supported request codes are the following.

For the request code 0x00 the following response will be transmitted.

.. table:: GPS data

  ===============  ===================  ==========
  Datagram offset  Description          Unit
  ===============  ===================  ==========
  0                0x00 (success)
  1                0x00 (request code)
  2-5              Latitude             Degrees
  6-9              Longitude            Degrees
  10-13            Altitude             Meters
  14-17            Airspeed             Meters/Sec
  18-21            Heading              Degrees
  ===============  ===================  ==========

For the request code 0x01 the following response will be transmitted.

.. table:: Accelerometer data

  ===============  ===================  ============
  Datagram offset  Description          Unit
  ===============  ===================  ============
  0                0x00 (success)
  1                0x01 (request code)
  2-5              x axis acceleration  Meters/Sec^2
  6-9              y axis acceleration  Meters/Sec^2
  10-13            z axis acceleration  Meters/Sec^2
  ===============  ===================  ============

For the request code 0x02 the following response will be transmitted.

.. table:: Gyroscope data

  ===============  ===================  ===========
  Datagram offset  Description          Unit
  ===============  ===================  ===========
  0                0x00 (success)
  1                0x02 (request code)
  2-5              roll rate            Degrees/Sec 
  6-9              pitch rate           Degrees/Sec
  10-13            yaw rate             Degrees/Sec
  ===============  ===================  ===========

For the request code 0x03 the following response will be transmitted.

.. table:: Magnetometer data

  ===============  ================================
  Datagram offset  Description 
  ===============  ================================
  0                0x00 (success)
  1                0x03 (request code)
  2-5              not implemented yet, will be 0.0
  6-9              not implemented yet, will be 0.0
  10-13            not implemented yet, will be 0.0
  ===============  ================================

For the request code 0x04 the following response will be transmitted.

.. table:: Thermometer data

  ===============  ===================  =======
  Datagram offset  Description          Unit
  ===============  ===================  =======
  0                0x00 (success)
  1                0x04 (request code)
  2-5              Temperature          Celsius
  ===============  ===================  =======

For the request code 0x05 the following response will be transmitted.

.. table:: Pitot tube data

  ===============  ===================  ======
  Datagram offset  Description          Unit
  ===============  ===================  ======
  0                0x00 (success)
  1                0x05 (request code)
  2-5              Pressure             Pascal
  ===============  ===================  ======

For the request code 0x06 the following response will be transmitted.

.. table:: Static pressure data

  ===============  ===================  ======
  Datagram offset  Description          Unit
  ===============  ===================  ======
  0                0x00 (success)
  1                0x06 (request code)
  2-5              Pressure             Pascal
  ===============  ===================  ======

For the request code 0x07 the following response will be transmitted.

.. table:: Inertial navigation system data

  ===============  ===================  ===========
  Datagram offset  Description          Unit
  ===============  ===================  ===========
  0                0x00 (success)
  1                0x07 (request code)
  2-5              Roll                 Degrees
  6-9              Pitch                Degrees
  10-13            Heading              Degrees
  14-17            Latitude             Degress
  18-21            Longitude            Degrees
  22-25            Airspeed             Meters/Sec
  26-29            Altitude             Meters
  ===============  ===================  ===========

The aircraft can be controlled by sending 4 float values to the controls UDP port.
These values must be in the range -1.0 to 1.0 except for the throttle that must
be in the range 0.0 to 1.0. The datagram must have the following format.

.. table:: Aircraft controls

  ===============  ===========
  Datagram offset  Description
  ===============  ===========
  0-3              aileron
  4-7              elevator
  8-11             rudder
  12-16            throttle
  ===============  ===========
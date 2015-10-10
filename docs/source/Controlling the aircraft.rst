Controlling the aircraft
========================

The default aircraft controls UDP port is 10301. The aircraft can be controlled
by sending 4 float values to this port. These values must be in the range -1.0
to 1.0 except for the throttle that must be in the range 0.0 to 1.0. The datagram
must have the following format.

.. table:: Aircraft controls

  ===============  ===========
  Datagram offset  Description
  ===============  ===========
  0-3              aileron
  4-7              elevator
  8-11             rudder
  12-16            throttle
  ===============  ===========
Controlling the aircraft
========================

The default aircraft controls UDP port is 10301. The aircraft can be controlled
by using the classes created with the protocol buffer schema that can be found in
huginn/protobuf/fdm.proto. The values of the control surfaces must be in the range -1.0
to 1.0 except for the throttle that must be in the range 0.0 to 1.0.

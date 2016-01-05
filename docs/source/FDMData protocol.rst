FDMData protocol
================

Huginn can transmit data from the flight dynamics model to an external application
that can be used to test an autopilot and any other application that can process
flight data. By default Huginn will attempt to send data to UPD port 10302 at the
localhost address.

The flight data will be encoded using Protocol Buffers. See the file
protobuf/fdm.proto for the schema used.
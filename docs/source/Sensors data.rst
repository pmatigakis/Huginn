Sensors data
============

Clients can request sensor data from Huginn by sending a request on port 10300.
The request must be encoded using protocol buffers and it must be transmitted over TCP.
The length of the request must be in the first 4 bytes of the data that are to be
sent to the server and they must be in network order.

See the file protobuf/fdm.proto for more information about the schema used.  
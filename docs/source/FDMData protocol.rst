FDMData protocol
================

Huginn can transmit data from the flight dynamics model to an external application
that can be used to test an autopilot and any other application that can process
flight data.

To send fdm data to an external application use the --fdm argument in hugin_start.py script

.. code-block:: bash

  huginn_start.py --fdm 127.0.0.1,10302,0.1 

The flight data will be encoded using Protocol Buffers. See the file
huginn/protobuf/fdm.proto for the schema used.
Starting the simulator
======================
The simulator is started with the following command.

.. code-block:: bash

    huginn_start.py
    
By default the simulator will start paused. The fdm data and controls interfaces will use 
udp ports 10300 and 10301 respectively. The RPC interface will run on port 10500 and the 
web interface will run at port 8080. 

The simulator can be controlled with the *huginn_control.py* script.

.. code-block:: bash

    # resume the simulation
    huginn_control.py resume
    
    # pause the simulator
    huginn_control.py pause
    
    # reset the simulator
    huginn_control.py reset
    
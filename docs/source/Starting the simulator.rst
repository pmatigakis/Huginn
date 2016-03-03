Starting the simulator
======================
The simulator is started using the huginn_start.py script and passing to it the
name of the aircraft you want to use. The simulator supports two aircraft. The
easystar and the Rascal. The following command will start the simulator using 
the Rascal aircraft

.. code-block:: bash

    huginn_start.py --aircraft Rascal
    
By default the simulator will start paused. The fdm data and controls interfaces will use 
udp ports 10300 and 10301 respectively. The simulator control server will run on port 10500 
and the web interface will run at port 5000. 

The simulator can be controlled with the *huginn_cli.py* script.

.. code-block:: bash

    # resume the simulation
    huginn_cli.py control resume
    
    # pause the simulator
    huginn_cli.py control pause
    
    # reset the simulator
    huginn_cli.py control reset
    
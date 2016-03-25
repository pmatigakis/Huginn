Starting the simulator
======================
The simulator is started using the huginn_start.py script and passing to it the
name of the aircraft you want to use. The simulator supports two aircraft. The
easystar and the Rascal. The following command will start the simulator using 
the Rascal aircraft

.. code-block:: bash

    huginn_start.py --aircraft Rascal
    
By default the simulator will start paused. The fdm data and controls interfaces will use 
tcp port 10300 and udp port 10301 respectively. The simulator web interface will run at port 8090. 

The simulator can be controlled with the *huginn_control.py* script.

.. code-block:: bash

    # resume the simulation
    huginn_control.py resume
    
    # pause the simulator
    huginn_control.py pause
    
    # reset the simulator
    huginn_control.py reset
    
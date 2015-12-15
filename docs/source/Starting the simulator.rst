Starting the simulator
======================
The simulator is started using the huginn_start.py script and passing to it the path
to the source code of JSBSim as well as the name of the script to run. The
following command will start the simulator using the 737 cruise script of JSBSim

.. code-block:: bash

    huginn_start.py --jsbsim /home/panagiotis/jsbsim/ --script scripts/737_cruise.xml
    
By default the simulator will start paused. The fdm data and controls interfaces will use 
udp ports 10300 and 10301 respectively. The simulator control server will run on port 10500 
and the web interface will run at port 8090. 

The simulator can be controlled with the *huginn_control.py* script.

.. code-block:: bash

    # resume the simulation
    huginn_control.py resume
    
    # pause the simulator
    huginn_control.py pause
    
    # reset the simulator
    huginn_control.py reset
    
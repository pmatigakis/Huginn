Starting the simulator
======================
The simulator is started using the huginn_start.py script and the appropriate
fdm model, aircraft and initial condition arguments. The following command
will start the simulator with the JSBSim model using the Cessna 172p aircraft at
an altitude of 1000 feet and an airspeed of  90 knots.

.. code-block:: bash

    huginn_start.py --fdmmodel jsbsim --aircraft c172p --altitude 1000.0 --airspeed 90.0
    
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
    
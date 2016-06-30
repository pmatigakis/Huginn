Starting the simulator
======================
The simulator is started using the huginn_start.py script and passing to it the
name of the aircraft you want to use. The simulator supports two aircraft. The
easystar and the Rascal. The following command will start the simulator using 
the Rascal aircraft

.. code-block:: bash

    huginn_start.py

By default the simulator will start paused. The fdm data and controls interfaces will use 
tcp port 10300 and udp port 10301 respectively. The simulator web interface will run at port 8090. 

Use the *--help* command line argument to see the available command line arguments
supported by the simulator argument

.. code-block:: bash

    panagiotis@panagiotis-laptop:~/development/projects/jsbsim/huginn/examples$ huginn_start --help

    usage: huginn_start [-h] [--web WEB] [--fdm FDM] [--controls CONTROLS]
                        [--log_level {critical,error,warning,info,debug}]
                        [--dt DT] [--log LOG] [--trim] [--latitude LATITUDE]
                        [--longitude LONGITUDE] [--altitude ALTITUDE]
                        [--airspeed AIRSPEED] [--heading HEADING]

    Huginn flight simulator

    optional arguments:
      -h, --help            show this help message and exit
      --web WEB             The web server port
      --fdm FDM             The fdm data endpoint
      --controls CONTROLS   The controls port
      --log_level {critical,error,warning,info,debug}
                            Enable debug logs
      --dt DT               the simulation timestep
      --log LOG             The output log file
      --trim                trim the aircraft
      --latitude LATITUDE   The starting latitude
      --longitude LONGITUDE
                            The starting longitude
      --altitude ALTITUDE   The starting altitude
      --airspeed AIRSPEED   The starting airspeed
      --heading HEADING     The starting heading

The simulator can be controlled with the *huginn_control.py* script.

.. code-block:: bash

    # resume the simulation
    huginn_control.py resume
    
    # pause the simulator
    huginn_control.py pause
    
    # reset the simulator
    huginn_control.py reset
    
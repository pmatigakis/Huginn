import os

from huginn_jsbsim import FGFDMExec
from huginn import configuration

def get_fdmexec():
    jsbsim_path = os.environ["JSBSIM_HOME"]
    
    fdmexec = FGFDMExec()
    
    fdmexec.set_root_dir(jsbsim_path)
    fdmexec.set_aircraft_path("/aircraft")
    fdmexec.set_engine_path("/engine")
    fdmexec.set_systems_path("/systems")

    fdmexec.set_dt(1.0/60.0)

    fdmexec.load_model("c172p")

    fdmexec.load_ic("reset00")

    fdmexec.set_property_value("ic/lat-gc-deg", configuration.INITIAL_LATITUDE)
    fdmexec.set_property_value("ic/long-gc-deg", configuration.INITIAL_LONGITUDE)
    fdmexec.set_property_value("ic/h-sl-ft", configuration.INITIAL_ALTITUDE)
    fdmexec.set_property_value("ic/vt-kts", configuration.INITIAL_AIRSPEED)
    fdmexec.set_property_value("ic/psi-true-deg", configuration.INITIAL_HEADING)

    fdmexec.set_property_value("fcs/throttle-cmd-norm", 0.65)
    fdmexec.set_property_value("fcs/mixture-cmd-norm", 0.87)
    fdmexec.set_property_value("propulsion/magneto_cmd", 3.0)
    fdmexec.set_property_value("propulsion/starter_cmd", 1.0)

    initial_condition_result = fdmexec.run_ic()

    if not initial_condition_result:
        print("Failed to run initial condition")
        exit(-1)

    running = fdmexec.run()
    while running and fdmexec.get_sim_time() < 0.1:
        fdmexec.process_message()
        fdmexec.check_incremental_hold()

        running = fdmexec.run()
    
    result = fdmexec.trim() 
    if not result:
        print("Failed to trim the aircraft")
        exit(-1)
        
    return fdmexec
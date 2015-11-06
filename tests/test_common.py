import os

from PyJSBSim import FGFDMExec
from huginn import configuration

def get_fdmexec():
    jsbsim_path = os.environ["JSBSIM_HOME"]
    
    fdmexec = FGFDMExec()
    
    fdmexec.SetRootDir(jsbsim_path)
    fdmexec.SetAircraftPath("/aircraft")
    fdmexec.SetEnginePath("/engine")
    fdmexec.SetSystemsPath("/systems")

    fdmexec.Setdt(configuration.DT)

    fdmexec.LoadModel("737")

    fdmexec.SetPropertyValue("ic/lat-gc-deg", configuration.INITIAL_LATITUDE)
    fdmexec.SetPropertyValue("ic/long-gc-deg", configuration.INITIAL_LONGITUDE)
    fdmexec.SetPropertyValue("ic/h-sl-ft", configuration.INITIAL_ALTITUDE)
    fdmexec.SetPropertyValue("ic/vt-kts", configuration.INITIAL_AIRSPEED)
    fdmexec.SetPropertyValue("ic/psi-true-deg", configuration.INITIAL_HEADING)
    fdmexec.SetPropertyValue("propulsion/set-running", -1);
    fdmexec.SetPropertyValue("simulation/do_simple_trim", 1);

    initial_condition_result = fdmexec.RunIC()

    if not initial_condition_result:
        print("Failed to run initial condition")
        exit(-1)

    running = fdmexec.Run()
    while running and fdmexec.GetSimTime() < 0.1:
        fdmexec.ProcessMessage()
        fdmexec.CheckIncrementalHold()

        running = fdmexec.Run()
        
    return fdmexec
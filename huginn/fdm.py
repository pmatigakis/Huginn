"""
The huginn.fdm module contains classes and functions that can be used to
initialize the flight dynamics model and create a model for a simulated
aircraft
"""

import logging

from PyJSBSim import FGFDMExec  # @UnresolvedImport

fdm_properties = [
    "simulation/sim-time-sec",
    "simulation/dt",
    "position/lat-gc-deg",
    "position/long-gc-deg",
    "position/h-sl-ft",
    "velocities/vtrue-kts",
    "velocities/v-north-fps",
    "velocities/v-east-fps",
    "velocities/v-down-fps",
    "velocities/u-fps",
    "velocities/v-fps",
    "velocities/w-fps",
    "velocities/p-rad_sec",
    "velocities/q-rad_sec",
    "velocities/r-rad_sec",
    "velocities/mach",
    "accelerations/a-pilot-x-ft_sec2",
    "accelerations/a-pilot-y-ft_sec2",
    "accelerations/a-pilot-z-ft_sec2",
    "accelerations/pdot-rad_sec2",
    "accelerations/qdot-rad_sec2",
    "accelerations/rdot-rad_sec2",
    "accelerations/udot-ft_sec2",
    "accelerations/vdot-ft_sec2",
    "accelerations/wdot-ft_sec2",
    "attitude/phi-rad",
    "attitude/theta-rad",
    "attitude/psi-rad",
    "attitude/roll-rad",
    "attitude/pitch-rad",
    "attitude/heading-true-rad",
    "propulsion/engine/engine-rpm",
    "propulsion/engine/thrust-lbs",
    "propulsion/engine/power-hp",
    "atmosphere/T-R",
    "atmosphere/T-sl-R",
    "atmosphere/P-psf",
    "atmosphere/P-sl-psf",
    "aero/qbar-psf",
    "fcs/elevator-cmd-norm",
    "fcs/aileron-cmd-norm",
    "fcs/rudder-cmd-norm",
    "fcs/throttle-cmd-norm"
]

fdm_data_properties = [
   "accelerations/a-pilot-x-ft_sec2",
   "accelerations/a-pilot-y-ft_sec2",
   "accelerations/a-pilot-z-ft_sec2",
   "velocities/p-rad_sec",
   "velocities/q-rad_sec",
   "velocities/r-rad_sec",
   "atmosphere/P-psf",
   "aero/qbar-psf",
   "atmosphere/T-R",
   "position/lat-gc-deg",
   "position/long-gc-deg",
   "position/h-sl-ft",
   "velocities/vtrue-kts",
   "attitude/heading-true-rad"
]

controls_properties = [
    "fcs/elevator-cmd-norm",
    "fcs/aileron-cmd-norm",
    "fcs/rudder-cmd-norm",
    "fcs/throttle-cmd-norm"
]

def create_fdmexec(jsbsim_path, aircraft_name, dt):
    """
    Initialize JSBSim and create an FGFDMExec object that will be used for
    the simulation
    """
    fdmexec = FGFDMExec()

    logging.debug("Using jsbsim data at %s", jsbsim_path)
    logging.debug("Using aircraft %s", aircraft_name)

    fdmexec.SetRootDir(jsbsim_path)
    fdmexec.SetAircraftPath("")
    fdmexec.SetEnginePath("/%s/Engines" % aircraft_name)
    fdmexec.SetSystemsPath("/%s/Systems" % aircraft_name)

    logging.debug("JSBSim dt is %f", dt)
    fdmexec.Setdt(dt)

    fdmexec.LoadModel(aircraft_name)

    engine = fdmexec.GetPropulsion().GetEngine(0)
    engine.SetRunning(True)

    fdmexec.GetFCS().SetThrottleCmd(0, 0.2)

    ic = fdmexec.GetIC()

    ic.Load("reset")

    ic_result = fdmexec.RunIC()

    if not ic_result:
        logging.error("Failed to run initial condition")
        return None

    running = fdmexec.Run()

    if not running:
        logging.error("Failed to execute initial run")
        return None

    return fdmexec

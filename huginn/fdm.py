"""
The huginn.fdm module contains classes and functions that can be used to
initialize the flight dynamics model and create a model for a simulated
aircraft
"""
import logging

from huginn import configuration
from huginn_jsbsim import FDM
from huginn.unit_conversions import convert_meters_to_feet,\
    convert_meters_per_sec_to_knots

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

class FDMBuilder(object):
    """The FDMBuilder created the flight dynamics model object that will be
    used by the simulator"""
    def __init__(self, data_path):
        self.data_path = data_path
        self.dt = configuration.DT

        self.aircraft = configuration.AIRCRAFT

        self.latitude = configuration.LATITUDE
        self.longitude = configuration.LONGITUDE
        self.altitude = configuration.ALTITUDE
        self.airspeed = configuration.AIRSPEED
        self.heading = configuration.HEADING

        self.trim = False

    def create_fdm(self):
        """Create the flight dynamics model"""
        logger = logging.getLogger("huginn")

        fdm = FDM()

        logger.debug("Using jsbsim data at %s", self.data_path)

        fdm.set_data_path(self.data_path)

        logger.debug("JSBSim dt is %f", self.dt)
        fdm.set_dt(self.dt)

        logger.debug("Using aircraft %s", self.aircraft)
        fdm.load_model(self.aircraft)

        fdm.start_engines()

        fdm.set_throttle(0.0)

        altitude_in_feet = convert_meters_to_feet(self.altitude)
        airspeed_in_knots = convert_meters_per_sec_to_knots(self.airspeed)
        fdm.set_initial_condition(self.latitude, self.longitude, altitude_in_feet, airspeed_in_knots, self.heading);

        if not fdm.run_ic():
            logger.error("Failed to run initial condition")
            return None

        if self.trim:
            trim_result = fdm.trim()

            if not trim_result:
                logger.warning("Failed to trim the aircraft")

        if not fdm.run():
            logger.error("Failed to execute initial run")
            return None

        return fdm

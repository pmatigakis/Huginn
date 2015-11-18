import logging
import os
from abc import ABCMeta, abstractmethod, abstractproperty

from PyJSBSim import FGFDMExec, FGTrim, tFull

from huginn.aircraft import Aircraft, C172P, Boing737

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

class FDMModel(object):
    """The FDMModel class is the base that defined the methods that must be
    implemented by a flight dynamics model."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_initial_conditions(self, latitude, longitude, altitude, airspeed, heading):
        pass

    @abstractmethod
    def run(self):
        """Run the flight dynamics model for one step"""
        pass

    @abstractmethod
    def reset(self):
        """Reset the flight dynamics model"""
        pass

    @abstractmethod
    def pause(self):
        """Pause the flight dynamics model"""
        pass

    @abstractmethod
    def resume(self):
        """Resume simulation"""
        pass

    @abstractmethod
    def get_aircraft(self):
        """Get the simulated aircraft model"""
        pass

    @abstractproperty
    def dt(self):
        """Get the simulation timestep"""
        pass

    @abstractproperty
    def sim_time(self):
        """Get the current simulation time"""
        pass 

class JSBSimFDMModel(FDMModel):
    """This class is a wrapper around JSBSim"""
    def __init__(self, fdmexec, aircraft):
        FDMModel.__init__(self)

        self.fdmexec = fdmexec
        self.aircraft = aircraft

    def get_aircraft(self):
        return self.aircraft

    def load_initial_conditions(self, latitude, longitude, altitude, airspeed, heading):        
        ic = self.fdmexec.GetIC()
        
        #ic.SetVtrueKtsIC(airspeed)
        ic.SetVcalibratedKtsIC(airspeed)
        ic.SetLatitudeDegIC(latitude)
        ic.SetLongitudeDegIC(longitude)
        ic.SetAltitudeASLFtIC(altitude)
        ic.SetPsiDegIC(heading)

        logging.debug("Initial conditions: latitude=%f, longitude=%f, altitude=%f, airspeed=%f, heading=%f",
                      latitude,
                      longitude,
                      altitude,
                      airspeed,
                      heading)

        return self._reset_fdmexec()

    def _reset_fdmexec(self):
        #resume simulation just in case the simulator was paused
        self.fdmexec.Resume()
            
        initial_condition_result = self.fdmexec.RunIC()

        if not initial_condition_result:
            logging.error("Failed to set the flight dynamics model's initial condition")
            return False

        if not self.fdmexec.Run():
            logging.error("Failed to make initial run")
            return False

        running = True
        while running and self.fdmexec.GetSimTime() < 0.1:
            self.fdmexec.ProcessMessage()
            self.fdmexec.CheckIncrementalHold()

            running = self.fdmexec.Run()

        return running
        
    def run(self):
        self.fdmexec.ProcessMessage()
        self.fdmexec.CheckIncrementalHold()
        
        return self.fdmexec.Run()

    def pause(self):
        self.fdmexec.Hold()

    def resume(self):
        self.fdmexec.Resume()

    def reset(self):
        logging.debug("Reseting the simulator")
        
        reset_result = self._reset_fdmexec()
        
        if not reset_result:
            return False

        engines_started = self.aircraft.start_engines()

        if not engines_started:
            logging.debug("Failed to start the engines")
            return False

        trim_result = self.aircraft.trim()
        
        if not trim_result:
            logging.debug("Failed to trim the aircraft")
        
        return trim_result


    @property
    def dt(self):
        return self.fdmexec.GetDeltaT()

    @property
    def sim_time(self):
        return self.fdmexec.GetSimTime()

def create_jsbsim_fdm_model(jsbsim_path, dt, aircraft_name):
    fdmexec = FGFDMExec()

    logging.debug("Using jsbsim data at %s", jsbsim_path)

    fdmexec.SetRootDir(jsbsim_path)
    fdmexec.SetAircraftPath("/aircraft")
    fdmexec.SetEnginePath("/engine")
    fdmexec.SetSystemsPath("/systems")

    fdmexec.Setdt(dt)

    logging.debug("Will use aircraft %s", aircraft_name)

    fdmexec.LoadModel(aircraft_name)

    if aircraft_name == "c172p":
        aircraft = C172P(fdmexec)
    elif aircraft_name == "737":
        aircraft = Boing737(fdmexec)
    else:
        return None

    #fdmexec.SetPropertyValue("propulsion/engine/set-running", 1.0)
    #fdmexec.SetPropertyValue("propulsion/engine[1]/set-running", 1.0)

    return JSBSimFDMModel(fdmexec, aircraft)

def create_fdmmodel(fdm_model_name, aircraft_name, dt):    
    if fdm_model_name == "jsbsim":
        jsbsim_path = os.environ.get("JSBSIM_HOME", None)
        
        return create_jsbsim_fdm_model(jsbsim_path, dt, aircraft_name) 
    else:
        return None

import logging
from abc import ABCMeta, abstractmethod, abstractproperty

from PyJSBSim import FGFDMExec, FGTrim, tFull

from huginn.aircraft import Aircraft

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
    def __init__(self, fdmexec):
        FDMModel.__init__(self)

        self.fdmexec = fdmexec
        self.aircraft = Aircraft(fdmexec)

    def load_initial_conditions(self, latitude, longitude, altitude, airspeed, heading):        
        ic = self.fdmexec.GetIC()
        
        ic.SetVtrueKtsIC(airspeed)
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
        
        num_engines = self.fdmexec.GetPropulsion().GetNumEngines()
        for i in range(num_engines):
            engine = self.fdmexec.GetPropulsion().GetEngine(i)
            engine.SetRunning(True)
            
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

        if running:
            trimmer = FGTrim(self.fdmexec, tFull) 
            trim_result = trimmer.DoTrim()
            
            self.fdmexec.Hold()
            
            if not trim_result:
                logging.error("Failed to trim the aircraft")
            
            return trim_result
        
    def run(self):
        self.fdmexec.ProcessMessage()
        self.fdmexec.CheckIncrementalHold()
    
        #print "engine 11 ", self.fdmexec.GetPropulsion().GetEngine(0).GetThrust()
        #print "engine 22 ", self.fdmexec.GetPropulsion().GetEngine(1).GetThrust()
    
        return self.fdmexec.Run()
    
    def reset(self):
        #TODO: The reset procedure needs to be refactored
        logging.debug("Reseting the simulator")
        
        return self._reset_fdmexec()

    def pause(self):        
        self.fdmexec.Hold()

    def resume(self):
        self.fdmexec.Resume()
    
    def get_aircraft(self):
        return self.aircraft

    @property
    def dt(self):
        return self.fdmexec.GetDeltaT()

    @property
    def sim_time(self):
        return self.fdmexec.GetSimTime()

class FDMModelCreator(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_fdm_model(self):
        pass

class JSBSimFDMModelCreator(FDMModelCreator):
    def __init__(self, jsbsim_root_path, dt):
        self.jsbsim_root_path = jsbsim_root_path
        self.dt = dt

        self.aircraft_name = "737"

    def create_fdm_model(self):
        fdmexec = FGFDMExec()
    
        logging.debug("Using jsbsim data at %s", self.jsbsim_root_path)
    
        fdmexec.SetRootDir(self.jsbsim_root_path)
        fdmexec.SetAircraftPath("/aircraft")
        fdmexec.SetEnginePath("/engine")
        fdmexec.SetSystemsPath("/systems")
    
        fdmexec.Setdt(self.dt)
    
        logging.debug("Will use aircraft %s", self.aircraft_name)

        fdmexec.LoadModel(self.aircraft_name)

        #fdmexec.SetPropertyValue("propulsion/engine/set-running", 1.0)
        #fdmexec.SetPropertyValue("propulsion/engine[1]/set-running", 1.0)

        return JSBSimFDMModel(fdmexec)

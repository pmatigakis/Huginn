import logging
from abc import ABCMeta, abstractmethod

from huginn_jsbsim import FGFDMExec

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
    def run(self):
        pass
    
    def reset(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def get_property_value(self, property_name):
        pass

    def set_property_value(self, property_name, value):
        pass

    def dt(self):
        pass 

class JSBSimFDMModel(FDMModel):
    def __init__(self, fdmexec):
        FDMModel.__init__(self)

        self.fdmexec = fdmexec
        
    def run(self):
        self.fdmexec.process_message()
        self.fdmexec.check_incremental_hold()
    
        return self.fdmexec.run()
    
    def reset(self):
        #TODO: The reset procedure needs to be refactored
        logging.debug("Reseting the simulator")
        
        #resume simulation just in case the simulator was paused
        self.fdmexec.resume()
        
        if not self.fdmexec.run_ic():
            logging.error("Failed to run initial condition")
            return

        if not self.fdmexec.run():
            logging.error("Failed to make initial run")
            return

        running = True
        while running and self.fdmexec.get_sim_time() < 0.1:
            self.fdmexec.process_message()
            self.fdmexec.check_incremental_hold()

            running = self.fdmexec.run()

        if running:
            logging.debug("Trimming the aircraft")
            
            trim_result = self.fdmexec.trim()
            
            self.fdmexec.hold()
            
            return trim_result
        else:
            logging.error("Failed to run up to 0.1 sec")

    def pause(self):        
        self.fdmexec.hold()

    def resume(self):
        self.fdmexec.resume()
    
    def get_property_value(self, property_name):
        return self.fdmexec.get_property_value(property_name)
    
    def set_property_value(self, property_name, value):
        self.fdmexec.set_property_value(property_name, value)

    def dt(self):
        return self.fdmexec.get_dt()

class FDMModelCreator(object):
    def __init__(self, dt, latitude, longitude, altitude, airspeed, heading):
        self.dt = dt

        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.airspeed = airspeed
        self.heading = heading

    def create_fdm_model(self, latitude, longitude, altitude, airspeed, heading):
        return None

class JSBSimFDMModelCreator(FDMModelCreator):
    def __init__(self, jsbsim_root_path, dt, latitude, longitude, altitude, airspeed, heading):
        FDMModelCreator.__init__(self, dt, latitude, longitude, altitude, airspeed, heading)

        self.jsbsim_root_path = jsbsim_root_path

        self.aircraft_name = "c172p"
        self.reset_file = "reset00"

    def create_fdm_model(self):
        fdmexec = FGFDMExec()
    
        logging.debug("Using jsbsim data at %s", self.jsbsim_root_path)
    
        fdmexec.set_root_dir(self.jsbsim_root_path)
        fdmexec.set_aircraft_path("/aircraft")
        fdmexec.set_engine_path("/engine")
        fdmexec.set_systems_path("/systems")
    
        fdmexec.set_dt(self.dt)
    
        logging.debug("Will use aircraft %s with reset file %s",
                      self.aircraft_name,
                      self.reset_file)

        fdmexec.load_model(self.aircraft_name)

        fdmexec.load_ic(self.reset_file)

        logging.debug("Initial conditions: latitude=%f, longitude=%f, altitude=%f, airspeed=%f, heading=%f",
                      self.latitude,
                      self.longitude,
                      self.altitude,
                      self.airspeed,
                      self.heading)

        fdmexec.set_property_value("ic/lat-gc-deg", self.latitude)
        fdmexec.set_property_value("ic/long-gc-deg", self.longitude)
        fdmexec.set_property_value("ic/h-sl-ft", self.altitude)
        fdmexec.set_property_value("ic/vt-kts", self.airspeed)
        fdmexec.set_property_value("ic/psi-true-deg", self.heading)

        #the following statements will make the aircraft to start it's engine
        fdmexec.set_property_value("fcs/throttle-cmd-norm", 0.65)
        fdmexec.set_property_value("fcs/mixture-cmd-norm", 0.87)
        fdmexec.set_property_value("propulsion/magneto_cmd", 3.0)
        fdmexec.set_property_value("propulsion/starter_cmd", 1.0)

        initial_condition_result = fdmexec.run_ic()

        if not initial_condition_result:
            logging.error("Failed to set the flight dynamics model's initial condition")
            return None

        running = fdmexec.run()

        if not running:
            logging.error("Failed to make initial flight dynamics model run")
            return None

        #run the simulation for some time before we attempt to trim the aircraft
        while running and fdmexec.get_sim_time() < 0.1:
            fdmexec.process_message()
            fdmexec.check_incremental_hold()

            running = fdmexec.run()

        #trim the aircraft
        result = fdmexec.trim()
        if not result:
            logging.error("Failed to trim the aircraft")
            return None

        return JSBSimFDMModel(fdmexec)

class Model(object):
    __metaclass__ = ABCMeta

    def __init__(self, fdm_model):
        self.fdm_model = fdm_model

    @abstractmethod
    def run(self):
        pass

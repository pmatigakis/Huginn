import logging

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
"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from huginn import configuration

class SimulatorEventListener(object):
    def simulator_reset(self, simulator):
        pass

    def simulator_paused(self, simulator):
        pass

    def simulator_resumed(self, simulator):
        pass

    def simulator_state_update(self, simulator):
        pass

class Simulator(object):
    def __init__(self, fdmexec, aircraft):
        self.aircraft = aircraft
        self.fdmexec = fdmexec
        self.sensors_port = configuration.SENSORS_PORT
        self.controls_port = configuration.CONTROLS_PORT
        self.fdm_client_address = configuration.FDM_CLIENT_ADDRESS
        self.fdm_client_port = configuration.FDM_CLIENT_PORT
        self.fdm_client_dt = configuration.FDM_CLIENT_DT
        self.listeners = []

        self.paused = True

    @property
    def dt(self):
        return self.fdmexec.GetDeltaT()

    @property
    def simulation_time(self):
        return self.fdmexec.GetSimTime()

    def add_simulator_event_listener(self, listener):
        self.listeners.append(listener)

    def remove_simulator_event_listener(self, listener):
        self.listeners.remove(listener)

    def _simulator_has_reset(self):
        for listener in self.listeners:
            listener.simulator_reset(self)

    def _simulator_has_paused(self):
        for listener in self.listeners:
            listener.simulator_paused(self)

    def _simulator_has_resumed(self):
        for listener in self.listeners:
            listener.simulator_resumed(self)

    def _simulator_has_updated(self):
        for listener in self.listeners:
            listener.simulator_state_update(self)

    def set_initial_conditions(self, latitude, longitude, altitude, airspeed, heading):
        """Set the initial aircraft conditions"""
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

    def pause(self):
        self.paused = True

        self._simulator_has_paused()

    def resume(self):
        self.paused = False

        self._simulator_has_resumed()

    def reset(self):
        logging.debug("Reseting the aircraft")
        
        self.fdmexec.Resume()

        ic_result = self.fdmexec.RunIC()

        if not ic_result:
            logging.error("Failed to run initial condition")
            return False

        self.aircraft.controls.aileron = 0.0
        self.aircraft.controls.elevator = 0.0
        self.aircraft.controls.rudder = 0.0
        self.aircraft.controls.throttle = 0.0

        running = True
        while running and self.fdmexec.GetSimTime() < self.fdmexec.GetDeltaT() * 10:
            self.fdmexec.ProcessMessage()
            self.fdmexec.CheckIncrementalHold()

            running = self.fdmexec.Run()

        if not running:
            logging.error("Failed to execute initial run")
            return False

        engine_start = self.aircraft.start_engines()

        if not engine_start:
            logging.error("Failed to start the engines")
            return False

        trim_result = self.aircraft.trim()

        if not trim_result:
            logging.error("Failed to trim the aircraft")
            return False

        self.aircraft.run()

        logging.debug("Trimmed aircraft controls: aileron %f, elevator %f, rudder: %f, throttle: %f",
                      self.aircraft.controls.aileron, self.aircraft.controls.elevator,
                      self.aircraft.controls.rudder, self.aircraft.controls.throttle)

        logging.debug("Trimmed aircraft state: roll: %f, pitch: %f, throttle: %f",
                      self.aircraft.inertial_navigation_system.roll,
                      self.aircraft.inertial_navigation_system.pitch,
                      self.aircraft.engine.thrust)

        self._simulator_has_reset()

        self.paused = True

        return True

    def run(self):
        if not self.paused:
            self.fdmexec.ProcessMessage()
            self.fdmexec.CheckIncrementalHold()

            run_result = self.fdmexec.Run()

            if run_result:
                self.aircraft.run()
            else:
                logging.error("Failed to update the fdm model")

            self._simulator_has_updated()

            return run_result

        return True

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
    def __init__(self, aircraft):
        self.aircraft = aircraft
        self.fdmexec = aircraft.fdmexec
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

    def _update_aircraft(self):
        #running = self.fdm_model.run()
        if not self.paused:
            running = self.aircraft.run()

            if not running:
                logging.error("Failed to update the flight dynamics model")

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
        reset_result = self.aircraft.reset()

        self._simulator_has_reset()

        return reset_result

    def run(self):
        if not self.paused:
            running = self.aircraft.run()

            self._simulator_has_updated()

            return running

        return True

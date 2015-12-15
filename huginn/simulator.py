"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from twisted.internet import reactor

from huginn import configuration
from huginn.unit_conversions import convert_meters_per_sec_to_knots,\
    convert_meters_to_feet

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

    def pause(self):
        self.paused = True

        self._simulator_has_paused()

    def resume(self):
        self.paused = False

        self._simulator_has_resumed()

    def reset(self):
        logging.debug("Reseting the aircraft")
        self.fdmexec.Resume()

        self.fdmexec.ResetToInitialConditions(0)

        self.aircraft.controls.aileron = 0.0
        self.aircraft.controls.elevator = 0.0
        self.aircraft.controls.rudder = 0.0
        self.aircraft.controls.throttle = 0.0

        self._simulator_has_reset()

        self.paused = True

    def run(self):
        if not self.paused:
            self.fdmexec.ProcessMessage()
            self.fdmexec.CheckIncrementalHold()

            run_result = self.fdmexec.Run()

            if run_result:
                self.aircraft.run()

                self._simulator_has_updated()
            else:
                reactor.stop()
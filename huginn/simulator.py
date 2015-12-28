"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from twisted.internet import reactor

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
    """The Simulator class is used to perform the simulation of an aircraft"""
    def __init__(self, fdmexec, aircraft):
        self.aircraft = aircraft
        self.fdmexec = fdmexec
        self.sensors_port = configuration.SENSORS_PORT
        self.controls_port = configuration.CONTROLS_PORT
        self.fdm_client_address = configuration.FDM_CLIENT_ADDRESS
        self.fdm_client_port = configuration.FDM_CLIENT_PORT
        self.fdm_client_dt = configuration.FDM_CLIENT_DT
        self.listeners = []
        self.logger = logging.getLogger("huginn")

    @property
    def dt(self):
        """The simulation time step"""
        return self.fdmexec.GetDeltaT()

    @property
    def simulation_time(self):
        """The current simulation time"""
        return self.fdmexec.GetSimTime()

    @property
    def paused(self):
        """Returns true if the simulator is paused"""
        return self.fdmexec.Holding()

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
        """Pause the simulator"""
        self.fdmexec.Hold()

        self._simulator_has_paused()

    def resume(self):
        """Resume the simulation"""
        self.fdmexec.Resume()

        self._simulator_has_resumed()

    def reset(self):
        """Reset the simulation"""
        self.logger.debug("Reseting the aircraft")
        self.fdmexec.Resume()

        self.fdmexec.ResetToInitialConditions(0)

        self.aircraft.controls.aileron = 0.0
        self.aircraft.controls.elevator = 0.0
        self.aircraft.controls.rudder = 0.0
        self.aircraft.controls.throttle = 0.2

        self.fdmexec.PrintSimulationConfiguration()

        self.fdmexec.GetPropagate().DumpState()

        running = self.fdmexec.Run()

        if not running:
            self.logger.error("Failed to reset the simulator")
            reactor.stop()  # @UndefinedVariable

        self.aircraft.run()

        self.logger.debug("Engine thrust after simulation reset %f", self.aircraft.engine.thrust)

        self._simulator_has_reset()

    def run(self):
        """Run the simulation"""
        self.fdmexec.ProcessMessage()
        self.fdmexec.CheckIncrementalHold()

        run_result = self.fdmexec.Run()

        if run_result:
            self.aircraft.run()

            self._simulator_has_updated()
        else:
            self.logger.error("The simulator has failed to run")
            reactor.stop()  # @UndefinedVariable

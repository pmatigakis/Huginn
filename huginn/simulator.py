"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from twisted.internet import reactor

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
        self.listeners = []
        self.logger = logging.getLogger("huginn")
        self.paused = False;

    @property
    def dt(self):
        """The simulation time step"""
        return self.fdmexec.GetDeltaT()

    @property
    def simulation_time(self):
        """The current simulation time"""
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
        """Pause the simulator"""
        self.paused = True

        self._simulator_has_paused()

    def resume(self):
        """Resume the simulation"""
        self.paused = False

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

    def step(self):
        """Run the simulation one time"""
        self.fdmexec.ProcessMessage()
        self.fdmexec.CheckIncrementalHold()

        run_result = self.fdmexec.Run()

        if run_result:
            self.aircraft.run()

            self._simulator_has_updated()
        else:
            self.logger.error("The simulator has failed to run")
            reactor.stop()  # @UndefinedVariable

    def run_for(self, time_to_run):
        """Run the simulation for the given time in seconds"""
        start_time = self.fdmexec.GetSimTime()
        end_time = start_time + time_to_run

        while self.fdmexec.GetSimTime() < end_time:
            self.step()

    def run(self):
        """Run the simulation"""
        if not self.paused:
            self.step()

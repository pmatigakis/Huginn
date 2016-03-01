"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from twisted.internet import reactor

class SimulatorEventListener(object):
    """The SimulatorEventListener class must be implemented by any object
    that has to notified when a simulation event is raised"""

    def simulator_reset(self, simulator):
        """The simulator has reset"""
        pass

    def simulator_paused(self, simulator):
        """The simulator has paused"""
        pass

    def simulator_resumed(self, simulator):
        """The simulator has resumed execution"""
        pass

    def simulator_state_update(self, simulator):
        """The simulator has run"""
        pass

class Simulator(object):
    """The Simulator class is used to perform the simulation of an aircraft"""

    def __init__(self, fdm, aircraft):
        self.aircraft = aircraft
        self.fdm = fdm
        self.listeners = []
        self.logger = logging.getLogger("huginn")
        self.paused = False
        self.start_trimmed = False

    @property
    def dt(self):
        """The simulation time step"""
        return self.fdm.get_dt()

    @property
    def simulation_time(self):
        """The current simulation time"""
        return self.fdm.get_simulation_time()

    def add_simulator_event_listener(self, listener):
        """Add a simulator event listener"""
        self.listeners.append(listener)

    def remove_simulator_event_listener(self, listener):
        """Remove a simulator event listener"""
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
        print "=-======reset====="

        running = self.fdm.reset_to_initial_conditions()

        if not running:
            self.logger.error("Failed to reset the simulator")
            return False

        while True:
            if not self.fdm.run():
                self.logger.error("Failed to execute initial run")
                return False

            if self.fdm.get_simulation_time() > 1.0:
                break

        self.fdm.update_aircraft(self.aircraft)

        self.logger.debug("Engine thrust after simulation reset %f", self.aircraft.engine.thrust)

        self._simulator_has_reset()

        return True

    def step(self):
        """Run the simulation one time"""
        run_result = self.fdm.run()

        if run_result:
            self.fdm.update_aircraft(self.aircraft)

            self._simulator_has_updated()

            return True
        else:
            self.logger.error("The simulator has failed to run")
            return False

    def run_for(self, time_to_run):
        """Run the simulation for the given time in seconds"""
        if time_to_run < 0.0:
            self.logger.error("Invalid simulator run time length %f", time_to_run)
            return False

        start_time = self.fdm.get_simulation_time()
        end_time = start_time + time_to_run

        while self.fdm.get_simulation_time() <= end_time:
            result = self.step()

            if not result:
                return False

        return True

    def run(self):
        """Run the simulation"""
        if not self.paused:
            result = self.step()

            if not result:
                return False

        return True

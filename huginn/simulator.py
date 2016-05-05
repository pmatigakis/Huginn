"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from huginn.aircraft import Aircraft
from huginn.fdm import FDM

class SimulationError(Exception):
    """SimulationError raised when an error occurs during simulation"""
    pass

class Simulator(object):
    """The Simulator class is used to perform the simulation of an aircraft"""

    def __init__(self, fdmexec):
        """Constructor for the Simulator object

        Arguments:
        fdm: A flight dynamics model
        aircraft: The aircraft object that will be updated every time the
                  simulator runs
        """
        self.aircraft = Aircraft(fdmexec)
        self.fdmexec = fdmexec
        self.fdm = FDM(fdmexec)
        self.logger = logging.getLogger("huginn")
        self.start_trimmed = False

    @property
    def dt(self):
        """The simulation time step"""
        return self.fdmexec.GetDeltaT()

    @property
    def simulation_time(self):
        """The current simulation time"""
        return self.fdmexec.GetSimTime()

    def pause(self):
        """Pause the simulator"""
        self.fdmexec.Hold()

    def resume(self):
        """Resume the simulation"""
        self.fdmexec.Resume()

    def is_paused(self):
        return self.fdmexec.Holding()

    def reset(self):
        """Reset the simulation"""
        self.logger.debug("Reseting the aircraft")

        self.resume()

        self.fdmexec.ResetToInitialConditions(0)

        if not self.fdmexec.RunIC():
            self.logger.error("Failed to run initial condition")
            return False

        self.aircraft.controls.aileron = 0.0
        self.aircraft.controls.elevator = 0.0
        self.aircraft.controls.rudder = 0.0

        self.logger.debug("starting the aircraft's engines")
        self.fdmexec.GetPropulsion().GetEngine(0).SetRunning(1)
        self.aircraft.controls.throttle = 0.0

#        running = self.fdm.reset_to_initial_conditions()

#        if not running:
#            self.logger.error("Failed to reset the simulator")
#            return False

#        while self.fdm.get_simulation_time() < 1.0:
        while self.fdmexec.GetSimTime() < 1.0:
            if not self.fdmexec.Run():
                self.logger.error("Failed to execute initial run")
                return False


        self.logger.debug("Engine thrust after simulation reset %f", self.aircraft.engine.thrust)

        self.pause()

        return True

    def step(self):
        """Run the simulation one time"""
        was_paused = self.is_paused()

        if was_paused:
            self.resume()

        try:
            run_result = self.fdmexec.Run()
        except:
            raise SimulationError()

        if run_result:
            if was_paused:
                self.pause()

            return True
        else:
            if was_paused:
                self.pause()

            self.logger.error("The simulator has failed to run")
            return False

    def run_for(self, time_to_run):
        """Run the simulation for the given time in seconds

        Arguments:
        time_to_run: the time in seconds that the simulator will run
        """
        if time_to_run < 0.0:
            self.logger.error("Invalid simulator run time length %f", time_to_run)
            return False

        start_time = self.fdmexec.GetSimTime()
        end_time = start_time + time_to_run

        while self.fdmexec.GetSimTime() <= end_time:
            result = self.step()

            if not result:
                return False

        return True

    def run(self):
        """Run the simulation"""
        if not self.fdmexec.Holding():
            result = self.step()

            return result

        return True

    def set_aircraft_controls(self, aileron, elevator, rudder, throttle):
        self.aircraft.controls.aileron = aileron
        self.aircraft.controls.elevator = elevator
        self.aircraft.controls.rudder = rudder
        self.aircraft.controls.throttle = throttle

    def print_simulator_state(self):
        """Show the current state of the simulation"""
        print("Simulation state")
        print("================")
        print("Time: %f seconds" % self.simulation_time)
        print("DT: %f seconds" % self.dt)
        print("Running: %s" % (not self.is_paused()))
        print("")

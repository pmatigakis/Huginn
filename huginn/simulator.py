"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

class SimulationError(Exception):
    """SimulationError raised when an error occurs during simulation"""
    pass

class Simulator(object):
    """The Simulator class is used to perform the simulation of an aircraft"""

    def __init__(self, fdm, aircraft):
        self.aircraft = aircraft
        self.fdm = fdm
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

    def pause(self):
        """Pause the simulator"""
        self.paused = True

    def resume(self):
        """Resume the simulation"""
        self.paused = False

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

        return True

    def step(self):
        """Run the simulation one time"""
        try:
            run_result = self.fdm.run()
        except:
            raise SimulationError()

        if run_result:
            self.fdm.update_aircraft(self.aircraft)

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

            return result

        return True

    def print_simulator_state(self):
        """Show the current state of the simulation"""
        print("Simulation state")
        print("================")
        print("Time: %f seconds" % self.simulation_time)
        print("DT: %f seconds" % self.dt)
        print("Running: %s" % (not self.paused))
        print("")

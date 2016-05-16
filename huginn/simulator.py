"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from huginn import configuration
from huginn.aircraft import Aircraft
from huginn.fdm import FDM, FDMBuilder

class SimulationError(Exception):
    """SimulationError raised when an error occurs during simulation"""
    pass

class SimulationBuilder(object):
    """The SimulationBuilder if a factory class that can be used to create a
    Simulator object"""
    def __init__(self, data_path):
        self.data_path = data_path
        self.dt = configuration.DT

        self.aircraft = configuration.AIRCRAFT

        self.latitude = configuration.LATITUDE
        self.longitude = configuration.LONGITUDE
        self.altitude = configuration.ALTITUDE
        self.airspeed = configuration.AIRSPEED
        self.heading = configuration.HEADING

        self.trim = False

        self.logger = logging.getLogger("huginn")

    def create_simulator(self):
        """Create the Simulator object"""
        fdm_builder = FDMBuilder(self.data_path) 
        fdm_builder.dt = self.dt
        fdm_builder.aircraft = self.aircraft
        fdm_builder.latitude = self.latitude
        fdm_builder.longitude = self.longitude
        fdm_builder.altitude = self.altitude
        fdm_builder.airspeed = self.airspeed
        fdm_builder.heading = self.heading

        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec, self.aircraft)

        aircraft.start_engines()

        if self.trim:
            self.logger.debug("trimming the aircraft")
            aircraft.trim()

        simulator = Simulator(fdmexec)
        simulator.start_trimmed = self.trim

        while simulator.simulation_time < 1.0:
            result = simulator.step()

            if not result:
                self.logger.error("Failed to execute simulator run")
                return None

        return simulator

class Simulator(object):
    """The Simulator class is used to perform the simulation of an aircraft"""

    def __init__(self, fdmexec):
        """Constructor for the Simulator object

        Arguments:
        fdmexec: A flight dynamics model
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
        """Check if the simulator is paused"""
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
        self.aircraft.controls.throttle = 0.0

        self.logger.debug("starting the aircraft's engines")
        self.aircraft.start_engines()
        
        while self.simulation_time < 1.0:
            if not self.step():
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
            self.fdmexec.ProcessMessage()
            self.fdmexec.CheckIncrementalHold()
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
        """Update the aircraft controls"""
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

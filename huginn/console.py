"""
The huginn.console module contains classes and functions that can be used to
print simulator and aircraft data on the console
"""

from huginn.simulator import SimulatorEventListener

class SimulatorStatePrinter(SimulatorEventListener):
    """The SimulatorStatePrinter class is used to print the state of the
    simulator to the console."""
    def print_simulator_state(self, simulator):
        print("Simulation state")
        print("================")
        print("Time: %f seconds" % simulator.simulation_time)
        print("DT: %f seconds" % simulator.dt)
        print("Running: %s" % (not simulator.paused))
        print("")

    def print_aircraft_state(self, aircraft):
        print("Aircraft state")
        print("")
        print("Position")
        print("========")
        print("Latitude: %f degrees" % aircraft.gps.latitude)
        print("Longitude: %f degrees" % aircraft.gps.longitude)
        print("Altitude: %f meters" % aircraft.gps.altitude)
        print("Airspeed: %f meters/second" % aircraft.gps.airspeed)
        print("Heading: %f degrees" % aircraft.gps.heading)
        print("")
        print("Orientation")
        print("===========")
        print("Roll: %f degrees" % aircraft.inertial_navigation_system.roll)
        print("Pitch: %f degrees" % aircraft.inertial_navigation_system.pitch)
        print("")
        print("Engines")
        print("=======")
        print("Thrust: %f Newtons" % aircraft.engine.thrust)
        print("")
        print("Controls")
        print("========")
        print("Aileron: %f" % aircraft.controls.aileron)
        print("Elevator: %f" % aircraft.controls.elevator)
        print("Rudder: %f" % aircraft.controls.rudder)
        print("Throttle: %f" % aircraft.controls.throttle)
        print("")

    def simulator_reset(self, simulator):
        self.print_simulator_state(simulator)
        self.print_aircraft_state(simulator.aircraft)

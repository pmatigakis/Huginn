"""
The huginn.aircraft module contains classes that wrap the jsbsim object and
and provide access to the simulated components of the aircraft.
"""
from PyJSBSim import tFull

from huginn.unit_conversions import convert_libra_to_newtons
from huginn.sensors import Sensors
from huginn.instruments import Instruments

class Controls(object):
    """The Controls class holds the aircraft control surfaces values"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def aileron(self):
        """return the aileron control value. This value will be in the range
        -1.0 to 1.0"""
        return self.fdmexec.GetFCS().GetDaCmd()

    @aileron.setter
    def aileron(self, value):
        """Set the aileron control value"""
        if value < -1.0:
            value = -1.0
        elif value > 1.0:
            value = 1.0

        self.fdmexec.GetFCS().SetDaCmd(value)

    @property
    def elevator(self):
        """return the elevator control value. This value will be in the range
        -1.0 to 1.0"""
        return self.fdmexec.GetFCS().GetDeCmd()

    @elevator.setter
    def elevator(self, value):
        """Set the elevator control value"""
        if value < -1.0:
            value = -1.0
        elif value > 1.0:
            value = 1.0

        self.fdmexec.GetFCS().SetDeCmd(value)

    @property
    def rudder(self):
        """return the rudder control value. This value will be in the range
        -1.0 to 1.0"""
        return self.fdmexec.GetFCS().GetDrCmd()

    @rudder.setter
    def rudder(self, value):
        """Set the rudder control value"""
        if value < -1.0:
            value = -1.0
        elif value > 1.0:
            value = 1.0

        self.fdmexec.GetFCS().SetDrCmd(value)

    @property
    def throttle(self):
        """return the throttle control value. This value will be in the range
        0.0 to 1.0"""
        return self.fdmexec.GetFCS().GetThrottleCmd(0)

    @throttle.setter
    def throttle(self, value):
        """Set the throttle control value"""
        if value < 0.0:
            value = 0.0
        elif value > 1.0:
            value = 1.0

        self.fdmexec.GetFCS().SetThrottleCmd(0, value)

class Engine(object):
    """The Engine class contains data about the state of the aircraft's
    engine."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def thrust(self):
        """Return the engine thrust in newtons"""
        return convert_libra_to_newtons(self.fdmexec.GetPropulsion().GetEngine(0).GetThruster().GetThrust())

    @property
    def throttle(self):
        """Return the throttle value. This will be in the range 0.0 to 1.0"""
        return self.fdmexec.GetFCS().GetThrottleCmd(0)

class Aircraft(object):
    """The Aircraft class is a wrapper around jsbsim that contains data about
    the aircraft state."""
    def __init__(self, fdmexec, aircraft_type=None):
        self.fdmexec = fdmexec
        self.type = aircraft_type
        self.sensors = Sensors(fdmexec)
        self.instruments = Instruments(fdmexec)
        self.engine = Engine(fdmexec)
        self.controls = Controls(fdmexec)

    def start_engines(self):
        """Start the aircraft engines"""
        for i in range(self.fdmexec.GetPropulsion().GetNumEngines()):
            self.fdmexec.GetPropulsion().GetEngine(i).SetRunning(1)

    def trim(self, mode=tFull):
        """Trim the aircraft"""
        self.fdmexec.DoTrim(mode)

    def print_aircraft_state(self):
        """Print the aircraft state"""
        print("Aircraft state")
        print("")
        print("Position")
        print("========")
        print("Latitude: %f degrees" % self.instruments.gps.latitude)
        print("Longitude: %f degrees" % self.instruments.gps.longitude)
        print("Altitude: %f meters" % self.instruments.gps.altitude)
        print("Airspeed: %f meters/second" % self.instruments.gps.airspeed)
        print("Heading: %f degrees" % self.instruments.gps.heading)
        print("")
        print("Orientation")
        print("===========")
        print("Roll: %f degrees" % self.inertial_navigation_system.roll)
        print("Pitch: %f degrees" % self.inertial_navigation_system.pitch)
        print("")
        print("Engines")
        print("=======")
        print("Thrust: %f Newtons" % self.engine.thrust)
        print("")
        print("Controls")
        print("========")
        print("Aileron: %f" % self.controls.aileron)
        print("Elevator: %f" % self.controls.elevator)
        print("Rudder: %f" % self.controls.rudder)
        print("Throttle: %f" % self.controls.throttle)
        print("")

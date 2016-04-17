"""
The huginn.aircraft module contains classes that wrap the jsbsim object and
and provide access to the simulated components of the aircraft.
"""
from math import degrees

from huginn.unit_conversions import convert_feet_to_meters,\
                                    convert_rankine_to_kelvin,\
                                    convert_psf_to_pascal,\
                                    convert_libra_to_newtons
from huginn.sensors import Sensors
from huginn.instruments import Instruments

class Thermometer(object):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def temperature(self):
        """return the temperature in Kelvin"""
        return convert_rankine_to_kelvin(self.fdmexec.GetAtmosphere().GetTemperature())

class PressureSensor(object):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def pressure(self):
        """Returns the pressure in Pascal"""
        return convert_psf_to_pascal(self.fdmexec.GetAtmosphere().GetPressure())

class PitotTube(object):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def pressure(self):
        """Return the pressure in pascal"""
        return convert_psf_to_pascal(self.fdmexec.GetAuxiliary().GetTotalPressure())

class InertialNavigationSystem(object):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def roll(self):
        """Return the roll angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(1)

    @property
    def pitch(self):
        """Return the pitch angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(2)

    @property
    def latitude(self):
        """Returns the latitude in degrees"""
        return self.fdmexec.GetPropagate().GetLatitudeDeg()

    @property
    def longitude(self):
        """Returns the longitude in degrees"""
        return self.fdmexec.GetPropagate().GetLongitudeDeg()

    @property
    def altitude(self):
        """Returns the altitude in meters"""
        return self.fdmexec.GetPropagate().GetAltitudeASLmeters()

    @property
    def airspeed(self):
        """Returns the airspeed in meters per second"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetVtrueFPS())

    @property
    def heading(self):
        """Returns the heading in degrees"""
        return degrees(self.fdmexec.GetPropagate().GetEuler(3))

class Controls(object):
    """The Controls class holds the aircraft control surfaces values"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def aileron(self):
        """return the aileron control value. This value will be in the range -1.0 to 1.0"""
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
        """return the elevator control value. This value will be in the range -1.0 to 1.0"""
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
        """return the rudder control value. This value will be in the range -1.0 to 1.0"""
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
        """return the throttle control value. This value will be in the range 0.0 to 1.0"""
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
    """The Engine class contains data about the state of the aircraft's engine."""
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
        self.thermometer = Thermometer(fdmexec)
        self.pressure_sensor = PressureSensor(fdmexec)
        self.pitot_tube = PitotTube(fdmexec)
        self.inertial_navigation_system = InertialNavigationSystem(fdmexec)
        self.engine = Engine(fdmexec)
        self.controls = Controls(fdmexec)

    def print_aircraft_state(self):
        """Print the aircraft state"""
        print("Aircraft state")
        print("")
        print("Position")
        print("========")
        print("Latitude: %f degrees" % self.intruments.gps.latitude)
        print("Longitude: %f degrees" % self.intruments.gps.longitude)
        print("Altitude: %f meters" % self.intruments.gps.altitude)
        print("Airspeed: %f meters/second" % self.intruments.gps.airspeed)
        print("Heading: %f degrees" % self.intruments.gps.heading)
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

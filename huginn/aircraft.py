"""
The huginn.aircraft module contains classes that wrap the jsbsim object and
and provide access to the simulated components of the aircraft.
"""

class GPS(object):
    """The GPS class simulates the aircraft's GPS system."""
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

class Accelerometer(object):
    """The Accelerometer class returns the acceleration measures on the body
    frame."""
    def __init__(self):
        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0

class Gyroscope(object):
    """The Gyroscope class contains the angular velocities measured on the body axis."""
    def __init__(self):
        self.roll_rate = 0.0
        self.pitch_rate = 0.0
        self.yaw_rate = 0.0

class Thermometer(object):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self):
        self.temperature = 0.0

class PressureSensor(object):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self):
        self.pressure = 0.0

class PitotTube(object):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self):
        self.pressure = 0.0

class InertialNavigationSystem(object):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self):
        self.roll = 0.0
        self.pitch = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

class Controls(object):
    """The Controls class holds the aircraft control surfaces values"""
    def __init__(self):
        self.aileron = 0.0
        self.elevator = 0.0
        self.rudder = 0.0
        self.throttle = 0.0

class Engine(object):
    """The Engine class contains data about the state of the aircraft's engine."""
    def __init__(self):
        self.thrust = 0.0
        self.throttle = 0.0

class Aircraft(object):
    """The Aircraft class is a wrapper around jsbsim that contains data about
    the aircraft state."""
    def __init__(self, aircraft_type=None):
        self._fdmexec_state_listeners = []

        self.type = aircraft_type
        self.gps = GPS()
        self.accelerometer = Accelerometer()
        self.gyroscope = Gyroscope()
        self.thermometer = Thermometer()
        self.pressure_sensor = PressureSensor()
        self.pitot_tube = PitotTube()
        self.inertial_navigation_system = InertialNavigationSystem()
        self.engine = Engine()
        self.controls = Controls()

    def print_aircraft_state(self):
        """Print the aircraft state"""
        print("Aircraft state")
        print("")
        print("Position")
        print("========")
        print("Latitude: %f degrees" % self.gps.latitude)
        print("Longitude: %f degrees" % self.gps.longitude)
        print("Altitude: %f meters" % self.gps.altitude)
        print("Airspeed: %f meters/second" % self.gps.airspeed)
        print("Heading: %f degrees" % self.gps.heading)
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

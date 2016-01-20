"""
The huginn.aircraft module contains classes that wrap the jsbsim object and
and provide access to the simulated components of the aircraft.
"""

from abc import ABCMeta, abstractmethod
from math import degrees

from huginn.unit_conversions import (convert_feet_to_meters,
                                     convert_rankine_to_kelvin,
                                     convert_psf_to_pascal,
                                     convert_libra_to_newtons)

class Component(object):
    """The Component class is the base for every part that simulates a part
    of an aircraft."""
    __metaclass__ = ABCMeta

    def __init__(self, fdm):
        self.fdm = fdm

    @abstractmethod
    def run(self):
        """Update the component using data from JSBSim."""
        pass

class GPS(Component):
    """The GPS class simulates the aircraft's GPS system."""
    def __init__(self, fdm):
        Component.__init__(self, fdm)

        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.latitude = self.fdm.get_latitude()
        self.longitude = self.fdm.get_longitude()

        self.altitude = self.fdm.get_altitude()

        airspeed_in_fps = self.fdm.get_airspeed()
        self.airspeed = convert_feet_to_meters(airspeed_in_fps)
        #self.airspeed = convert_knots_to_meters_per_sec(airspeed_in_knots)

        self.heading = degrees(self.fdm.get_heading())

class Accelerometer(Component):
    """The Accelerometer class returns the acceleration measures on the body
    frame."""
    def __init__(self, fdm):
        Component.__init__(self, fdm)

        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.x_acceleration = convert_feet_to_meters(self.fdm.get_x_acceleration())

        self.y_acceleration = convert_feet_to_meters(self.fdm.get_y_acceleration())

        self.z_acceleration = convert_feet_to_meters(self.fdm.get_z_acceleration())

class Gyroscope(Component):
    """The Gyroscope class contains the angular velocities measured on the body axis."""
    def __init__(self, fdm):
        Component.__init__(self, fdm)

        self.roll_rate = 0.0
        self.pitch_rate = 0.0
        self.yaw_rate = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.roll_rate = degrees(self.fdm.get_roll_rate())

        self.pitch_rate = degrees(self.fdm.get_pitch_rate())

        self.yaw_rate = degrees(self.fdm.get_yaw_rate())

class Thermometer(Component):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self, fdm):
        Component.__init__(self, fdm)

        self.temperature = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        #self.temperature = self.fdmexec.GetAuxiliary().GetTAT_C()
        self.temperature = convert_rankine_to_kelvin(self.fdm.get_temperature())

class PressureSensor(Component):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self, fdm):
        Component.__init__(self, fdm)

        self.pressure = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.pressure = convert_psf_to_pascal(self.fdm.get_pressure())

class PitotTube(Component):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self, fdm):
        Component.__init__(self, fdm)

        self.pressure = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.pressure = convert_psf_to_pascal(self.fdm.get_total_pressure())

class InertialNavigationSystem(Component):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self, fdm):
        Component.__init__(self, fdm)

        self.roll = 0.0
        self.pitch = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.roll = self.fdm.get_roll()

        self.pitch = self.fdm.get_pitch()

        self.heading = degrees(self.fdm.get_heading())

        self.latitude = self.fdm.get_latitude()
        self.longitude = self.fdm.get_longitude()

        airspeed_in_fps = self.fdm.get_airspeed()
        self.airspeed = convert_feet_to_meters(airspeed_in_fps)

        self.altitude = self.fdm.get_altitude()

class Controls(object):
    """The Controls class holds the aircraft control surfaces values"""
    def __init__(self, fdm):
        self.fdm = fdm

    @property
    def aileron(self):
        """The aileron deflection."""
        return self.fdm.get_aileron()

    @aileron.setter
    def aileron(self, value):
        """Set the aileron deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdm.set_aileron(value)

    @property
    def elevator(self):
        """The elevator deflection."""
        return self.fdm.get_elevator()

    @elevator.setter
    def elevator(self, value):
        """Set the elevator deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdm.set_elevator(value)

    @property
    def rudder(self):
        """The rudder deflection."""
        return self.fdm.get_rudder()

    @rudder.setter
    def rudder(self, value):
        """Set the rudder deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdm.set_rudder(value)

    @property
    def throttle(self):
        """The throttle setting."""
        return self.fdm.get_throttle()

    @throttle.setter
    def throttle(self, value):
        """Set the engine's throttle position.

        This value must be between 0.0 and 1.0."""
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0

        self.fdm.set_throttle(value)

class Engine(Component):
    """The Engine class contains data about the state of the aircraft's engine."""
    def __init__(self, fdm):
        Component.__init__(self, fdm)

        self.thrust = 0.0
        self.throttle = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.thrust = convert_libra_to_newtons(self.fdm.get_thrust())

        self.throttle = self.fdm.get_throttle()

class Aircraft(object):
    """The Aircraft class is a wrapper around jsbsim that contains data about
    the aircraft state."""
    def __init__(self, fdm):
        self.fdm = fdm

        self._fdmexec_state_listeners = []

        self.gps = GPS(fdm)
        self.accelerometer = Accelerometer(fdm)
        self.gyroscope = Gyroscope(fdm)
        self.thermometer = Thermometer(fdm)
        self.pressure_sensor = PressureSensor(fdm)
        self.pitot_tube = PitotTube(fdm)
        self.inertial_navigation_system = InertialNavigationSystem(fdm)
        self.engine = Engine(fdm)
        self.controls = Controls(fdm)

    def run(self):
        """Update the aircraft state using the data from JSBSim"""
        self.gps.run()
        self.accelerometer.run()
        self.gyroscope.run()
        self.thermometer.run()
        self.pressure_sensor.run()
        self.pitot_tube.run()
        self.inertial_navigation_system.run()
        self.engine.run()

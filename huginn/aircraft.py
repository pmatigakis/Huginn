"""
The huginn.aircraft module contains classes that wrap the jsbsim object and
return data about the simulation.
"""

from math import degrees

from huginn.unit_conversions import (convert_feet_to_meters,
                                     convert_knots_to_meters_per_sec,
                                     convert_feet_sec_squared_to_meters_sec_squared,
                                     convert_radians_sec_to_degrees_sec,
                                     convert_rankine_to_kelvin,
                                     convert_psf_to_pascal,
                                     convert_pounds_to_newtons)

class GPS(object):
    """The GPS class simulates the aircraft's GPS system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def latitude(self):
        """The aircraft's latitude in degrees."""
        return self.fdmexec.get_property_value("position/lat-gc-deg")

    @property
    def longitude(self):
        """The aircraft's longitude in degrees."""
        return self.fdmexec.get_property_value("position/long-gc-deg")

    @property
    def altitude(self):
        """Return the altitude in meters"""
        altitude_in_feet = self.fdmexec.get_property_value("position/h-sl-ft")
        altitude_in_meters = convert_feet_to_meters(altitude_in_feet)

        return altitude_in_meters

    @property
    def airspeed(self):
        """Return the true airspeed in meters/sec"""
        airspeed_in_knots = self.fdmexec.get_property_value("velocities/vtrue-kts")
        airspeed_in_meters_per_sec = convert_knots_to_meters_per_sec(airspeed_in_knots)

        return airspeed_in_meters_per_sec

    @property
    def heading(self):
        """Return the true heading in degrees"""
        heading_in_radians = self.fdmexec.get_property_value("attitude/heading-true-rad")
        heading_in_degrees = degrees(heading_in_radians)

        return heading_in_degrees

class Accelerometer(object):
    """The Accelerometer class returns the acceleration measures on the body frame."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def x_acceleration(self):
        """Return the acceleration on the x axis in meters/sex^2"""
        acceleration_in_feet_per_sec = self.fdmexec.get_property_value("accelerations/a-pilot-x-ft_sec2")

        return convert_feet_sec_squared_to_meters_sec_squared(acceleration_in_feet_per_sec)

    @property
    def y_acceleration(self):
        """Return the acceleration on the y axis in meters/sex^2"""
        acceleration_in_feet_per_sec = self.fdmexec.get_property_value("accelerations/a-pilot-y-ft_sec2")

        return convert_feet_sec_squared_to_meters_sec_squared(acceleration_in_feet_per_sec)

    @property
    def z_acceleration(self):
        """Return the acceleration on the z axis in meters/sex^2"""
        acceleration_in_feet_per_sec = self.fdmexec.get_property_value("accelerations/a-pilot-z-ft_sec2")

        return convert_feet_sec_squared_to_meters_sec_squared(acceleration_in_feet_per_sec)

class Gyroscope(object):
    """The Gyroscope class contains the angular velocities measured on the body axis."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def roll_rate(self):
        """The roll rate in rad/sec."""
        roll_rate_in_radians_sec = self.fdmexec.get_property_value("velocities/p-rad_sec")

        roll_rate_in_degress_sec = convert_radians_sec_to_degrees_sec(roll_rate_in_radians_sec)

        return roll_rate_in_degress_sec

    @property
    def pitch_rate(self):
        """The pitch rate in rad/sec."""
        pitch_rate_in_radians_sec = self.fdmexec.get_property_value("velocities/q-rad_sec")

        pitch_rate_in_degress_sec = convert_radians_sec_to_degrees_sec(pitch_rate_in_radians_sec)

        return pitch_rate_in_degress_sec

    @property
    def yaw_rate(self):
        """The yaw rate in rad/sec."""
        yaw_rate_in_radians_sec = self.fdmexec.get_property_value("velocities/r-rad_sec")

        yaw_rate_in_degress_sec = convert_radians_sec_to_degrees_sec(yaw_rate_in_radians_sec)

        return yaw_rate_in_degress_sec

class Thermometer(object):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def temperature(self):
        """The atmosphere temperature in Kelvin."""
        temperature_in_rankine = self.fdmexec.get_property_value("atmosphere/T-R")

        temperature_in_kelvin = convert_rankine_to_kelvin(temperature_in_rankine)

        return temperature_in_kelvin

class PressureSensor(object):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def pressure(self):
        """The static pressure in Pascal."""
        pressure_in_psf = self.fdmexec.get_property_value("atmosphere/P-psf")

        pressure_in_pascal = convert_psf_to_pascal(pressure_in_psf)

        return pressure_in_pascal

class PitotTube(object):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def pressure(self):
        """The dynamic pressure in Pascal."""
        pressure_in_psf = self.fdmexec.get_property_value("aero/qbar-psf")

        pressure_in_pascal = convert_psf_to_pascal(pressure_in_psf)

        return pressure_in_pascal

class InertialNavigationSystem(object):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def roll(self):
        """The aircraft's roll angle in degrees."""
        roll_in_radians = self.fdmexec.get_property_value("attitude/roll-rad")

        roll_in_degrees = degrees(roll_in_radians)

        return roll_in_degrees

    @property
    def pitch(self):
        """The aircraft's pitch angle in degrees."""
        pitch_in_radians = self.fdmexec.get_property_value("attitude/pitch-rad")

        pitch_in_degrees = degrees(pitch_in_radians)

        return pitch_in_degrees

    @property
    def heading(self):
        """The aircraft's heading angle in degrees."""
        yaw_in_radians = self.fdmexec.get_property_value("attitude/heading-true-rad")

        yaw_in_degrees = degrees(yaw_in_radians)

        return yaw_in_degrees

    @property
    def latitude(self):
        """The aircraft's latitude in degrees."""
        return self.fdmexec.get_property_value("position/lat-gc-deg")

    @property
    def longitude(self):
        """The aircraft's longitude in degrees."""
        return self.fdmexec.get_property_value("position/long-gc-deg")

    @property
    def airspeed(self):
        """The aircraft's true aircraft's airspeedd in meters/sec"""
        airspeed_in_knots = self.fdmexec.get_property_value("velocities/vtrue-kts")
        airspeed_in_meters_per_sec = convert_knots_to_meters_per_sec(airspeed_in_knots)

        return airspeed_in_meters_per_sec

    @property
    def altitude(self):
        """The aircraft's altitude in meters."""
        altitude_in_feet = self.fdmexec.get_property_value("position/h-sl-ft")
        altitude_in_meters = convert_feet_to_meters(altitude_in_feet)

        return altitude_in_meters

class Controls(object):
    """The Controls class holds the aircraft control surfaces values"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def aileron(self):
        """The aileron deflection."""
        return self.fdmexec.get_property_value("fcs/aileron-cmd-norm")

    @aileron.setter
    def aileron(self, value):
        """Set the aileron deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.set_property_value("fcs/aileron-cmd-norm", value)

    @property
    def elevator(self):
        """The elevator deflection."""
        return self.fdmexec.get_property_value("fcs/elevator-cmd-norm")

    @elevator.setter
    def elevator(self, value):
        """Set the elevator deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.set_property_value("fcs/elevator-cmd-norm", value)

    @property
    def rudder(self):
        """The rudder deflection."""
        return self.fdmexec.get_property_value("fcs/rudder-cmd-norm")

    @rudder.setter
    def rudder(self, value):
        """Set the rudder deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.set_property_value("fcs/rudder-cmd-norm", value)

class Engine(object):
    """The Engine class contains data about the state of the aircraft's engine."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def rpm(self):
        """The engine's rounds per minute."""
        return self.fdmexec.get_property_value("propulsion/engine/engine-rpm")

    @property
    def thrust(self):
        """The engine's thrust in Newtons."""
        thrust_in_lbs = self.fdmexec.get_property_value("propulsion/engine/thrust-lbs")

        return convert_pounds_to_newtons(thrust_in_lbs)

    @property
    def power(self):
        """The engine's horsepower."""
        return self.fdmexec.get_property_value("propulsion/engine/power-hp")

    @property
    def throttle(self):
        """The throttle setting."""
        return self.fdmexec.get_property_value("fcs/throttle-cmd-norm")

    @throttle.setter
    def throttle(self, value):
        """Set the engine's throttle position.

        This value must be between 0.0 and 1.0."""
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0

        self.fdmexec.set_property_value("fcs/throttle-cmd-norm", value)

class Aircraft(object):
    """The Aircraft class is a wrapper around jsbsim that contains data about
    the aircraft state."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.gps = GPS(fdmexec)
        self.accelerometer = Accelerometer(fdmexec)
        self.gyroscope = Gyroscope(fdmexec)
        self.thermometer = Thermometer(fdmexec)
        self.pressure_sensor = PressureSensor(fdmexec)
        self.pitot_tube = PitotTube(fdmexec)
        self.inertial_navigation_system = InertialNavigationSystem(fdmexec)
        self.engine = Engine(fdmexec)
        self.controls = Controls(fdmexec)

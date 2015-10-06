"""
The huginn.aircraft module contains classes that wrap the jsbsim object and
return data about the simulation.
"""

import logging
from math import degrees

from huginn.unit_conversions import (convert_feet_to_meters,
                                     convert_knots_to_meters_per_sec,
                                     convert_feet_sec_squared_to_meters_sec_squared,
                                     convert_radians_sec_to_degrees_sec,
                                     convert_rankine_to_kelvin,
                                     convert_psf_to_pascal,
                                     convert_pounds_to_newtons)

from huginn.fdm import Model

class GPS(Model):
    """The GPS class simulates the aircraft's GPS system."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

    def run(self):
        self.latitude = self.fdm_model.get_property_value("position/lat-gc-deg")
        self.longitude = self.fdm_model.get_property_value("position/long-gc-deg")
        
        altitude_in_feet = self.fdm_model.get_property_value("position/h-sl-ft")
        self.altitude = convert_feet_to_meters(altitude_in_feet) 

        airspeed_in_knots = self.fdm_model.get_property_value("velocities/vtrue-kts")
        self.airspeed = convert_knots_to_meters_per_sec(airspeed_in_knots)

        heading_in_radians = self.fdm_model.get_property_value("attitude/heading-true-rad")
        self.heading = degrees(heading_in_radians)

        return True

class Accelerometer(Model):
    """The Accelerometer class returns the acceleration measures on the body frame."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0

    def run(self):
        x_acceleration_in_feet_per_sec = self.fdm_model.get_property_value("accelerations/a-pilot-x-ft_sec2")
        self.x_acceleration = convert_feet_sec_squared_to_meters_sec_squared(x_acceleration_in_feet_per_sec)

        y_acceleration_in_feet_per_sec = self.fdm_model.get_property_value("accelerations/a-pilot-y-ft_sec2")
        self.y_acceleration = convert_feet_sec_squared_to_meters_sec_squared(y_acceleration_in_feet_per_sec)

        z_acceleration_in_feet_per_sec = self.fdm_model.get_property_value("accelerations/a-pilot-z-ft_sec2")
        self.z_acceleration = convert_feet_sec_squared_to_meters_sec_squared(z_acceleration_in_feet_per_sec)

        return True

class Gyroscope(Model):
    """The Gyroscope class contains the angular velocities measured on the body axis."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.roll_rate = 0.0
        self.pitch_rate = 0.0
        self.yaw_rate = 0.0

    def run(self):
        roll_rate_in_radians_sec = self.fdm_model.get_property_value("velocities/p-rad_sec")
        self.roll_rate = convert_radians_sec_to_degrees_sec(roll_rate_in_radians_sec)

        pitch_rate_in_radians_sec = self.fdm_model.get_property_value("velocities/q-rad_sec")
        self.pitch_rate = convert_radians_sec_to_degrees_sec(pitch_rate_in_radians_sec)

        yaw_rate_in_radians_sec = self.fdm_model.get_property_value("velocities/r-rad_sec")
        self.yaw_rate = convert_radians_sec_to_degrees_sec(yaw_rate_in_radians_sec)

        return True

class Thermometer(Model):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.temperature = 0.0

    def run(self):
        temperature_in_rankine = self.fdm_model.get_property_value("atmosphere/T-R")

        self.temperature = convert_rankine_to_kelvin(temperature_in_rankine)

        return True

class PressureSensor(Model):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.pressure = 0.0

    def run(self):
        pressure_in_psf = self.fdm_model.get_property_value("atmosphere/P-psf")

        self.pressure = convert_psf_to_pascal(pressure_in_psf)

        return True

class PitotTube(Model):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.pressure = 0.0

    def run(self):
        pressure_in_psf = self.fdm_model.get_property_value("aero/qbar-psf")

        self.pressure = convert_psf_to_pascal(pressure_in_psf)

        return True

class InertialNavigationSystem(Model):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.roll = 0.0
        self.pitch = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

    def run(self):
        roll_in_radians = self.fdm_model.get_property_value("attitude/roll-rad")
        self.roll = degrees(roll_in_radians)
        
        pitch_in_radians = self.fdm_model.get_property_value("attitude/pitch-rad")
        self.pitch = degrees(pitch_in_radians)

        yaw_in_radians = self.fdm_model.get_property_value("attitude/heading-true-rad")
        self.heading = degrees(yaw_in_radians)

        self.latitude = self.fdm_model.get_property_value("position/lat-gc-deg")
        self.longitude = self.fdm_model.get_property_value("position/long-gc-deg")
        
        airspeed_in_knots = self.fdm_model.get_property_value("velocities/vtrue-kts")
        self.airspeed = convert_knots_to_meters_per_sec(airspeed_in_knots)

        altitude_in_feet = self.fdm_model.get_property_value("position/h-sl-ft")
        self.altitude = convert_feet_to_meters(altitude_in_feet)

        return True

class Controls(object):
    """The Controls class holds the aircraft control surfaces values"""
    def __init__(self, fdm_model):
        self.fdm_model = fdm_model

    @property
    def aileron(self):
        """The aileron deflection."""
        return self.fdm_model.get_property_value("fcs/aileron-cmd-norm")

    @aileron.setter
    def aileron(self, value):
        """Set the aileron deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdm_model.set_property_value("fcs/aileron-cmd-norm", value)

    @property
    def elevator(self):
        """The elevator deflection."""
        return self.fdm_model.get_property_value("fcs/elevator-cmd-norm")

    @elevator.setter
    def elevator(self, value):
        """Set the elevator deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdm_model.set_property_value("fcs/elevator-cmd-norm", value)

    @property
    def rudder(self):
        """The rudder deflection."""
        return self.fdm_model.get_property_value("fcs/rudder-cmd-norm")

    @rudder.setter
    def rudder(self, value):
        """Set the rudder deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdm_model.set_property_value("fcs/rudder-cmd-norm", value)

    @property
    def throttle(self):
        """The throttle setting."""
        return self.fdm_model.get_property_value("fcs/throttle-cmd-norm")

    @throttle.setter
    def throttle(self, value):
        """Set the engine's throttle position.

        This value must be between 0.0 and 1.0."""
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0

        self.fdm_model.set_property_value("fcs/throttle-cmd-norm", value)

class Engine(Model):
    """The Engine class contains data about the state of the aircraft's engine."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.rpm = 0.0
        self.thrust = 0.0
        self.power = 0.0
        self.throttle = 0.0

    def run(self):
        self.rpm = self.fdm_model.get_property_value("propulsion/engine/engine-rpm")

        thrust_in_lbs = self.fdm_model.get_property_value("propulsion/engine/thrust-lbs")
        self.thrust = convert_pounds_to_newtons(thrust_in_lbs)

        self.power = self.fdm_model.get_property_value("propulsion/engine/power-hp")

        self.throttle = self.fdm_model.get_property_value("fcs/throttle-cmd-norm")

        return True

class Aircraft(Model):
    """The Aircraft class is a wrapper around jsbsim that contains data about
    the aircraft state."""
    def __init__(self, fdm_model):
        Model.__init__(self, fdm_model)

        self.gps = GPS(fdm_model)
        self.accelerometer = Accelerometer(fdm_model)
        self.gyroscope = Gyroscope(fdm_model)
        self.thermometer = Thermometer(fdm_model)
        self.pressure_sensor = PressureSensor(fdm_model)
        self.pitot_tube = PitotTube(fdm_model)
        self.inertial_navigation_system = InertialNavigationSystem(fdm_model)
        self.engine = Engine(fdm_model)
        self.controls = Controls(fdm_model)

    def run(self):
        run_result = self.fdm_model.run()
        
        if run_result:
            self.gps.run()
            self.accelerometer.run()
            self.gyroscope.run()
            self.thermometer.run()
            self.pressure_sensor.run()
            self.pitot_tube.run()
            self.inertial_navigation_system.run()
            self.engine.run()
        else:
            logging.error("Failed to update the fdm model")
        
        return run_result
        
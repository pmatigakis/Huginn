from math import degrees

from huginn.unit_conversions import convert_feet_to_meters, convert_knots_to_meters_per_sec
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared, convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal

class Sensor(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

class GPS(Sensor):
    def __init__(self, fdmexec):
        Sensor.__init__(self, fdmexec)
    
    @property
    def latitude(self):
        return self.fdmexec.get_property_value("position/lat-gc-deg")
    
    @property
    def longitude(self):
        return self.fdmexec.get_property_value("position/long-gc-deg")
    
    @property
    def altitude(self):
        altitude_in_feet = self.fdmexec.get_property_value("position/h-sl-ft")
        altitude_in_meters = convert_feet_to_meters(altitude_in_feet)
        
        return altitude_in_meters
    
    @property
    def airspeed(self):
        airspeed_in_knots = self.fdmexec.get_property_value("velocities/vtrue-kts")
        airspeed_in_meters_per_sec = convert_knots_to_meters_per_sec(airspeed_in_knots)
        
        return airspeed_in_meters_per_sec
    
    @property
    def heading(self):
        heading_in_radians = self.fdmexec.get_property_value("attitude/heading-true-rad")
        heading_in_degrees = degrees(heading_in_radians)
        
        return heading_in_degrees
    
class Accelerometer(Sensor):
    def __init__(self, fdmexec):
        Sensor.__init__(self, fdmexec)

    @property        
    def x_acceleration(self):
        acceleration_in_feet_per_sec = self.fdmexec.get_property_value("accelerations/a-pilot-x-ft_sec2")
        
        return convert_feet_sec_squared_to_meters_sec_squared(acceleration_in_feet_per_sec)
    
    @property        
    def y_acceleration(self):
        acceleration_in_feet_per_sec = self.fdmexec.get_property_value("accelerations/a-pilot-y-ft_sec2")
        
        return convert_feet_sec_squared_to_meters_sec_squared(acceleration_in_feet_per_sec)
    
    @property        
    def z_acceleration(self):
        acceleration_in_feet_per_sec = self.fdmexec.get_property_value("accelerations/a-pilot-z-ft_sec2")
        
        return convert_feet_sec_squared_to_meters_sec_squared(acceleration_in_feet_per_sec)
    
class Gyroscope(Sensor):
    def __init__(self, fdmexec):
        Sensor.__init__(self, fdmexec)

    @property
    def roll_rate(self):
        roll_rate_in_radians_sec = self.fdmexec.get_property_value("velocities/p-rad_sec")
        
        roll_rate_in_degress_sec = convert_radians_sec_to_degrees_sec(roll_rate_in_radians_sec)
        
        return roll_rate_in_degress_sec
    
    @property
    def pitch_rate(self):
        pitch_rate_in_radians_sec = self.fdmexec.get_property_value("velocities/q-rad_sec")
        
        pitch_rate_in_degress_sec = convert_radians_sec_to_degrees_sec(pitch_rate_in_radians_sec)
        
        return pitch_rate_in_degress_sec

    @property
    def yaw_rate(self):
        yaw_rate_in_radians_sec = self.fdmexec.get_property_value("velocities/r-rad_sec")
        
        yaw_rate_in_degress_sec = convert_radians_sec_to_degrees_sec(yaw_rate_in_radians_sec)
        
        return yaw_rate_in_degress_sec

class Thermometer(Sensor):
    def __init__(self, fdmexec):
        Sensor.__init__(self, fdmexec)
    
    @property
    def temperature(self):
        temperature_in_rankine = self.fdmexec.get_property_value("atmosphere/T-R")
        
        temperature_in_Kelvin = convert_rankine_to_kelvin(temperature_in_rankine)
        
        return temperature_in_Kelvin
    
class PressureSensor(Sensor):
    def __init__(self, fdmexec):
        Sensor.__init__(self, fdmexec)
    
    @property
    def pressure(self):
        pressure_in_psf = self.fdmexec.get_property_value("atmosphere/P-psf")
        
        pressure_in_pascal = convert_psf_to_pascal(pressure_in_psf)
        
        return pressure_in_pascal
    
class PitotTube(Sensor):
    def __init__(self, fdmexec):
        Sensor.__init__(self, fdmexec)
    
    @property
    def pressure(self):
        pressure_in_psf = self.fdmexec.get_property_value("aero/qbar-psf")
        
        pressure_in_pascal = convert_psf_to_pascal(pressure_in_psf)
        
        return pressure_in_pascal
    
class AttitudeIndicator(Sensor):
    def __init__(self, fdmexec):
        Sensor.__init__(self, fdmexec)
        
    @property
    def roll(self):
        roll_in_radians = self.fdmexec.get_property_value("attitude/roll-rad")
        
        roll_in_degrees = degrees(roll_in_radians)
        
        return roll_in_degrees
    
    @property
    def pitch(self):
        pitch_in_radians = self.fdmexec.get_property_value("attitude/pitch-rad")
        
        pitch_in_degrees = degrees(pitch_in_radians)
        
        return pitch_in_degrees
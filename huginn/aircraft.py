from math import degrees

from huginn.unit_conversions import convert_feet_to_meters, convert_knots_to_meters_per_sec
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared, convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal

from huginn.unit_conversions import convert_pounds_to_newtons

class GPS(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
    
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
    
class Accelerometer(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
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
    
class Gyroscope(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

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

class Thermometer(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
    
    @property
    def temperature(self):
        temperature_in_rankine = self.fdmexec.get_property_value("atmosphere/T-R")
        
        temperature_in_Kelvin = convert_rankine_to_kelvin(temperature_in_rankine)
        
        return temperature_in_Kelvin
    
class PressureSensor(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def pressure(self):
        pressure_in_psf = self.fdmexec.get_property_value("atmosphere/P-psf")
        
        pressure_in_pascal = convert_psf_to_pascal(pressure_in_psf)
        
        return pressure_in_pascal
    
class PitotTube(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
    
    @property
    def pressure(self):
        pressure_in_psf = self.fdmexec.get_property_value("aero/qbar-psf")
        
        pressure_in_pascal = convert_psf_to_pascal(pressure_in_psf)
        
        return pressure_in_pascal        

class InertialNavigationSystem(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
    
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
    
    @property
    def heading(self):
        yaw_in_radians = self.fdmexec.get_property_value("attitude/heading-true-rad")
        
        yaw_in_degrees = degrees(yaw_in_radians)
        
        return yaw_in_degrees
    
    @property
    def latitude(self):
        return self.fdmexec.get_property_value("position/lat-gc-deg")
    
    @property
    def longitude(self):
        return self.fdmexec.get_property_value("position/long-gc-deg")
    
    @property
    def airspeed(self):
        airspeed_in_knots = self.fdmexec.get_property_value("velocities/vtrue-kts")
        airspeed_in_meters_per_sec = convert_knots_to_meters_per_sec(airspeed_in_knots)
        
        return airspeed_in_meters_per_sec
    
    @property
    def altitude(self):
        altitude_in_feet = self.fdmexec.get_property_value("position/h-sl-ft")
        altitude_in_meters = convert_feet_to_meters(altitude_in_feet)
        
        return altitude_in_meters
    
class Controls(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
    @property
    def aileron(self):
        return self.fdmexec.get_property_value("fcs/aileron-cmd-norm")
    
    @aileron.setter
    def aileron(self, value):
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0 
        
        self.fdmexec.set_property_value("fcs/aileron-cmd-norm", value)

    @property
    def elevator(self):
        return self.fdmexec.get_property_value("fcs/elevator-cmd-norm")
    
    @elevator.setter
    def elevator(self, value):
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0 
        
        self.fdmexec.set_property_value("fcs/elevator-cmd-norm", value)

    @property
    def rudder(self):
        return self.fdmexec.get_property_value("fcs/rudder-cmd-norm")
    
    @rudder.setter
    def rudder(self, value):
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0 
        
        self.fdmexec.set_property_value("fcs/rudder-cmd-norm", value)

class Engine(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
    @property
    def rpm(self):
        return self.fdmexec.get_property_value("propulsion/engine/engine-rpm")
    
    @property
    def thrust(self):
        thrust_in_lbs = self.fdmexec.get_property_value("propulsion/engine/thrust-lbs")
        
        return convert_pounds_to_newtons(thrust_in_lbs)
    
    @property
    def power(self):
        return self.fdmexec.get_property_value("propulsion/engine/power-hp")
    
    @property
    def throttle(self):
        return self.fdmexec.get_property_value("fcs/throttle-cmd-norm")
    
    @throttle.setter
    def throttle(self, value):
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0
            
        self.fdmexec.set_property_value("fcs/throttle-cmd-norm", value)

class Aircraft(object):
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
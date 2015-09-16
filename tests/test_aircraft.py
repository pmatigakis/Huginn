from unittest import TestCase
import math

from huginn.aircraft import Controls, Engine, GPS, Accelerometer, Gyroscope, Thermometer, PressureSensor, PitotTube, InertialNavigationSystem
from huginn.unit_conversions import convert_pounds_to_newtons, convert_knots_to_meters_per_sec, convert_feet_to_meters 
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared, convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal

from test_common import get_fdmexec

class TestControls(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
    
    def test_get_aileron(self):
        controls = Controls(self.fdmexec)
        
        aileron = controls.aileron
        
        expected_aileron = self.fdmexec.get_property_value("fcs/aileron-cmd-norm")
        
        self.assertAlmostEqual(aileron, expected_aileron, 3)
    
    def test_set_aileron(self):
        controls = Controls(self.fdmexec)
        
        controls.aileron = 0.678
        
        expected_aileron = self.fdmexec.get_property_value("fcs/aileron-cmd-norm")
        
        self.assertAlmostEqual(expected_aileron, 0.678, 3)
        
    def test_get_elevator(self):
        controls = Controls(self.fdmexec)
        
        elevator = controls.elevator
        
        expected_elevator = self.fdmexec.get_property_value("fcs/elevator-cmd-norm")
        
        self.assertAlmostEqual(elevator, expected_elevator, 3)
    
    def test_set_elevator(self):
        controls = Controls(self.fdmexec)
        
        controls.elevator = 0.378
        
        expected_elevator = self.fdmexec.get_property_value("fcs/elevator-cmd-norm")
        
        self.assertAlmostEqual(expected_elevator, 0.378, 3)
        
    def test_get_rudder(self):
        controls = Controls(self.fdmexec)
        
        rudder = controls.rudder
        
        expected_rudder = self.fdmexec.get_property_value("fcs/rudder-cmd-norm")
        
        self.assertAlmostEqual(rudder, expected_rudder, 3)
    
    def test_set_rudder(self):
        controls = Controls(self.fdmexec)
        
        controls.rudder = 0.178
        
        expected_rudder = self.fdmexec.get_property_value("fcs/rudder-cmd-norm")
        
        self.assertAlmostEqual(expected_rudder, 0.178, 3)

class TestEngine(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        
    def test_rpm(self):
        engine = Engine(self.fdmexec)
        
        rpm = engine.rpm
        
        expected_rpm = self.fdmexec.get_property_value("propulsion/engine/engine-rpm")
        
        self.assertAlmostEqual(rpm, expected_rpm, 3)
        
    def test_thrust(self):
        engine = Engine(self.fdmexec)
        
        thrust = engine.thrust
        
        expected_thrust = self.fdmexec.get_property_value("propulsion/engine/thrust-lbs")
        
        expected_thrust = convert_pounds_to_newtons(expected_thrust)
        
        self.assertAlmostEqual(thrust, expected_thrust, 3)
        
    def test_power(self):
        engine = Engine(self.fdmexec)
        
        engine_power = engine.power
        
        expected_engine_power = self.fdmexec.get_property_value("propulsion/engine/power-hp")
        
        self.assertAlmostEqual(engine_power, expected_engine_power, 3)
        
    def test_get_throttle(self):
        engine = Engine(self.fdmexec)
        
        throttle = engine.throttle
        
        expected_throttle = self.fdmexec.get_property_value("fcs/throttle-cmd-norm")
        
        self.assertAlmostEqual(throttle, expected_throttle, 3)
        
    def test_set_throttle(self):
        engine = Engine(self.fdmexec)
        
        engine.throttle = 0.678
        
        throttle = self.fdmexec.get_property_value("fcs/throttle-cmd-norm")
        
        self.assertAlmostEqual(throttle, 0.678, 3)

class TestGPS(TestCase):        
    def setUp(self):
        self.fdmexec = get_fdmexec()
    
    def test_gps_latitude(self):
        gps = GPS(self.fdmexec)
        
        latitude = gps.latitude
        
        expected_latitude = self.fdmexec.get_property_value("position/lat-gc-deg")
        
        self.assertAlmostEqual(latitude, expected_latitude, 3)

    def test_gps_longitude(self):        
        gps = GPS(self.fdmexec)
        
        longitude = gps.longitude
        
        expected_longitude = self.fdmexec.get_property_value("position/long-gc-deg")
        
        self.assertAlmostEqual(longitude, expected_longitude, 3)
        
    def test_airspeed(self):
        gps = GPS(self.fdmexec)

        airspeed = gps.airspeed
        
        expected_airspeed_in_knots = self.fdmexec.get_property_value("velocities/vtrue-kts")
        expected_airspeed_in_meters_per_sec = convert_knots_to_meters_per_sec(expected_airspeed_in_knots)
        
        self.assertAlmostEqual(airspeed, expected_airspeed_in_meters_per_sec, 3)
        
    def test_altitude(self):        
        gps = GPS(self.fdmexec)

        altitude = gps.altitude
        
        expected_altitude_in_feet = self.fdmexec.get_property_value("position/h-sl-ft")
        expected_altitude_in_meters = convert_feet_to_meters(expected_altitude_in_feet)
        
        self.assertAlmostEqual(altitude, expected_altitude_in_meters, 3)
        
    def test_heading(self):        
        gps = GPS(self.fdmexec)
        
        heading = gps.heading
        
        expected_heading_in_radians = self.fdmexec.get_property_value("attitude/heading-true-rad")
        expected_heading_in_degrees = math.degrees(expected_heading_in_radians)
        
        self.assertAlmostEqual(heading, expected_heading_in_degrees, 3)
        
class TestAccelerometer(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()

    def test_x_acceleration(self):        
        accelerometer = Accelerometer(self.fdmexec)
        
        acceleration = accelerometer.x_acceleration
        
        expected_acceleration_in_ft_sec2 = self.fdmexec.get_property_value("accelerations/a-pilot-x-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
    def test_y_acceleration(self):
        accelerometer = Accelerometer(self.fdmexec)
        
        acceleration = accelerometer.y_acceleration
        
        expected_acceleration_in_ft_sec2 = self.fdmexec.get_property_value("accelerations/a-pilot-y-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
    def test_z_acceleration(self):
        accelerometer = Accelerometer(self.fdmexec)
        
        acceleration = accelerometer.z_acceleration
        
        expected_acceleration_in_ft_sec2 = self.fdmexec.get_property_value("accelerations/a-pilot-z-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
class TestGyroscope(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
    
    def test_roll_rate(self):        
        gyroscope = Gyroscope(self.fdmexec)
        
        roll_rate = gyroscope.roll_rate
        
        expected_roll_rate_in_rad_sec = self.fdmexec.get_property_value("velocities/p-rad_sec")
        expected_roll_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_roll_rate_in_rad_sec)
        
        self.assertAlmostEqual(roll_rate, expected_roll_rate_in_degres_sec, 3)
        
    def test_pitch_rate(self):
        gyroscope = Gyroscope(self.fdmexec)
        
        pitch_rate = gyroscope.pitch_rate
        
        expected_pitch_rate_in_rad_sec = self.fdmexec.get_property_value("velocities/q-rad_sec")
        expected_pitch_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_pitch_rate_in_rad_sec)
        
        self.assertAlmostEqual(pitch_rate, expected_pitch_rate_in_degres_sec, 3)
        
    def test_yaw_rate(self):        
        gyroscope = Gyroscope(self.fdmexec)
        
        yaw_rate = gyroscope.yaw_rate
        
        expected_yaw_rate_in_rad_sec = self.fdmexec.get_property_value("velocities/q-rad_sec")
        expected_yaw_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_yaw_rate_in_rad_sec)
        
        self.assertAlmostEqual(yaw_rate, expected_yaw_rate_in_degres_sec, 3)
        
class TestThermometer(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()

    def test_temperature(self):
        thermometer = Thermometer(self.fdmexec)
        
        temperature = thermometer.temperature
        
        expected_temperature_in_rankine = self.fdmexec.get_property_value("atmosphere/T-R")
        
        expected_temperature_in_kelvin = convert_rankine_to_kelvin(expected_temperature_in_rankine)
        
        self.assertAlmostEqual(temperature, expected_temperature_in_kelvin)
        
class TestPressureSensor(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()

    def test_pressure(self):
        pressure_sensor = PressureSensor(self.fdmexec)
        
        pressure = pressure_sensor.pressure
        
        expected_pressure_in_psf = self.fdmexec.get_property_value("atmosphere/P-psf")
        
        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)
        
        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)
        
class TestPitotTube(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()

    def test_pressure(self):
        pitot_tube = PitotTube(self.fdmexec)
        
        pressure = pitot_tube.pressure
        
        expected_pressure_in_psf = self.fdmexec.get_property_value("aero/qbar-psf")
        
        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)
        
        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)
        
class TestInertialNavigationSystem(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()

    def test_climb_rate(self):
        ins = InertialNavigationSystem(self.fdmexec)
         
        climb_rate = ins.climb_rate
         
        expected_climb_rate = self.fdmexec.get_property_value("velocities/v-down-fps")
         
        expected_climb_rate_in_meters_sec = convert_feet_to_meters(expected_climb_rate)
         
        self.assertAlmostEqual(climb_rate, expected_climb_rate_in_meters_sec, 3)    
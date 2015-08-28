from unittest import TestCase
import math

from huginn.sensors import GPS, Accelerometer, Gyroscope, Thermometer, PressureSensor, PitotTube
from huginn.unit_conversions import convert_knots_to_meters_per_sec, convert_feet_to_meters
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared, convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal

from test_protocols import get_fdmexec

class TestGPS(TestCase):        
    def test_gps_latitude(self):
        fdmexec = get_fdmexec()
        
        gps = GPS(fdmexec)
        
        latitude = gps.latitude
        
        expected_latitude = fdmexec.get_property_value("position/lat-gc-deg")
        
        self.assertAlmostEqual(latitude, expected_latitude, 3)

    def test_gps_longitude(self):
        fdmexec = get_fdmexec()
        
        gps = GPS(fdmexec)
        
        longitude = gps.longitude
        
        expected_longitude = fdmexec.get_property_value("position/long-gc-deg")
        
        self.assertAlmostEqual(longitude, expected_longitude, 3)
        
    def test_airspeed(self):
        fdmexec = get_fdmexec()
        
        gps = GPS(fdmexec)

        airspeed = gps.airspeed
        
        expected_airspeed_in_knots = fdmexec.get_property_value("velocities/vtrue-kts")
        expected_airspeed_in_meters_per_sec = convert_knots_to_meters_per_sec(expected_airspeed_in_knots)
        
        self.assertAlmostEqual(airspeed, expected_airspeed_in_meters_per_sec, 3)
        
    def test_altitude(self):
        fdmexec = get_fdmexec()
        
        gps = GPS(fdmexec)

        altitude = gps.altitude
        
        expected_altitude_in_feet = fdmexec.get_property_value("position/h-sl-ft")
        expected_altitude_in_meters = convert_feet_to_meters(expected_altitude_in_feet)
        
        self.assertAlmostEqual(altitude, expected_altitude_in_meters, 3)
        
    def test_heading(self):
        fdmexec = get_fdmexec()
        
        gps = GPS(fdmexec)
        
        heading = gps.heading
        
        expected_heading_in_radians = fdmexec.get_property_value("attitude/heading-true-rad")
        expected_heading_in_degrees = math.degrees(expected_heading_in_radians)
        
        self.assertAlmostEqual(heading, expected_heading_in_degrees, 3)
        
class TestAccelerometer(TestCase):
    def test_x_acceleration(self):
        fdmexec = get_fdmexec()
        
        accelerometer = Accelerometer(fdmexec)
        
        acceleration = accelerometer.x_acceleration
        
        expected_acceleration_in_ft_sec2 = fdmexec.get_property_value("accelerations/a-pilot-x-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
    def test_y_acceleration(self):
        fdmexec = get_fdmexec()
        
        accelerometer = Accelerometer(fdmexec)
        
        acceleration = accelerometer.y_acceleration
        
        expected_acceleration_in_ft_sec2 = fdmexec.get_property_value("accelerations/a-pilot-y-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
    def test_z_acceleration(self):
        fdmexec = get_fdmexec()
        
        accelerometer = Accelerometer(fdmexec)
        
        acceleration = accelerometer.z_acceleration
        
        expected_acceleration_in_ft_sec2 = fdmexec.get_property_value("accelerations/a-pilot-z-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
class TestGyroscope(TestCase):
    def test_roll_rate(self):
        fdmexec = get_fdmexec()
        
        gyroscope = Gyroscope(fdmexec)
        
        roll_rate = gyroscope.roll_rate
        
        expected_roll_rate_in_rad_sec = fdmexec.get_property_value("velocities/p-rad_sec")
        expected_roll_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_roll_rate_in_rad_sec)
        
        self.assertAlmostEqual(roll_rate, expected_roll_rate_in_degres_sec, 3)
        
    def test_pitch_rate(self):
        fdmexec = get_fdmexec()
        
        gyroscope = Gyroscope(fdmexec)
        
        pitch_rate = gyroscope.pitch_rate
        
        expected_pitch_rate_in_rad_sec = fdmexec.get_property_value("velocities/q-rad_sec")
        expected_pitch_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_pitch_rate_in_rad_sec)
        
        self.assertAlmostEqual(pitch_rate, expected_pitch_rate_in_degres_sec, 3)
        
    def test_yaw_rate(self):
        fdmexec = get_fdmexec()
        
        gyroscope = Gyroscope(fdmexec)
        
        yaw_rate = gyroscope.yaw_rate
        
        expected_yaw_rate_in_rad_sec = fdmexec.get_property_value("velocities/q-rad_sec")
        expected_yaw_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_yaw_rate_in_rad_sec)
        
        self.assertAlmostEqual(yaw_rate, expected_yaw_rate_in_degres_sec, 3)
        
class TestThermometer(TestCase):
    def test_temperature(self):
        fdmexec = get_fdmexec()
        
        thermometer = Thermometer(fdmexec)
        
        temperature = thermometer.temperature
        
        expected_temperature_in_rankine = fdmexec.get_property_value("atmosphere/T-R")
        
        expected_temperature_in_kelvin = convert_rankine_to_kelvin(expected_temperature_in_rankine)
        
        self.assertAlmostEqual(temperature, expected_temperature_in_kelvin)
        
class TestPressureSensor(TestCase):
    def test_pressure(self):
        fdmexec = get_fdmexec()
        
        pressure_sensor = PressureSensor(fdmexec)
        
        pressure = pressure_sensor.pressure
        
        expected_pressure_in_psf = fdmexec.get_property_value("atmosphere/P-psf")
        
        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)
        
        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)
        
class TestPitotTube(TestCase):
    def test_pressure(self):
        fdmexec = get_fdmexec()
        
        pitot_tube = PitotTube(fdmexec)
        
        pressure = pitot_tube.pressure
        
        expected_pressure_in_psf = fdmexec.get_property_value("aero/qbar-psf")
        
        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)
        
        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)
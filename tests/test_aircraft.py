import pkg_resources
from unittest import TestCase
import math

from huginn.aircraft import Controls, Engine, GPS, Accelerometer, Gyroscope,\
                            Thermometer, PressureSensor, PitotTube
from huginn.unit_conversions import convert_feet_to_meters 
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared,\
                                    convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal,\
                                    convert_libra_to_newtons
from huginn.fdm import create_fdmexec
from huginn import configuration

from mock.mock import MagicMock

class TestControls(TestCase):    
    def test_get_aileron(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        controls = Controls(fdm)
        
        aileron = controls.aileron
        
        expected_aileron = fdm.get_aileron()
        
        self.assertAlmostEqual(aileron, expected_aileron, 3)
    
    def test_set_aileron(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        fdm.set_aileron = MagicMock()
        
        controls = Controls(fdm)
        
        controls.aileron = 0.678
        
        fdm.set_aileron.assert_called_once_with(0.678)
        
    def test_get_elevator(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        controls = Controls(fdm)
        
        elevator = controls.elevator
        
        expected_elevator = fdm.get_elevator()
        
        self.assertAlmostEqual(elevator, expected_elevator, 3)
    
    def test_set_elevator(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        fdm.set_elevator = MagicMock()
        
        controls = Controls(fdm)
        
        controls.elevator = 0.378
        
        fdm.set_elevator.assert_called_once_with(0.378)
        
    def test_get_rudder(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        controls = Controls(fdm)
        
        rudder = controls.rudder
        
        expected_rudder = fdm.get_rudder()
        
        self.assertAlmostEqual(rudder, expected_rudder, 3)
    
    def test_set_rudder(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        fdm.set_rudder = MagicMock()
        
        controls = Controls(fdm)
        
        controls.rudder = 0.178
        
        fdm.set_rudder.assert_called_once_with(0.178)

    def test_get_throttle(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        controls = Controls(fdm)
        
        throttle = controls.throttle
        
        expected_throttle = fdm.get_throttle()
        
        self.assertAlmostEqual(throttle, expected_throttle, 3)
    
    def test_set_throttle(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)
        
        fdm.set_throttle = MagicMock()
        
        controls = Controls(fdm)
        
        controls.throttle = 0.178
        
        fdm.set_throttle.assert_called_once_with(0.178)

class TestEngine(TestCase):                
    def test_thrust(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)        

        engine = Engine(fdm)
        engine.run()

        thrust = engine.thrust 

        expected_thrust = convert_libra_to_newtons(fdm.get_thrust())

        self.assertAlmostEqual(thrust, expected_thrust, 3)

    def test_get_throttle(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        engine = Engine(fdm)
        engine.run()

        throttle = engine.throttle

        expected_throttle = fdm.get_throttle()

        self.assertAlmostEqual(throttle, expected_throttle, 3)

class TestGPS(TestCase):            
    def test_gps_latitude(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        gps = GPS(fdm)
        gps.run()

        latitude = gps.latitude

        expected_latitude = fdm.get_latitude()

        self.assertAlmostEqual(latitude, expected_latitude, 3)

    def test_gps_longitude(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        gps = GPS(fdm)
        gps.run()

        longitude = gps.longitude

        expected_longitude = fdm.get_longitude()

        self.assertAlmostEqual(longitude, expected_longitude, 3)

    def test_airspeed(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        gps = GPS(fdm)
        gps.run()

        airspeed = gps.airspeed

        expected_airspeed_in_fps = fdm.get_airspeed()
        expected_airspeed_in_meters_per_sec = convert_feet_to_meters(expected_airspeed_in_fps)

        self.assertAlmostEqual(airspeed, expected_airspeed_in_meters_per_sec, 3)

    def test_altitude(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        gps = GPS(fdm)
        gps.run()

        altitude = gps.altitude

        expected_altitude_in_meters = fdm.get_altitude()

        self.assertAlmostEqual(altitude, expected_altitude_in_meters, 3)

    def test_heading(self):        
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        gps = GPS(fdm)
        gps.run()

        heading = gps.heading

        expected_heading_in_radians = fdm.get_heading()
        expected_heading_in_degrees = math.degrees(expected_heading_in_radians)

        self.assertAlmostEqual(heading, expected_heading_in_degrees, 3)

class TestAccelerometer(TestCase):
    def test_x_acceleration(self):        
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        accelerometer = Accelerometer(fdm)
        accelerometer.run()

        acceleration = accelerometer.x_acceleration

        expected_acceleration_in_ft_sec2 = fdm.get_x_acceleration()
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)

        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)

    def test_y_acceleration(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        accelerometer = Accelerometer(fdm)
        accelerometer.run()
        
        acceleration = accelerometer.y_acceleration
        
        expected_acceleration_in_ft_sec2 = fdm.get_y_acceleration()
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
    def test_z_acceleration(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        accelerometer = Accelerometer(fdm)
        accelerometer.run()

        acceleration = accelerometer.z_acceleration

        expected_acceleration_in_ft_sec2 = fdm.get_z_acceleration()
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)

        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)

class TestGyroscope(TestCase):    
    def test_roll_rate(self):        
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        gyroscope = Gyroscope(fdm)
        gyroscope.run()

        roll_rate = gyroscope.roll_rate

        expected_roll_rate_in_rad_sec = fdm.get_roll_rate()
        expected_roll_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_roll_rate_in_rad_sec)

        self.assertAlmostEqual(roll_rate, expected_roll_rate_in_degres_sec, 3)

    def test_pitch_rate(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        gyroscope = Gyroscope(fdm)
        gyroscope.run()

        pitch_rate = gyroscope.pitch_rate

        expected_pitch_rate_in_rad_sec = fdm.get_pitch_rate()
        expected_pitch_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_pitch_rate_in_rad_sec)

        self.assertAlmostEqual(pitch_rate, expected_pitch_rate_in_degres_sec, 3)

    def test_yaw_rate(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        gyroscope = Gyroscope(fdm)
        gyroscope.run() 
        
        yaw_rate = gyroscope.yaw_rate
        
        expected_yaw_rate_in_rad_sec = fdm.get_yaw_rate()
        expected_yaw_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_yaw_rate_in_rad_sec)
        
        self.assertAlmostEqual(yaw_rate, expected_yaw_rate_in_degres_sec, 3)
        
class TestThermometer(TestCase):
    def test_temperature(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        thermometer = Thermometer(fdm)
        thermometer.run()
        
        temperature = thermometer.temperature

        expected_temperature_in_rankine = fdm.get_temperature()

        expected_temperature_in_kelvin = convert_rankine_to_kelvin(expected_temperature_in_rankine)

        self.assertAlmostEqual(temperature, expected_temperature_in_kelvin)
        
class TestPressureSensor(TestCase):
    def test_pressure(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        pressure_sensor = PressureSensor(fdm)
        pressure_sensor.run()
        
        pressure = pressure_sensor.pressure
        
        expected_pressure_in_psf = fdm.get_pressure()
        
        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)
        
        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)
        
class TestPitotTube(TestCase):
    def test_pressure(self):
        huginn_data_path = pkg_resources.resource_filename("huginn", "data")

        fdm = create_fdmexec(huginn_data_path, "Rascal", configuration.DT)

        pitot_tube = PitotTube(fdm)
        pitot_tube.run()
        
        pressure = pitot_tube.pressure

        expected_pressure_in_psf = fdm.get_total_pressure()

        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)

        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)

from unittest import TestCase
import math

from huginn.aircraft import Controls, Engine, GPS, Accelerometer, Gyroscope,\
                            Thermometer, PressureSensor, PitotTube
from huginn.unit_conversions import convert_feet_to_meters 
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared,\
                                    convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal,\
                                    convert_libra_to_newtons

from mockObjects import MockFDMExec
from mock.mock import MagicMock

class TestControls(TestCase):    
    def test_get_aileron(self):
        fdmexec = MockFDMExec()
        
        controls = Controls(fdmexec)
        
        aileron = controls.aileron
        
        expected_aileron = 0.55
        
        self.assertAlmostEqual(aileron, expected_aileron, 3)
    
    def test_set_aileron(self):
        fdmexec = MockFDMExec()
        
        fdmexec.GetFCS().SetDaCmd = MagicMock()
        
        controls = Controls(fdmexec)
        
        controls.aileron = 0.678
        
        fdmexec.GetFCS().SetDaCmd.assert_called_once_with(0.678)
        
    def test_get_elevator(self):
        fdmexec = MockFDMExec()
        
        controls = Controls(fdmexec)
        
        elevator = controls.elevator
        
        expected_elevator = 0.23
        
        self.assertAlmostEqual(elevator, expected_elevator, 3)
    
    def test_set_elevator(self):
        fdmexec = MockFDMExec()
        
        fdmexec.GetFCS().SetDeCmd = MagicMock()
        
        controls = Controls(fdmexec)
        
        controls.elevator = 0.378
        
        fdmexec.GetFCS().SetDeCmd.assert_called_once_with(0.378)
        
    def test_get_rudder(self):
        fdmexec = MockFDMExec()
        
        controls = Controls(fdmexec)
        
        rudder = controls.rudder
        
        expected_rudder = 0.7
        
        self.assertAlmostEqual(rudder, expected_rudder, 3)
    
    def test_set_rudder(self):
        fdmexec = MockFDMExec()
        
        fdmexec.GetFCS().SetDrCmd = MagicMock()
        
        controls = Controls(fdmexec)
        
        controls.rudder = 0.178
        
        fdmexec.GetFCS().SetDrCmd.assert_called_once_with(0.178)

    def test_get_throttle(self):
        fdmexec = MockFDMExec()
        
        controls = Controls(fdmexec)
        
        throttle = controls.throttle
        
        expected_throttle = 0.86
        
        self.assertAlmostEqual(throttle, expected_throttle, 3)
    
    def test_set_throttle(self):
        fdmexec = MockFDMExec()
        
        fdmexec.GetFCS().SetThrottleCmd = MagicMock()
        
        controls = Controls(fdmexec)
        
        controls.throttle = 0.178
        
        fdmexec.GetFCS().SetThrottleCmd.assert_called_once_with(0, 0.178)

class TestEngine(TestCase):                
    def test_thrust(self):
        fdmexec = MockFDMExec()        

        engine = Engine()
        engine.update_from_fdmexec(fdmexec)

        thrust = engine.thrust 

        expected_thrust = convert_libra_to_newtons(3452.87)

        self.assertAlmostEqual(thrust, expected_thrust, 3)

    def test_get_throttle(self):
        fdmexec = MockFDMExec()

        engine = Engine()
        engine.update_from_fdmexec(fdmexec)

        throttle = engine.throttle

        expected_throttle = 0.86

        self.assertAlmostEqual(throttle, expected_throttle, 3)

class TestGPS(TestCase):            
    def test_gps_latitude(self):
        fdmexec = MockFDMExec()

        gps = GPS()
        gps.update_from_fdmexec(fdmexec)

        latitude = gps.latitude

        expected_latitude = 37.34567

        self.assertAlmostEqual(latitude, expected_latitude, 3)

    def test_gps_longitude(self):
        fdmexec = MockFDMExec()

        gps = GPS()
        gps.update_from_fdmexec(fdmexec)

        longitude = gps.longitude

        expected_longitude = 21.63457

        self.assertAlmostEqual(longitude, expected_longitude, 3)

    def test_airspeed(self):
        fdmexec = MockFDMExec()

        gps = GPS()
        gps.update_from_fdmexec(fdmexec)

        airspeed = gps.airspeed

        expected_airspeed_in_fps = 375.453302
        expected_airspeed_in_meters_per_sec = convert_feet_to_meters(expected_airspeed_in_fps)

        self.assertAlmostEqual(airspeed, expected_airspeed_in_meters_per_sec, 3)

    def test_altitude(self):
        fdmexec = MockFDMExec()

        gps = GPS()
        gps.update_from_fdmexec(fdmexec)

        altitude = gps.altitude

        expected_altitude_in_meters = 10000.0

        self.assertAlmostEqual(altitude, expected_altitude_in_meters, 3)

    def test_heading(self):        
        fdmexec = MockFDMExec()

        gps = GPS()
        gps.update_from_fdmexec(fdmexec)

        heading = gps.heading

        expected_heading_in_radians = 0.3
        expected_heading_in_degrees = math.degrees(expected_heading_in_radians)

        self.assertAlmostEqual(heading, expected_heading_in_degrees, 3)

class TestAccelerometer(TestCase):
    def test_x_acceleration(self):        
        fdmexec = MockFDMExec()

        accelerometer = Accelerometer()
        accelerometer.update_from_fdmexec(fdmexec)

        acceleration = accelerometer.x_acceleration

        expected_acceleration_in_ft_sec2 = 0.1
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)

        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)

    def test_y_acceleration(self):
        fdmexec = MockFDMExec()

        accelerometer = Accelerometer()
        accelerometer.update_from_fdmexec(fdmexec)
        
        acceleration = accelerometer.y_acceleration
        
        expected_acceleration_in_ft_sec2 = 0.2
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
    def test_z_acceleration(self):
        fdmexec = MockFDMExec()

        accelerometer = Accelerometer()
        accelerometer.update_from_fdmexec(fdmexec)

        acceleration = accelerometer.z_acceleration

        expected_acceleration_in_ft_sec2 = 0.3
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)

        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)

class TestGyroscope(TestCase):    
    def test_roll_rate(self):        
        fdmexec = MockFDMExec()

        gyroscope = Gyroscope()
        gyroscope.update_from_fdmexec(fdmexec)

        roll_rate = gyroscope.roll_rate

        expected_roll_rate_in_rad_sec = 1.1
        expected_roll_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_roll_rate_in_rad_sec)

        self.assertAlmostEqual(roll_rate, expected_roll_rate_in_degres_sec, 3)

    def test_pitch_rate(self):
        fdmexec = MockFDMExec()

        gyroscope = Gyroscope()
        gyroscope.update_from_fdmexec(fdmexec)

        pitch_rate = gyroscope.pitch_rate

        expected_pitch_rate_in_rad_sec = 2.2
        expected_pitch_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_pitch_rate_in_rad_sec)

        self.assertAlmostEqual(pitch_rate, expected_pitch_rate_in_degres_sec, 3)

    def test_yaw_rate(self):
        fdmexec = MockFDMExec()

        gyroscope = Gyroscope()
        gyroscope.update_from_fdmexec(fdmexec) 
        
        yaw_rate = gyroscope.yaw_rate
        
        expected_yaw_rate_in_rad_sec = 3.3
        expected_yaw_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_yaw_rate_in_rad_sec)
        
        self.assertAlmostEqual(yaw_rate, expected_yaw_rate_in_degres_sec, 3)
        
class TestThermometer(TestCase):
    def test_temperature(self):
        fdmexec = MockFDMExec()

        thermometer = Thermometer()
        thermometer.update_from_fdmexec(fdmexec)
        
        temperature = thermometer.temperature

        expected_temperature_in_rankine = 567.32

        expected_temperature_in_kelvin = convert_rankine_to_kelvin(expected_temperature_in_rankine)

        self.assertAlmostEqual(temperature, expected_temperature_in_kelvin)
        
class TestPressureSensor(TestCase):
    def test_pressure(self):
        fdmexec = MockFDMExec()

        pressure_sensor = PressureSensor()
        pressure_sensor.update_from_fdmexec(fdmexec)
        
        pressure = pressure_sensor.pressure
        
        expected_pressure_in_psf = 456.39
        
        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)
        
        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)
        
class TestPitotTube(TestCase):
    def test_pressure(self):
        fdmexec = MockFDMExec()

        pitot_tube = PitotTube()
        pitot_tube.update_from_fdmexec(fdmexec)
        
        pressure = pitot_tube.pressure

        expected_pressure_in_psf = 12233.2

        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)

        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)

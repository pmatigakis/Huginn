from unittest import TestCase
import math

from huginn.aircraft import Controls, Engine, GPS, Accelerometer, Gyroscope,\
                            Thermometer, PressureSensor, PitotTube,\
                            InertialNavigationSystem
from huginn.unit_conversions import convert_pounds_to_newtons,\
                                    convert_knots_to_meters_per_sec,\
                                    convert_feet_to_meters 
from huginn.unit_conversions import convert_feet_sec_squared_to_meters_sec_squared,\
                                    convert_radians_sec_to_degrees_sec
from huginn.unit_conversions import convert_rankine_to_kelvin, convert_psf_to_pascal

from mockObjects import MockFDMModel
from mock.mock import MagicMock

class TestControls(TestCase):    
    def test_get_aileron(self):
        fdm_model = MockFDMModel()
        
        controls = Controls(fdm_model)
        
        aileron = controls.aileron
        
        expected_aileron = fdm_model.get_property_value("fcs/aileron-cmd-norm")
        
        self.assertAlmostEqual(aileron, expected_aileron, 3)
    
    def test_set_aileron(self):
        fdm_model = MockFDMModel()
        
        fdm_model.set_property_value = MagicMock()
        
        controls = Controls(fdm_model)
        
        controls.aileron = 0.678
        
        fdm_model.set_property_value.assert_called_once_with("fcs/aileron-cmd-norm", 0.678)
        
    def test_get_elevator(self):
        fdm_model = MockFDMModel()
        
        controls = Controls(fdm_model)
        
        elevator = controls.elevator
        
        expected_elevator = fdm_model.get_property_value("fcs/elevator-cmd-norm")
        
        self.assertAlmostEqual(elevator, expected_elevator, 3)
    
    def test_set_elevator(self):
        fdm_model = MockFDMModel()
        
        fdm_model.set_property_value = MagicMock()
        
        controls = Controls(fdm_model)
        
        controls.elevator = 0.378
        
        fdm_model.set_property_value.assert_called_once_with("fcs/elevator-cmd-norm", 0.378)
        
    def test_get_rudder(self):
        fdm_model = MockFDMModel()
        
        controls = Controls(fdm_model)
        
        rudder = controls.rudder
        
        expected_rudder = fdm_model.get_property_value("fcs/rudder-cmd-norm")
        
        self.assertAlmostEqual(rudder, expected_rudder, 3)
    
    def test_set_rudder(self):
        fdm_model = MockFDMModel()
        
        fdm_model.set_property_value = MagicMock()
        
        controls = Controls(fdm_model)
        
        controls.rudder = 0.178
        
        fdm_model.set_property_value.assert_called_once_with("fcs/rudder-cmd-norm", 0.178)
        
class TestEngine(TestCase):        
    def test_rpm(self):
        fdm_model = MockFDMModel()
        
        engine = Engine(fdm_model)
        
        rpm = engine.rpm
        
        expected_rpm = fdm_model.get_property_value("propulsion/engine/engine-rpm")
        
        self.assertAlmostEqual(rpm, expected_rpm, 3)
        
    def test_thrust(self):
        fdm_model = MockFDMModel()        

        engine = Engine(fdm_model)

        thrust = engine.thrust

        expected_thrust = fdm_model.get_property_value("propulsion/engine/thrust-lbs")

        expected_thrust = convert_pounds_to_newtons(expected_thrust)

        self.assertAlmostEqual(thrust, expected_thrust, 3)

    def test_power(self):
        fdm_model = MockFDMModel()

        engine = Engine(fdm_model)

        engine_power = engine.power

        expected_engine_power = fdm_model.get_property_value("propulsion/engine/power-hp")

        self.assertAlmostEqual(engine_power, expected_engine_power, 3)

    def test_get_throttle(self):
        fdm_model = MockFDMModel()

        engine = Engine(fdm_model)

        throttle = engine.throttle

        expected_throttle = fdm_model.get_property_value("fcs/throttle-cmd-norm")

        self.assertAlmostEqual(throttle, expected_throttle, 3)

    def test_set_throttle(self):
        fdm_model = MockFDMModel()

        fdm_model.set_property_value = MagicMock()

        engine = Engine(fdm_model)
        
        engine.throttle = 0.678

        fdm_model.set_property_value.assert_called_once_with("fcs/throttle-cmd-norm", 0.678)

class TestGPS(TestCase):            
    def test_gps_latitude(self):
        fdm_model = MockFDMModel()

        gps = GPS(fdm_model)

        latitude = gps.latitude

        expected_latitude = fdm_model.get_property_value("position/lat-gc-deg")

        self.assertAlmostEqual(latitude, expected_latitude, 3)

    def test_gps_longitude(self):
        fdm_model = MockFDMModel()
        
        gps = GPS(fdm_model)
        
        longitude = gps.longitude
        
        expected_longitude = fdm_model.get_property_value("position/long-gc-deg")
        
        self.assertAlmostEqual(longitude, expected_longitude, 3)
        
    def test_airspeed(self):
        fdm_model = MockFDMModel()

        gps = GPS(fdm_model)

        airspeed = gps.airspeed

        expected_airspeed_in_knots = fdm_model.get_property_value("velocities/vtrue-kts")
        expected_airspeed_in_meters_per_sec = convert_knots_to_meters_per_sec(expected_airspeed_in_knots)

        self.assertAlmostEqual(airspeed, expected_airspeed_in_meters_per_sec, 3)

    def test_altitude(self):
        fdm_model = MockFDMModel()

        gps = GPS(fdm_model)

        altitude = gps.altitude

        expected_altitude_in_feet = fdm_model.get_property_value("position/h-sl-ft")
        expected_altitude_in_meters = convert_feet_to_meters(expected_altitude_in_feet)

        self.assertAlmostEqual(altitude, expected_altitude_in_meters, 3)

    def test_heading(self):        
        fdm_model = MockFDMModel()

        gps = GPS(fdm_model)

        heading = gps.heading

        expected_heading_in_radians = fdm_model.get_property_value("attitude/heading-true-rad")
        expected_heading_in_degrees = math.degrees(expected_heading_in_radians)

        self.assertAlmostEqual(heading, expected_heading_in_degrees, 3)

class TestAccelerometer(TestCase):
    def test_x_acceleration(self):        
        fdm_model = MockFDMModel()

        accelerometer = Accelerometer(fdm_model)
        
        acceleration = accelerometer.x_acceleration
        
        expected_acceleration_in_ft_sec2 = fdm_model.get_property_value("accelerations/a-pilot-x-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
    def test_y_acceleration(self):
        fdm_model = MockFDMModel()

        accelerometer = Accelerometer(fdm_model)
        
        acceleration = accelerometer.y_acceleration
        
        expected_acceleration_in_ft_sec2 = fdm_model.get_property_value("accelerations/a-pilot-y-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)
        
        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)
        
    def test_z_acceleration(self):
        fdm_model = MockFDMModel()

        accelerometer = Accelerometer(fdm_model)

        acceleration = accelerometer.z_acceleration

        expected_acceleration_in_ft_sec2 = fdm_model.get_property_value("accelerations/a-pilot-z-ft_sec2")
        expected_acceleration_in_m_sec2 = convert_feet_sec_squared_to_meters_sec_squared(expected_acceleration_in_ft_sec2)

        self.assertAlmostEqual(acceleration, expected_acceleration_in_m_sec2, 3)

class TestGyroscope(TestCase):    
    def test_roll_rate(self):        
        fdm_model = MockFDMModel()

        gyroscope = Gyroscope(fdm_model)

        roll_rate = gyroscope.roll_rate

        expected_roll_rate_in_rad_sec = fdm_model.get_property_value("velocities/p-rad_sec")
        expected_roll_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_roll_rate_in_rad_sec)

        self.assertAlmostEqual(roll_rate, expected_roll_rate_in_degres_sec, 3)

    def test_pitch_rate(self):
        fdm_model = MockFDMModel()

        gyroscope = Gyroscope(fdm_model)

        pitch_rate = gyroscope.pitch_rate

        expected_pitch_rate_in_rad_sec = fdm_model.get_property_value("velocities/q-rad_sec")
        expected_pitch_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_pitch_rate_in_rad_sec)

        self.assertAlmostEqual(pitch_rate, expected_pitch_rate_in_degres_sec, 3)

    def test_yaw_rate(self):
        fdm_model = MockFDMModel()

        gyroscope = Gyroscope(fdm_model)
        
        yaw_rate = gyroscope.yaw_rate
        
        expected_yaw_rate_in_rad_sec = fdm_model.get_property_value("velocities/r-rad_sec")
        expected_yaw_rate_in_degres_sec = convert_radians_sec_to_degrees_sec(expected_yaw_rate_in_rad_sec)
        
        self.assertAlmostEqual(yaw_rate, expected_yaw_rate_in_degres_sec, 3)
        
class TestThermometer(TestCase):
    def test_temperature(self):
        fdm_model = MockFDMModel()

        thermometer = Thermometer(fdm_model)

        temperature = thermometer.temperature

        expected_temperature_in_rankine = fdm_model.get_property_value("atmosphere/T-R")

        expected_temperature_in_kelvin = convert_rankine_to_kelvin(expected_temperature_in_rankine)

        self.assertAlmostEqual(temperature, expected_temperature_in_kelvin)
        
class TestPressureSensor(TestCase):
    def test_pressure(self):
        fdm_model = MockFDMModel()

        pressure_sensor = PressureSensor(fdm_model)
        
        pressure = pressure_sensor.pressure
        
        expected_pressure_in_psf = fdm_model.get_property_value("atmosphere/P-psf")
        
        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)
        
        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)
        
class TestPitotTube(TestCase):
    def test_pressure(self):
        fdm_model = MockFDMModel()

        pitot_tube = PitotTube(fdm_model)

        pressure = pitot_tube.pressure

        expected_pressure_in_psf = fdm_model.get_property_value("aero/qbar-psf")

        expected_pressure_in_pascal = convert_psf_to_pascal(expected_pressure_in_psf)

        self.assertAlmostEqual(pressure, expected_pressure_in_pascal, 3)

from unittest import TestCase
import json 

from huginn.aircraft import Aircraft
from huginn.http import FDMData, GPSData, AccelerometerData, GyroscopeData,\
                        ThermometerData, PressureSensorData, PitotTubeData,\
                        InertialNavigationSystemData, EngineData,\
                        FlightControlsData

from test_common import get_fdmexec 

class TestFDMData(TestCase):
    def setUp(self):
        fdmexec = get_fdmexec()
        self.aircraft = Aircraft(fdmexec)
    
    def test_create_fdm_data_response(self):
        fdm_data_resource = FDMData(self.aircraft)

        fdm_data_response = fdm_data_resource.create_fdm_data_response()

        self.assertAlmostEqual(self.aircraft.thermometer.temperature, fdm_data_response["temperature"], 3)
        self.assertAlmostEqual(self.aircraft.pitot_tube.pressure, fdm_data_response["dynamic_pressure"], 3)
        self.assertAlmostEqual(self.aircraft.pressure_sensor.pressure, fdm_data_response["static_pressure"], 3)
        self.assertAlmostEqual(self.aircraft.gps.latitude, fdm_data_response["latitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.longitude, fdm_data_response["longitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.altitude, fdm_data_response["altitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.airspeed, fdm_data_response["airspeed"], 3)
        self.assertAlmostEqual(self.aircraft.gps.heading, fdm_data_response["heading"], 3)
        self.assertAlmostEqual(self.aircraft.accelerometer.x_acceleration, fdm_data_response["x_acceleration"], 3)
        self.assertAlmostEqual(self.aircraft.accelerometer.y_acceleration, fdm_data_response["y_acceleration"], 3)
        self.assertAlmostEqual(self.aircraft.accelerometer.z_acceleration, fdm_data_response["z_acceleration"], 3)
        self.assertAlmostEqual(self.aircraft.gyroscope.roll_rate, fdm_data_response["roll_rate"], 3)
        self.assertAlmostEqual(self.aircraft.gyroscope.pitch_rate, fdm_data_response["pitch_rate"], 3)
        self.assertAlmostEqual(self.aircraft.gyroscope.yaw_rate, fdm_data_response["yaw_rate"], 3)
        self.assertAlmostEqual(self.aircraft.inertial_navigation_system.roll, fdm_data_response["roll"], 3)
        self.assertAlmostEqual(self.aircraft.inertial_navigation_system.pitch, fdm_data_response["pitch"], 3)
        self.assertAlmostEqual(self.aircraft.engine.rpm, fdm_data_response["engine_rpm"], 3)
        self.assertAlmostEqual(self.aircraft.engine.thrust, fdm_data_response["engine_thrust"], 3)
        self.assertAlmostEqual(self.aircraft.engine.power, fdm_data_response["engine_power"], 3)
        self.assertAlmostEqual(self.aircraft.controls.aileron, fdm_data_response["aileron"], 3)
        self.assertAlmostEqual(self.aircraft.controls.elevator, fdm_data_response["elevator"], 3)
        self.assertAlmostEqual(self.aircraft.controls.rudder, fdm_data_response["rudder"], 3)
        self.assertAlmostEqual(self.aircraft.engine.throttle, fdm_data_response["throttle"], 3)

class TestGPSData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_gps_data(self):
        resource = GPSData(self.aircraft)

        gps_data = resource.get_gps_data()

        self.assertAlmostEqual(self.aircraft.gps.latitude, gps_data["latitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.longitude, gps_data["longitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.altitude, gps_data["altitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.airspeed, gps_data["airspeed"], 3)
        self.assertAlmostEqual(self.aircraft.gps.heading, gps_data["heading"], 3)

class TestAccelerometerData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_accelerometer_data(self):
        resource = AccelerometerData(self.aircraft)

        accelerometer_data = resource.get_accelerometer_data()

        self.assertAlmostEqual(self.aircraft.accelerometer.x_acceleration, accelerometer_data["x_acceleration"], 3)
        self.assertAlmostEqual(self.aircraft.accelerometer.y_acceleration, accelerometer_data["y_acceleration"], 3)
        self.assertAlmostEqual(self.aircraft.accelerometer.z_acceleration, accelerometer_data["z_acceleration"], 3)

class TestGyroscopeData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_gyroscope_data(self):
        resource = GyroscopeData(self.aircraft)

        gyroscope_data = resource.get_gyroscope_data()

        self.assertAlmostEqual(self.aircraft.gyroscope.roll_rate, gyroscope_data["roll_rate"], 3)
        self.assertAlmostEqual(self.aircraft.gyroscope.pitch_rate, gyroscope_data["pitch_rate"], 3)
        self.assertAlmostEqual(self.aircraft.gyroscope.yaw_rate, gyroscope_data["yaw_rate"], 3)

class TestThermometerData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_thermometer_data(self):
        resource = ThermometerData(self.aircraft)

        thermometer_data = resource.get_thermometer_data()

        self.assertAlmostEqual(self.aircraft.thermometer.temperature, thermometer_data["temperature"], 3)

class TestPressureSensorData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_pressure_sensor_data(self):
        resource = PressureSensorData(self.aircraft)

        pressure_sensor_data = resource.get_pressure_sensor_data()

        self.assertAlmostEqual(self.aircraft.pressure_sensor.pressure, pressure_sensor_data["static_pressure"], 3)

class TestPitotTubeData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_pitot_tube_data(self):
        resource = PitotTubeData(self.aircraft)

        pitot_tube_data = resource.get_pitot_tube_data()

        self.assertAlmostEqual(self.aircraft.pitot_tube.pressure, pitot_tube_data["dynamic_pressure"], 3)

class TestInertialNavigationSystemData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_inertial_navigation_system_data(self):
        resource = InertialNavigationSystemData(self.aircraft)

        inertial_navigation_system_data = resource.get_inertial_navigation_system_data()

        self.assertAlmostEqual(self.aircraft.gps.latitude, inertial_navigation_system_data["latitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.longitude, inertial_navigation_system_data["longitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.altitude, inertial_navigation_system_data["altitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.airspeed, inertial_navigation_system_data["airspeed"], 3)
        self.assertAlmostEqual(self.aircraft.gps.heading, inertial_navigation_system_data["heading"], 3)
        self.assertAlmostEqual(self.aircraft.inertial_navigation_system.roll, inertial_navigation_system_data["roll"], 3)
        self.assertAlmostEqual(self.aircraft.inertial_navigation_system.pitch, inertial_navigation_system_data["pitch"], 3)

class TestEngineData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_engine_data(self):
        resource = EngineData(self.aircraft)

        engine_data = resource.get_engine_data()

        self.assertAlmostEqual(self.aircraft.engine.rpm, engine_data["engine_rpm"], 3)
        self.assertAlmostEqual(self.aircraft.engine.thrust, engine_data["engine_thrust"], 3)
        self.assertAlmostEqual(self.aircraft.engine.power, engine_data["engine_power"], 3)

class TestFlightControlsData(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        self.aircraft = Aircraft(self.fdmexec)

    def test_get_flight_controls_data(self):
        resource = FlightControlsData(self.aircraft)

        flight_controls_data = resource.get_flight_controls_data()

        self.assertAlmostEqual(self.aircraft.controls.aileron, flight_controls_data["aileron"], 3)
        self.assertAlmostEqual(self.aircraft.controls.elevator, flight_controls_data["elevator"], 3)
        self.assertAlmostEqual(self.aircraft.controls.rudder, flight_controls_data["rudder"], 3)
        self.assertAlmostEqual(self.aircraft.engine.throttle, flight_controls_data["throttle"], 3)
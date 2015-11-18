from unittest import TestCase

from mock import MagicMock, ANY

from huginn.aircraft import C172P
from huginn.http import GPSData, AccelerometerData, GyroscopeData,\
                        ThermometerData, PressureSensorData, PitotTubeData,\
                        InertialNavigationSystemData, EngineData,\
                        FlightControlsData, SimulatorControl

from mockObjects import MockRequest, MockFDMExec, MockFDMModel

class TestGPSData(TestCase):
    def test_get_gps_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = GPSData(aircraft)

        gps_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.gps.latitude, gps_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.gps.longitude, gps_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.gps.altitude, gps_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.gps.airspeed, gps_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.gps.heading, gps_data["heading"], 3)

class TestAccelerometerData(TestCase):
    def test_get_accelerometer_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = AccelerometerData(aircraft)

        accelerometer_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.accelerometer.x_acceleration, accelerometer_data["x_acceleration"], 3)
        self.assertAlmostEqual(aircraft.accelerometer.y_acceleration, accelerometer_data["y_acceleration"], 3)
        self.assertAlmostEqual(aircraft.accelerometer.z_acceleration, accelerometer_data["z_acceleration"], 3)

class TestGyroscopeData(TestCase):
    def test_get_gyroscope_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = GyroscopeData(aircraft)

        gyroscope_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.gyroscope.roll_rate, gyroscope_data["roll_rate"], 3)
        self.assertAlmostEqual(aircraft.gyroscope.pitch_rate, gyroscope_data["pitch_rate"], 3)
        self.assertAlmostEqual(aircraft.gyroscope.yaw_rate, gyroscope_data["yaw_rate"], 3)

class TestThermometerData(TestCase):
    def test_get_thermometer_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = ThermometerData(aircraft)

        thermometer_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.thermometer.temperature, thermometer_data["temperature"], 3)

class TestPressureSensorData(TestCase):
    def test_get_pressure_sensor_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = PressureSensorData(aircraft)

        pressure_sensor_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.pressure_sensor.pressure, pressure_sensor_data["static_pressure"], 3)

class TestPitotTubeData(TestCase):
    def test_get_pitot_tube_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = PitotTubeData(aircraft)

        pitot_tube_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.pitot_tube.pressure, pitot_tube_data["total_pressure"], 3)

class TestInertialNavigationSystemData(TestCase):
    def test_get_inertial_navigation_system_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = InertialNavigationSystemData(aircraft)

        inertial_navigation_system_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.gps.latitude, inertial_navigation_system_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.gps.longitude, inertial_navigation_system_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.gps.altitude, inertial_navigation_system_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.gps.airspeed, inertial_navigation_system_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.gps.heading, inertial_navigation_system_data["heading"], 3)
        self.assertAlmostEqual(aircraft.inertial_navigation_system.roll, inertial_navigation_system_data["roll"], 3)
        self.assertAlmostEqual(aircraft.inertial_navigation_system.pitch, inertial_navigation_system_data["pitch"], 3)

class TestEngineData(TestCase):
    def test_get_engine_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = EngineData(aircraft)

        engine_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.engine.thrust, engine_data["thrust"], 3)

class TestFlightControlsData(TestCase):
    def test_get_flight_controls_data(self):
        fdmexec = MockFDMExec()
        aircraft = C172P(fdmexec)

        resource = FlightControlsData(aircraft)

        flight_controls_data = resource.get_flight_data()

        self.assertAlmostEqual(aircraft.controls.aileron, flight_controls_data["aileron"], 3)
        self.assertAlmostEqual(aircraft.controls.elevator, flight_controls_data["elevator"], 3)
        self.assertAlmostEqual(aircraft.controls.rudder, flight_controls_data["rudder"], 3)
        self.assertAlmostEqual(aircraft.engine.throttle, flight_controls_data["throttle"], 3)

class TestSimulatorControl(TestCase):
    def test_pause_simulator(self):
        fdm_model = MockFDMModel()

        simulator_control_resource = SimulatorControl(fdm_model)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {"command": ["pause"]}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "pause",
                                                                          "result": "ok"})

    def test_reset_simulator(self):
        fdm_model = MockFDMModel()

        simulator_control_resource = SimulatorControl(fdm_model)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {"command": ["reset"]}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "reset",
                                                                          "result": "ok"})

    def test_resume_simulator(self):
        fdm_model = MockFDMModel()

        simulator_control_resource = SimulatorControl(fdm_model)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {"command": ["resume"]}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "resume",
                                                                          "result": "ok"})

    def test_invalid_simulator_command(self):
        fdmexec = MockFDMExec()

        simulator_control_resource = SimulatorControl(fdmexec)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {"command": ["abcdef"]}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "abcdef",
                                                                          "result": "error",
                                                                          "reason": "invalid simulator command"})

    def test_invalid_simulator_request(self):
        fdmexec = MockFDMExec()

        simulator_control_resource = SimulatorControl(fdmexec)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"result": "error",
                                                                          "reason": "invalid simulator command request"})

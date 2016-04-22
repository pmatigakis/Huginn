from unittest import TestCase

from mock import MagicMock, ANY

from huginn.simulator import Simulator
from huginn.aircraft import Aircraft
from huginn.http import GPSData, AccelerometerData, GyroscopeData,\
                        ThermometerData, PressureSensorData, PitotTubeData,\
                        InertialNavigationSystemData, EngineData,\
                        FlightControlsData, SimulatorControl, FDMData,\
                        StepSimulatorCommand, RunForSimulatorCommand,\
                        PauseSimulatorCommand, ResetSimulatorCommand,\
                        ResetSimulatorCommand, ResumeSimulatorCommand
from huginn.fdm import FDMBuilder
from huginn import configuration

from mockObjects import MockRequest

class TestGPSData(TestCase):
    def test_get_gps_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = GPSData(aircraft.instruments.gps)

        gps_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.instruments.gps.latitude, gps_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.longitude, gps_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.altitude, gps_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.airspeed, gps_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.heading, gps_data["heading"], 3)

class TestAccelerometerData(TestCase):
    def test_get_accelerometer_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = AccelerometerData(aircraft.sensors.accelerometer)

        accelerometer_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.sensors.accelerometer.x, accelerometer_data["x_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.y, accelerometer_data["y_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.z, accelerometer_data["z_acceleration"], 3)

class TestGyroscopeData(TestCase):
    def test_get_gyroscope_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = GyroscopeData(aircraft.sensors.gyroscope)

        gyroscope_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.sensors.gyroscope.roll_rate, gyroscope_data["roll_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.pitch_rate, gyroscope_data["pitch_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.yaw_rate, gyroscope_data["yaw_rate"], 3)

class TestThermometerData(TestCase):
    def test_get_thermometer_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = ThermometerData(aircraft.sensors.thermometer)

        thermometer_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.sensors.thermometer.temperature, thermometer_data["temperature"], 3)

class TestPressureSensorData(TestCase):
    def test_get_pressure_sensor_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = PressureSensorData(aircraft.sensors.pressure_sensor)

        pressure_sensor_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.sensors.pressure_sensor.pressure, pressure_sensor_data["static_pressure"], 3)

class TestPitotTubeData(TestCase):
    def test_get_pitot_tube_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = PitotTubeData(aircraft.sensors.pitot_tube)

        pitot_tube_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.sensors.pitot_tube.pressure, pitot_tube_data["total_pressure"], 3)

class TestInertialNavigationSystemData(TestCase):
    def test_get_inertial_navigation_system_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = InertialNavigationSystemData(aircraft.sensors.inertial_navigation_system)

        inertial_navigation_system_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.latitude, inertial_navigation_system_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.longitude, inertial_navigation_system_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.altitude, inertial_navigation_system_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.airspeed, inertial_navigation_system_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.heading, inertial_navigation_system_data["heading"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.roll, inertial_navigation_system_data["roll"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.pitch, inertial_navigation_system_data["pitch"], 3)

class TestEngineData(TestCase):
    def test_get_engine_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = EngineData(aircraft.engine)

        engine_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.engine.thrust, engine_data["thrust"], 3)

class TestFlightControlsData(TestCase):
    def test_get_flight_controls_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = FlightControlsData(aircraft.controls)

        flight_controls_data = resource._get_flight_data()

        self.assertAlmostEqual(aircraft.controls.aileron, flight_controls_data["aileron"], 3)
        self.assertAlmostEqual(aircraft.controls.elevator, flight_controls_data["elevator"], 3)
        self.assertAlmostEqual(aircraft.controls.rudder, flight_controls_data["rudder"], 3)
        self.assertAlmostEqual(aircraft.engine.throttle, flight_controls_data["throttle"], 3)

class TestSimulatorControl(TestCase):
    def test_pause_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        simulator_control_resource = PauseSimulatorCommand(simulator)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {"command": ["pause"]}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "pause",
                                                                          "result": "ok"})

    def test_reset_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        simulator_control_resource = ResetSimulatorCommand(simulator)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {"command": ["reset"]}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "reset",
                                                                          "result": "ok"})

    def test_resume_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        simulator_control_resource = ResumeSimulatorCommand(simulator)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {"command": ["resume"]}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "resume",
                                                                          "result": "ok"})

    def test_step_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        simulator_control_resource = StepSimulatorCommand(simulator)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        request.args = {"command": ["step"]}

        simulator_control_resource.render_POST(request)
        
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "step",
                                                                          "result": "ok"})

    def test_run_for_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)
        simulator.run_for = MagicMock()

        simulator_control_resource = RunForSimulatorCommand(simulator)

        simulator_control_resource.send_response = MagicMock()

        request = MockRequest()

        time_to_run = 1.0
        request.args = {"command": ["run_for"], "time_to_run": [time_to_run]}

        simulator_control_resource.render_POST(request)

        simulator.run_for.assert_called_once_with(time_to_run)
        simulator_control_resource.send_response.assert_called_once_with(ANY, 
                                                                         {"command": "run_for",
                                                                          "result": "ok"})

class TestFDMData(TestCase):
    def test_get_fdm_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = FDMData(fdmexec, aircraft)

        fdm_data = resource._get_flight_data()

        self.assertAlmostEqual(fdmexec.GetSimTime(), fdm_data["time"], 3)
        self.assertAlmostEqual(fdmexec.GetDeltaT(), fdm_data["dt"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.latitude, fdm_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.longitude, fdm_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.altitude, fdm_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.airspeed, fdm_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.heading, fdm_data["heading"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.x, fdm_data["x_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.y, fdm_data["y_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.z, fdm_data["z_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.roll_rate, fdm_data["roll_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.pitch_rate, fdm_data["pitch_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.yaw_rate, fdm_data["yaw_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.thermometer.temperature, fdm_data["temperature"], 3)
        self.assertAlmostEqual(aircraft.sensors.pressure_sensor.pressure, fdm_data["static_pressure"], 3)
        self.assertAlmostEqual(aircraft.sensors.pitot_tube.pressure, fdm_data["total_pressure"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.roll, fdm_data["roll"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.pitch, fdm_data["pitch"], 3)
        self.assertAlmostEqual(aircraft.engine.thrust, fdm_data["thrust"], 3)
        self.assertAlmostEqual(aircraft.controls.aileron, fdm_data["aileron"], 3)
        self.assertAlmostEqual(aircraft.controls.elevator, fdm_data["elevator"], 3)
        self.assertAlmostEqual(aircraft.controls.rudder, fdm_data["rudder"], 3)
        self.assertAlmostEqual(aircraft.engine.throttle, fdm_data["throttle"], 3)

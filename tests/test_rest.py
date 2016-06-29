from unittest import TestCase

from huginn.rest import (FDMResource, AccelerometerResource, GyroscopeResource,
                         GPSResource, ThermometerResource, PitotTubeResource,
                         PressureSensorResource, EngineResource,
                         InertialNavigationSystemResource, AircraftResource,
                         FlightControlsResource, SimulatorControlResource,
                         ObjectResource, AccelerationsResource,
                         VelocitiesResource, OrientationResource,
                         AtmosphereResource, ForcesResource,
                         InitialConditionResource, PositionResource,
                         AirspeedIndicatorResource, AltimeterResource,
                         AttitudeIndicatorResource, HeadingIndicatorResource,
                         VerticalSpeedIndicatorResource)

from huginn import configuration

from huginn.fdm import (FDMBuilder, Accelerations, Velocities, Orientation,
                        Atmosphere, Forces, InitialCondition, Position)

from huginn.aircraft import Aircraft
from huginn.simulator import Simulator
from huginn.schemas import AccelerationsSchema
from huginn.unit_conversions import convert_jsbsim_velocity

from huginn.instruments import (AirspeedIndicator, Altimeter,
                                AttitudeIndicator, HeadingIndicator,
                                VerticalSpeedIndicator)


class FDMResourceTests(TestCase):
    def test_get_fdm_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = FDMResource(fdmexec, aircraft)

        fdm_data = resource.get()

        self.assertAlmostEqual(fdmexec.GetSimTime(), fdm_data["time"], 3)
        self.assertAlmostEqual(fdmexec.GetDeltaT(), fdm_data["dt"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.latitude, fdm_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.longitude, fdm_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.altitude, fdm_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.airspeed, fdm_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.heading, fdm_data["heading"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.true_x, fdm_data["x_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.true_y, fdm_data["y_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.true_z, fdm_data["z_acceleration"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.true_roll_rate, fdm_data["roll_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.true_pitch_rate, fdm_data["pitch_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.true_yaw_rate, fdm_data["yaw_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.thermometer.true_temperature, fdm_data["temperature"], 3)
        self.assertAlmostEqual(aircraft.sensors.pressure_sensor.true_pressure, fdm_data["static_pressure"], 3)
        self.assertAlmostEqual(aircraft.sensors.pitot_tube.true_pressure, fdm_data["total_pressure"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.true_roll, fdm_data["roll"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.true_pitch, fdm_data["pitch"], 3)
        self.assertAlmostEqual(aircraft.engine.thrust, fdm_data["thrust"], 3)
        self.assertAlmostEqual(aircraft.controls.aileron, fdm_data["aileron"], 3)
        self.assertAlmostEqual(aircraft.controls.elevator, fdm_data["elevator"], 3)
        self.assertAlmostEqual(aircraft.controls.rudder, fdm_data["rudder"], 3)
        self.assertAlmostEqual(aircraft.engine.throttle, fdm_data["throttle"], 3)

        climb_rate = convert_jsbsim_velocity(-fdmexec.GetPropagate().GetVel(3))
        
        self.assertAlmostEqual(climb_rate, fdm_data["climb_rate"], 3)

class AccelerometerResourceTests(TestCase):
    def test_get_accelerometer_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = AccelerometerResource(aircraft.sensors.accelerometer)

        accelerometer_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.accelerometer.x, accelerometer_data["x"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.y, accelerometer_data["y"], 3)
        self.assertAlmostEqual(aircraft.sensors.accelerometer.z, accelerometer_data["z"], 3)

class GyroscopeResourceTests(TestCase):
    def test_get_gyroscope_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = GyroscopeResource(aircraft.sensors.gyroscope)

        gyroscope_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.gyroscope.roll_rate, gyroscope_data["roll_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.pitch_rate, gyroscope_data["pitch_rate"], 3)
        self.assertAlmostEqual(aircraft.sensors.gyroscope.yaw_rate, gyroscope_data["yaw_rate"], 3)

class GPSResourceTests(TestCase):
    def test_get_gps_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = GPSResource(aircraft.instruments.gps)

        gps_data = resource.get()

        self.assertAlmostEqual(aircraft.instruments.gps.latitude, gps_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.longitude, gps_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.altitude, gps_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.airspeed, gps_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.instruments.gps.heading, gps_data["heading"], 3)

class ThermometerResourceTests(TestCase):
    def test_get_thermometer_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = ThermometerResource(aircraft.sensors.thermometer)

        thermometer_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.thermometer.temperature, thermometer_data["temperature"], 3)

class PressureResourceTests(TestCase):
    def test_get_pressure_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = PressureSensorResource(aircraft.sensors.pressure_sensor)

        pressure_sensor_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.pressure_sensor.pressure, pressure_sensor_data["static_pressure"], 3)

class PitotTubeResourceTests(TestCase):
    def test_get_pitot_tube_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = PitotTubeResource(aircraft.sensors.pitot_tube)

        pitot_tube_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.pitot_tube.pressure, pitot_tube_data["total_pressure"], 3)

class InertialNavigationSystemResourceTests(TestCase):
    def test_get_ins_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = InertialNavigationSystemResource(aircraft.sensors.inertial_navigation_system)

        inertial_navigation_system_data = resource.get()

        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.latitude, inertial_navigation_system_data["latitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.longitude, inertial_navigation_system_data["longitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.altitude, inertial_navigation_system_data["altitude"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.airspeed, inertial_navigation_system_data["airspeed"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.heading, inertial_navigation_system_data["heading"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.roll, inertial_navigation_system_data["roll"], 3)
        self.assertAlmostEqual(aircraft.sensors.inertial_navigation_system.pitch, inertial_navigation_system_data["pitch"], 3)

class EngineResourceTests(TestCase):
    def test_get_engine_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = EngineResource(aircraft.engine)

        engine_data = resource.get()

        self.assertAlmostEqual(aircraft.engine.thrust, engine_data["thrust"], 3)

class FlightControlsResourceTests(TestCase):
    def test_get_flight_controls(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = FlightControlsResource(aircraft.controls)

        flight_controls_data = resource.get()

        self.assertAlmostEqual(aircraft.controls.aileron, flight_controls_data["aileron"], 3)
        self.assertAlmostEqual(aircraft.controls.elevator, flight_controls_data["elevator"], 3)
        self.assertAlmostEqual(aircraft.controls.rudder, flight_controls_data["rudder"], 3)
        self.assertAlmostEqual(aircraft.engine.throttle, flight_controls_data["throttle"], 3)

class SimulatorControlResourceTests(TestCase):
    def test_get_simulator_state(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.get()
        
        self.assertTrue(response["running"])
        self.assertAlmostEqual(response["dt"], configuration.DT, 3)
        self.assertAlmostEqual(response["time"], fdmexec.GetSimTime(), 3)

    def test_pause_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        self.assertFalse(simulator.is_paused())

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.execute_command("pause")

        self.assertDictEqual(response,
                             {"result": "ok",
                              "command": "pause"})

        self.assertTrue(simulator.is_paused())

    def test_resume_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)
        simulator.pause()

        self.assertTrue(simulator.is_paused())

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.execute_command("resume")

        self.assertDictEqual(response,
                             {"result": "ok",
                              "command": "resume"})

        self.assertFalse(simulator.is_paused())

    def test_step_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        start_time = simulator.simulation_time

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.execute_command("step")

        self.assertDictEqual(response,
                             {"result": "ok",
                              "command": "step"})

        self.assertGreater(simulator.simulation_time, start_time)

    def test_run_for_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        start_time = simulator.simulation_time

        simulator_control_resource = SimulatorControlResource(simulator)

        response = simulator_control_resource.execute_command("run_for", {"time_to_run": 1.0})

        self.assertDictEqual(response,
                             {"result": "ok",
                              "command": "run_for"})

        self.assertGreater(simulator.simulation_time, start_time + 1.0)

    def test_reset_simulator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        simulator = Simulator(fdmexec)

        simulator_control_resource = SimulatorControlResource(simulator)

        simulator_control_resource.execute_command("run_for", {"time_to_run": 1.0})

        start_time = simulator.simulation_time

        response = simulator_control_resource.execute_command("reset")

        self.assertDictEqual(response,
                            {"result": "ok",
                              "command": "reset"})

        self.assertAlmostEqual(simulator.simulation_time, fdmexec.GetSimTime(), 3)
        self.assertLess(simulator.simulation_time, start_time)

class AircraftResourceTests(TestCase):
    def test_get_aircraft_information(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        aircraft = Aircraft(fdmexec)

        resource = AircraftResource(aircraft)

        aircraft_data = resource.get()

        self.assertDictEqual(aircraft_data, {"type": "Rascal"})

class ObjectResourceTests(TestCase):
    def test_get_object_resource_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        accelerations = Accelerations(fdmexec)
        accelerations_schema = AccelerationsSchema()

        object_resource = ObjectResource(accelerations, accelerations_schema)

        response = object_resource.get()

        expected_result = {
            "x": accelerations.x,
            "y": accelerations.y,
            "z": accelerations.z,
            "p_dot": accelerations.p_dot,
            "q_dot": accelerations.q_dot,
            "r_dot": accelerations.r_dot,
            "u_dot": accelerations.u_dot,
            "v_dot": accelerations.v_dot,
            "w_dot": accelerations.w_dot,
            "gravity": accelerations.gravity
        }

        self.assertDictEqual(response, expected_result)

class AccelerationsResourceTests(TestCase):
    def test_get_accelerations(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        accelerations_resource = AccelerationsResource(fdmexec)

        response = accelerations_resource.get()

        accelerations = Accelerations(fdmexec)
        
        self.assertAlmostEqual(response["x"], accelerations.x, 3)
        self.assertAlmostEqual(response["y"], accelerations.y, 3)
        self.assertAlmostEqual(response["z"], accelerations.z, 3)
        self.assertAlmostEqual(response["p_dot"], accelerations.p_dot, 3)
        self.assertAlmostEqual(response["q_dot"], accelerations.q_dot, 3)
        self.assertAlmostEqual(response["r_dot"], accelerations.r_dot, 3)
        self.assertAlmostEqual(response["u_dot"], accelerations.u_dot, 3)
        self.assertAlmostEqual(response["v_dot"], accelerations.v_dot, 3)
        self.assertAlmostEqual(response["w_dot"], accelerations.w_dot, 3)
        self.assertAlmostEqual(response["gravity"], accelerations.gravity, 3)

class VelocitiesResourceTests(TestCase):
    def test_get_velocities(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        velocities_resource = VelocitiesResource(fdmexec)

        response = velocities_resource.get()

        velocities = Velocities(fdmexec)

        self.assertAlmostEqual(response["u"], velocities.u, 3)
        self.assertAlmostEqual(response["v"], velocities.v, 3)
        self.assertAlmostEqual(response["w"], velocities.w, 3)
        self.assertAlmostEqual(response["p"], velocities.p, 3)
        self.assertAlmostEqual(response["q"], velocities.q, 3)
        self.assertAlmostEqual(response["r"], velocities.r, 3)
        self.assertAlmostEqual(response["climb_rate"], velocities.climb_rate, 3)
        self.assertAlmostEqual(response["true_airspeed"], velocities.true_airspeed, 3)
        self.assertAlmostEqual(response["calibrated_airspeed"], velocities.calibrated_airspeed, 3)
        self.assertAlmostEqual(response["equivalent_airspeed"], velocities.equivalent_airspeed, 3)
        self.assertAlmostEqual(response["ground_speed"], velocities.ground_speed, 3)


class OrientationResourceTests(TestCase):
    def test_get_orientation_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        orientation_resource = OrientationResource(fdmexec)

        response = orientation_resource.get()

        orientation = Orientation(fdmexec)

        self.assertAlmostEqual(response["phi"], orientation.phi, 3)
        self.assertAlmostEqual(response["theta"], orientation.theta, 3)
        self.assertAlmostEqual(response["psi"], orientation.psi, 3)


class AtmosphereResourceTests(TestCase):
    def test_get_atmospheric_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        atmosphere_resource = AtmosphereResource(fdmexec)

        response = atmosphere_resource.get()

        atmosphere = Atmosphere(fdmexec)

        self.assertAlmostEqual(response["pressure"], atmosphere.pressure, 3)
        self.assertAlmostEqual(response["sea_level_pressure"], atmosphere.sea_level_pressure, 3)
        self.assertAlmostEqual(response["temperature"], atmosphere.temperature, 3)
        self.assertAlmostEqual(response["sea_level_temperature"], atmosphere.sea_level_temperature, 3)
        self.assertAlmostEqual(response["density"], atmosphere.density, 3)
        self.assertAlmostEqual(response["sea_level_density"], atmosphere.sea_level_density, 3)

class ForceResourceTests(TestCase):
    def test_get_forces(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        forces_resource = ForcesResource(fdmexec)

        response = forces_resource.get()

        forces = Forces(fdmexec)

        self.assertAlmostEqual(response["x_body"], forces.x_body, 3)
        self.assertAlmostEqual(response["y_body"], forces.y_body, 3)
        self.assertAlmostEqual(response["z_body"], forces.z_body, 3)
        self.assertAlmostEqual(response["x_wind"], forces.x_wind, 3)
        self.assertAlmostEqual(response["y_wind"], forces.y_wind, 3)
        self.assertAlmostEqual(response["z_wind"], forces.z_wind, 3)
        self.assertAlmostEqual(response["x_total"], forces.x_total, 3)
        self.assertAlmostEqual(response["y_total"], forces.y_total, 3)
        self.assertAlmostEqual(response["z_total"], forces.z_total, 3)

class InitialConditionResourceTests(TestCase):
    def test_get_initial_condition(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        ic_resource = InitialConditionResource(fdmexec)

        response = ic_resource.get()

        ic = InitialCondition(fdmexec)

        self.assertAlmostEqual(response["latitude"], ic.latitude, 3)
        self.assertAlmostEqual(response["longitude"], ic.longitude, 3)
        self.assertAlmostEqual(response["altitude"], ic.altitude, 3)
        self.assertAlmostEqual(response["airspeed"], ic.airspeed, 3)
        self.assertAlmostEqual(response["heading"], ic.heading, 3)

    def test_update_initial_condition(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        ic_resource = InitialConditionResource(fdmexec)
        
        new_ic = {
            "latitude": 10.0,
            "longitude": 20.0,
            "altitude": 150.0,
            "airspeed": 60.0,
            "heading": 90.0
        }

        ic_resource.update_initial_conditions(new_ic)

        response = ic_resource.get()

        self.assertAlmostEqual(response["latitude"], 10.0, 3)
        self.assertAlmostEqual(response["longitude"], 20.0, 3)
        self.assertAlmostEqual(response["altitude"], 150.0, 3)
        self.assertAlmostEqual(response["airspeed"], 60.0, 3)
        self.assertAlmostEqual(response["heading"], 90.0, 3)

class PositionResourceTests(TestCase):
    def test_get_position(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        position_resource = PositionResource(fdmexec)

        response = position_resource.get()

        position = Position(fdmexec)

        self.assertAlmostEqual(response["latitude"], position.latitude, 3)
        self.assertAlmostEqual(response["longitude"], position.longitude, 3)
        self.assertAlmostEqual(response["altitude"], position.altitude, 3)
        self.assertAlmostEqual(response["heading"], position.heading, 3)

class AirspeedIndicatorResourceTests(TestCase):
    def test_get_airspeed(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        airspeed_indicator = AirspeedIndicator(fdmexec)

        airspeed_indicator_resource = AirspeedIndicatorResource(airspeed_indicator)

        response = airspeed_indicator_resource.get()

        self.assertAlmostEqual(response["airspeed"], airspeed_indicator.airspeed, 3)

class AltimeterResourceTests(TestCase):
    def test_get_altitude(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        altimeter = Altimeter(fdmexec)

        altimeter_resource = AltimeterResource(altimeter)

        response = altimeter_resource.get()

        self.assertAlmostEqual(response["altitude"], altimeter.altitude, 3)
        self.assertAlmostEqual(response["pressure"], altimeter.pressure, 3)

class AttitudeindicatorResourceTests(TestCase):
    def test_get_attitude_indicator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        attitude_indicator = AttitudeIndicator(fdmexec)

        attitude_indicator_resource = AttitudeIndicatorResource(attitude_indicator)

        response = attitude_indicator_resource.get()

        self.assertAlmostEqual(response["roll"], attitude_indicator.roll, 3)
        self.assertAlmostEqual(response["pitch"], attitude_indicator.pitch, 3)

class HeadingindicatorResourceTests(TestCase):
    def test_get_heading_indicator_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        heading_indicator = HeadingIndicator(fdmexec)

        heading_indicator_resource = HeadingIndicatorResource(heading_indicator)

        response = heading_indicator_resource.get()

        self.assertAlmostEqual(response["heading"], heading_indicator.heading, 3)

class VertialSpeedIndicatorResourceTests(TestCase):
    def test_get_climb_rate(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        vertical_speed_indicator = VerticalSpeedIndicator(fdmexec)

        vertical_speed_indicator_resource = VerticalSpeedIndicatorResource(vertical_speed_indicator)

        response = vertical_speed_indicator_resource.get()

        self.assertAlmostEqual(response["climb_rate"], vertical_speed_indicator.climb_rate, 3)

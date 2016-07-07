import math
from unittest import TestCase

from huginn import configuration
from huginn.unit_conversions import convert_jsbsim_temperature,\
                                    convert_jsbsim_pressure,\
                                    convert_jsbsim_acceleration,\
                                    convert_jsbsim_velocity
from huginn.fdm import FDMBuilder
from huginn.sensors import Sensors, Accelerometer, Gyroscope, Thermometer,\
                           PressureSensor, PitotTube, InertialNavigationSystem

class AccelerometerTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        accelerometer = Accelerometer(fdmexec)

        self.assertAlmostEqual(accelerometer.true_x, convert_jsbsim_acceleration(fdmexec.GetAuxiliary().GetPilotAccel(1)), 3)
        self.assertAlmostEqual(accelerometer.true_y, convert_jsbsim_acceleration(fdmexec.GetAuxiliary().GetPilotAccel(2)), 3)
        self.assertAlmostEqual(accelerometer.true_z, convert_jsbsim_acceleration(fdmexec.GetAuxiliary().GetPilotAccel(3)), 3)

        self.assertAlmostEqual(accelerometer.x, accelerometer.true_x + accelerometer.x_measurement_noise, 3)
        self.assertAlmostEqual(accelerometer.y, accelerometer.true_y + accelerometer.y_measurement_noise, 3)
        self.assertAlmostEqual(accelerometer.z, accelerometer.true_z + accelerometer.z_measurement_noise, 3)

    def test_accelerometer_bias_and_noise_modification_updates(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        accelerometer = Accelerometer(fdmexec)

        accelerometer._x_measurement_noise = 0.0

        fdmexec.Run()
        
        self.assertEqual(accelerometer.x_measurement_noise, 0.0)

        #make sure the model is not paused
        fdmexec.Resume()

        run_until = fdmexec.GetSimTime() + (1.0/accelerometer.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        #self.assertAlmostEqual(accelerometer.x, accelerometer.true_x + accelerometer._x_measurement_noise, 3)

        self.assertNotEqual(accelerometer.x_measurement_noise, 0.0)

class GyroscopeTests(TestCase):
    def test_gyroscope(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        gyroscope = Gyroscope(fdmexec)

        self.assertAlmostEqual(gyroscope.true_roll_rate, math.degrees(fdmexec.GetPropagate().GetPQR(1)), 3)
        self.assertAlmostEqual(gyroscope.true_pitch_rate, math.degrees(fdmexec.GetPropagate().GetPQR(2)), 3)
        self.assertAlmostEqual(gyroscope.true_yaw_rate, math.degrees(fdmexec.GetPropagate().GetPQR(3)), 3)

        self.assertAlmostEqual(gyroscope.roll_rate, gyroscope.true_roll_rate + gyroscope._roll_rate_measurement_noise, 3)
        self.assertAlmostEqual(gyroscope.pitch_rate, gyroscope.true_pitch_rate + gyroscope._pitch_rate_measurement_noise, 3)
        self.assertAlmostEqual(gyroscope.yaw_rate, gyroscope.true_yaw_rate + gyroscope._yaw_rate_measurement_noise, 3)

    def test_gyroscope_bias_and_measurement_noise_update(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        gyroscope = Gyroscope(fdmexec)

        gyroscope._roll_rate_measurement_noise = 0.0

        fdmexec.Run()

        self.assertEqual(gyroscope.roll_rate_measurement_noise, 0.0)

        run_until = fdmexec.GetSimTime() + (1.0/gyroscope.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        self.assertNotEqual(gyroscope.roll_rate_measurement_noise, 0.0)

class ThermometerTests(TestCase):
    def test_thermometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        thermometer = Thermometer(fdmexec)

        self.assertAlmostEqual(thermometer.true_temperature, convert_jsbsim_temperature(fdmexec.GetAtmosphere().GetTemperature()))
        self.assertAlmostEqual(thermometer.temperature, thermometer.true_temperature + thermometer.measurement_noise)

    def test_thermometer_meaurement_noise_update(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        thermometer = Thermometer(fdmexec)

        thermometer._measurement_noise = 0.0

        fdmexec.Run()
        
        self.assertEqual(thermometer._measurement_noise, 0.0)
        self.assertEqual(thermometer.measurement_noise, 0.0)

        run_until = fdmexec.GetSimTime() + (1.0/thermometer.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        self.assertNotEqual(thermometer.measurement_noise, 0.0)
        self.assertEqual(thermometer.measurement_noise, thermometer._measurement_noise)

class PressureSensorTests(TestCase):
    def test_presure_sensor(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        pressure_sensor = PressureSensor(fdmexec)

        self.assertAlmostEqual(pressure_sensor.true_pressure, convert_jsbsim_pressure(fdmexec.GetAtmosphere().GetPressure()), 3)
        self.assertAlmostEqual(pressure_sensor.pressure, pressure_sensor.true_pressure + pressure_sensor.measurement_noise, 3)

    def test_pressure_sensor_meaurement_noise_update(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        pressure_sensor = PressureSensor(fdmexec)

        pressure_sensor._measurement_noise = 0.0

        fdmexec.Run()
        
        self.assertEqual(pressure_sensor._measurement_noise, 0.0)
        self.assertEqual(pressure_sensor.measurement_noise, 0.0)

        run_until = fdmexec.GetSimTime() + (1.0/pressure_sensor.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        self.assertNotEqual(pressure_sensor.measurement_noise, 0.0)
        self.assertEqual(pressure_sensor.measurement_noise, pressure_sensor._measurement_noise)

class PitotTubeTests(TestCase):
    def test_pitot_tube(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        pitot_tube = PitotTube(fdmexec)

        self.assertAlmostEqual(pitot_tube.true_pressure, convert_jsbsim_pressure(fdmexec.GetAuxiliary().GetTotalPressure()), 3)
        self.assertAlmostEqual(pitot_tube.pressure, pitot_tube.true_pressure + pitot_tube.measurement_noise, 3)

    def test_pitot_tube_meaurement_noise_update(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        pitot_tube = PitotTube(fdmexec)

        pitot_tube._measurement_noise = 0.0

        fdmexec.Run()
        
        self.assertEqual(pitot_tube._measurement_noise, 0.0)
        self.assertEqual(pitot_tube.measurement_noise, 0.0)

        run_until = fdmexec.GetSimTime() + (1.0/pitot_tube.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        self.assertNotEqual(pitot_tube.measurement_noise, 0.0)
        self.assertEqual(pitot_tube.measurement_noise, pitot_tube._measurement_noise)

class InertialNavigationSystemTests(TestCase):
    def test_inertialNavigationSystem(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        ins = InertialNavigationSystem(fdmexec)

        self.assertAlmostEqual(ins.true_roll, fdmexec.GetPropagate().GetEulerDeg(1), 3)
        self.assertAlmostEqual(ins.true_pitch, fdmexec.GetPropagate().GetEulerDeg(2), 3)
        self.assertAlmostEqual(ins.true_latitude, fdmexec.GetPropagate().GetLatitudeDeg(), 3)
        self.assertAlmostEqual(ins.true_longitude, fdmexec.GetPropagate().GetLongitudeDeg(), 3)
        self.assertAlmostEqual(ins.true_altitude, fdmexec.GetPropagate().GetAltitudeASLmeters(), 3)
        self.assertAlmostEqual(ins.true_airspeed, convert_jsbsim_velocity(fdmexec.GetAuxiliary().GetVtrueFPS()), 3)
        self.assertAlmostEqual(ins.true_heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)), 3)

        self.assertAlmostEqual(ins.roll, ins.true_roll + ins.roll_measurement_noise, 3)
        self.assertAlmostEqual(ins.pitch, ins.true_pitch + ins.pitch_measurement_noise, 3)
        self.assertAlmostEqual(ins.latitude, ins.true_latitude + ins.latitude_measurement_noise, 3)
        self.assertAlmostEqual(ins.longitude, ins.true_longitude + ins.longitude_measurement_noise, 3)
        self.assertAlmostEqual(ins.altitude, ins.true_altitude + ins.altitude_measurement_noise, 3)
        self.assertAlmostEqual(ins.airspeed, ins.true_airspeed + ins.airspeed_measurement_noise, 3)
        self.assertAlmostEqual(ins.heading, ins.true_heading + ins.heading_measurement_noise, 3)

    def test_ins_meaurement_noise_update(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        ins = InertialNavigationSystem(fdmexec)

        ins._roll_measurement_noise = 0.0
        ins._pitch_measurement_noise = 0.0
        ins._heading_measurement_noise = 0.0
        ins._latitude_measurement_noise = 0.0
        ins._longitude_measurement_noise = 0.0
        ins._altitude_measurement_noise = 0.0
        ins._airspeed_measurement_noise = 0.0

        fdmexec.Run()
        
        self.assertEqual(ins._roll_measurement_noise, 0.0)
        self.assertEqual(ins.roll_measurement_noise, 0.0)
        self.assertEqual(ins._pitch_measurement_noise, 0.0)
        self.assertEqual(ins.pitch_measurement_noise, 0.0)
        self.assertEqual(ins._heading_measurement_noise, 0.0)
        self.assertEqual(ins.heading_measurement_noise, 0.0)
        self.assertEqual(ins._latitude_measurement_noise, 0.0)
        self.assertEqual(ins.latitude_measurement_noise, 0.0)
        self.assertEqual(ins._longitude_measurement_noise, 0.0)
        self.assertEqual(ins.longitude_measurement_noise, 0.0)
        self.assertEqual(ins._airspeed_measurement_noise, 0.0)
        self.assertEqual(ins.airspeed_measurement_noise, 0.0)
        self.assertEqual(ins._altitude_measurement_noise, 0.0)
        self.assertEqual(ins.altitude_measurement_noise, 0.0)

        run_until = fdmexec.GetSimTime() + (1.0/ins.update_rate) + 1.0
        while fdmexec.GetSimTime() < run_until:
            fdmexec.Run()

        self.assertNotEqual(ins.roll_measurement_noise, 0.0)
        self.assertEqual(ins._roll_measurement_noise, ins.roll_measurement_noise)
        self.assertNotEqual(ins.pitch_measurement_noise, 0.0)
        self.assertEqual(ins._pitch_measurement_noise, ins.pitch_measurement_noise)
        self.assertNotEqual(ins.heading_measurement_noise, 0.0)
        self.assertEqual(ins._heading_measurement_noise, ins.heading_measurement_noise)
        self.assertNotEqual(ins.latitude_measurement_noise, 0.0)
        self.assertEqual(ins._latitude_measurement_noise, ins.latitude_measurement_noise)
        self.assertNotEqual(ins.longitude_measurement_noise, 0.0)
        self.assertEqual(ins._longitude_measurement_noise, ins.longitude_measurement_noise)
        self.assertNotEqual(ins.altitude_measurement_noise, 0.0)
        self.assertEqual(ins._altitude_measurement_noise, ins.altitude_measurement_noise)
        self.assertNotEqual(ins.airspeed_measurement_noise, 0.0)
        self.assertEqual(ins._airspeed_measurement_noise, ins.airspeed_measurement_noise)

class SensorTests(TestCase):
    def test_accelerometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.accelerometer.true_x, convert_jsbsim_acceleration(fdmexec.GetAuxiliary().GetPilotAccel(1)))
        self.assertAlmostEqual(sensors.accelerometer.true_y, convert_jsbsim_acceleration(fdmexec.GetAuxiliary().GetPilotAccel(2)))
        self.assertAlmostEqual(sensors.accelerometer.true_z, convert_jsbsim_acceleration(fdmexec.GetAuxiliary().GetPilotAccel(3)))

    def test_gyroscope(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.gyroscope.true_roll_rate, math.degrees(fdmexec.GetPropagate().GetPQR(1)))
        self.assertAlmostEqual(sensors.gyroscope.true_pitch_rate, math.degrees(fdmexec.GetPropagate().GetPQR(2)))
        self.assertAlmostEqual(sensors.gyroscope.true_yaw_rate, math.degrees(fdmexec.GetPropagate().GetPQR(3)))

    def test_thermometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.thermometer.true_temperature, convert_jsbsim_temperature(fdmexec.GetAtmosphere().GetTemperature()))

    def test_presure_sensor(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.pressure_sensor.true_pressure, convert_jsbsim_pressure(fdmexec.GetAtmosphere().GetPressure()))

    def test_pitot_tube(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.pitot_tube.true_pressure, convert_jsbsim_pressure(fdmexec.GetAuxiliary().GetTotalPressure()))

    def test_inertialNavigationSystem(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        sensors = Sensors(fdmexec)

        self.assertAlmostEqual(sensors.inertial_navigation_system.true_roll, fdmexec.GetPropagate().GetEulerDeg(1), 3)
        self.assertAlmostEqual(sensors.inertial_navigation_system.true_pitch, fdmexec.GetPropagate().GetEulerDeg(2), 3)
        self.assertAlmostEqual(sensors.inertial_navigation_system.true_latitude, fdmexec.GetPropagate().GetLatitudeDeg(), 3)
        self.assertAlmostEqual(sensors.inertial_navigation_system.true_longitude, fdmexec.GetPropagate().GetLongitudeDeg(), 3)
        self.assertAlmostEqual(sensors.inertial_navigation_system.true_altitude, fdmexec.GetPropagate().GetAltitudeASLmeters(), 3)
        self.assertAlmostEqual(sensors.inertial_navigation_system.true_airspeed, convert_jsbsim_velocity(fdmexec.GetAuxiliary().GetVtrueFPS()), 3)
        self.assertAlmostEqual(sensors.inertial_navigation_system.true_heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)), 3)

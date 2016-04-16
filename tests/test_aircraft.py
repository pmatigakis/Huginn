from unittest import TestCase
import math

from huginn.aircraft import Aircraft,\
                            Gyroscope, Thermometer, PressureSensor,\
                            PitotTube, InertialNavigationSystem,\
                            Engine
from huginn.fdm import FDMBuilder
from huginn import configuration
from huginn.unit_conversions import convert_feet_to_meters, convert_rankine_to_kelvin,\
                                    convert_psf_to_pascal, convert_libra_to_newtons


class GyroscopeTests(TestCase):
    def test_gyroscope(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        gyroscope = Gyroscope(fdmexec)

        self.assertAlmostEqual(gyroscope.roll_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(1)))
        self.assertAlmostEqual(gyroscope.pitch_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(2)))
        self.assertAlmostEqual(gyroscope.yaw_rate, math.degrees(fdmexec.GetAuxiliary().GetEulerRates(3)))

class ThermometerTests(TestCase):
    def test_thermometer(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        thermometer = Thermometer(fdmexec)

        self.assertAlmostEqual(thermometer.temperature, convert_rankine_to_kelvin(fdmexec.GetAtmosphere().GetTemperature()))

class PressureSensorTests(TestCase):
    def test_presure_sensor(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        pressure_sensor = PressureSensor(fdmexec)

        self.assertAlmostEqual(pressure_sensor.pressure, convert_psf_to_pascal(fdmexec.GetAtmosphere().GetPressure()))

class PitotTubeTests(TestCase):
    def test_pitot_tube(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        pitot_tube = PitotTube(fdmexec)

        self.assertAlmostEqual(pitot_tube.pressure, convert_psf_to_pascal(fdmexec.GetAuxiliary().GetTotalPressure()))

class InertialNavigationSystemTests(TestCase):
    def test_inertialNavigationSystem(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        ins = InertialNavigationSystem(fdmexec)

        self.assertAlmostEqual(ins.roll, fdmexec.GetPropagate().GetEulerDeg(1))
        self.assertAlmostEqual(ins.pitch, fdmexec.GetPropagate().GetEulerDeg(2))
        self.assertAlmostEqual(ins.latitude, fdmexec.GetPropagate().GetLatitudeDeg())
        self.assertAlmostEqual(ins.longitude, fdmexec.GetPropagate().GetLongitudeDeg())
        self.assertAlmostEqual(ins.altitude, fdmexec.GetPropagate().GetAltitudeASLmeters())
        self.assertAlmostEqual(ins.airspeed, convert_feet_to_meters(fdmexec.GetAuxiliary().GetVtrueFPS()))
        self.assertAlmostEqual(ins.heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)))

class EngineTests(TestCase):
    def test_engine(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        engine = Engine(fdmexec)

        self.assertAlmostEqual(engine.thrust, convert_libra_to_newtons(fdmexec.GetPropulsion().GetEngine(0).GetThruster().GetThrust()))
        self.assertAlmostEqual(engine.throttle, fdmexec.GetFCS().GetThrottleCmd(0))

class TestControls(TestCase):
    def test_set_aileron(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        fdmexec.GetFCS().SetDaCmd(0.678)
        
        self.assertAlmostEqual(aircraft.controls.aileron, 0.678, 3)
            
    def test_set_elevator(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        fdmexec.GetFCS().SetDeCmd(0.378)
        
        self.assertAlmostEqual(aircraft.controls.elevator, 0.378, 3)
        
    def test_set_rudder(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        fdmexec.GetFCS().SetDrCmd(0.178)
        
        self.assertAlmostEqual(aircraft.controls.rudder, 0.178, 0.0)
    
    def test_set_throttle(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        aircraft = Aircraft(fdmexec)
        
        fdmexec.GetFCS().SetThrottleCmd(0, 0.198)
        
        self.assertAlmostEqual(aircraft.controls.throttle, 0.198)

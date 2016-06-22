import math
from unittest import TestCase

from huginn import configuration
from huginn.fdm import FDMBuilder, Atmosphere

from huginn.instruments import (Instruments, GPS, true_airspeed,
                                AirspeedIndicator)

from huginn.unit_conversions import convert_jsbsim_velocity, convert_jsbsim_pressure

class GPSTests(TestCase):
    def test_gps(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        gps = GPS(fdmexec)

        self.assertAlmostEqual(gps.latitude, fdmexec.GetPropagate().GetLatitudeDeg())
        self.assertAlmostEqual(gps.longitude, fdmexec.GetPropagate().GetLongitudeDeg())
        self.assertAlmostEqual(gps.altitude, fdmexec.GetPropagate().GetAltitudeASLmeters())
        self.assertAlmostEqual(gps.airspeed, convert_jsbsim_velocity(fdmexec.GetAuxiliary().GetVtrueFPS()))
        self.assertAlmostEqual(gps.heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)))

class InstrumentsTests(TestCase):
    def test_gps(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        instruments = Instruments(fdmexec)

        self.assertAlmostEqual(instruments.gps.latitude, fdmexec.GetPropagate().GetLatitudeDeg())
        self.assertAlmostEqual(instruments.gps.longitude, fdmexec.GetPropagate().GetLongitudeDeg())
        self.assertAlmostEqual(instruments.gps.altitude, fdmexec.GetPropagate().GetAltitudeASLmeters())
        self.assertAlmostEqual(instruments.gps.airspeed, convert_jsbsim_velocity(fdmexec.GetAuxiliary().GetVtrueFPS()))
        self.assertAlmostEqual(instruments.gps.heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)))

class TrueAirspeedEquationTests(TestCase):
    def test_true_airspeed(self):
        total_pressure = 2051.465699
        static_pressure = 2042.004394
        temperature = 286.1993966667

        expected_airspeed = 53.6079420899

        calculated_airspeed = true_airspeed(total_pressure, static_pressure, temperature)

        self.assertAlmostEqual(calculated_airspeed, expected_airspeed, 1)

class AirspeedIndicatorTests(TestCase):
    def test_airspeed(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        airspeed_indicator = AirspeedIndicator(fdmexec)

        total_pressure = fdmexec.GetAuxiliary().GetTotalPressure()

        total_pressure = convert_jsbsim_pressure(total_pressure)

        atmosphere = Atmosphere(fdmexec)

        expected_airspeed = true_airspeed(total_pressure,
                                          atmosphere.pressure,
                                          atmosphere.temperature)

        self.assertAlmostEqual(airspeed_indicator.airspeed,
                               expected_airspeed,
                               3)

import math
from unittest import TestCase

from huginn import configuration
from huginn.fdm import FDMBuilder, Atmosphere, Orientation, Velocities

from huginn.instruments import (Instruments, GPS, true_airspeed,
                                AirspeedIndicator, pressure_altitude,
                                Altimeter, AttitudeIndicator, HeadingIndicator,
                                VerticalSpeedIndicator)

from huginn.unit_conversions import convert_jsbsim_velocity, convert_jsbsim_pressure, ur
from huginn.constants import p0

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

class PressureAltitudeEquationTests(TestCase):
    def test_pressure_altitude(self):
        static_pressure = 97771.6992237
        temperature = 286.1993966667

        expected_altitude = 300.0

        calculated_altitude = pressure_altitude(p0, static_pressure, temperature)

        self.assertGreater(calculated_altitude, expected_altitude - 10.0)
        self.assertLess(calculated_altitude, expected_altitude + 10.0)

class AltimeterTests(TestCase):
    def test_altitude(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        altimeter = Altimeter(fdmexec)

        atmosphere = Atmosphere(fdmexec)

        expected_altitude = pressure_altitude(atmosphere.sea_level_pressure,
                                              atmosphere.pressure,
                                              atmosphere.temperature)

        calculated_altitude = altimeter.altitude * ur.foot
        calculated_altitude.ito(ur.meter)

        self.assertAlmostEqual(calculated_altitude.magnitude,
                               expected_altitude,
                               3)

class AttitudeindicatorTest(TestCase):
    def test_get_attitude_indicator_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        attitude_indicator = AttitudeIndicator(fdmexec)

        orientation = Orientation(fdmexec)

        self.assertAlmostEqual(attitude_indicator.roll, orientation.phi, 3)
        self.assertAlmostEqual(attitude_indicator.pitch, orientation.theta, 3)

class HeadingIndicatorTests(TestCase):
    def test_get_heading_indicator_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        heading_indicator = HeadingIndicator(fdmexec)

        orientation = Orientation(fdmexec)

        self.assertAlmostEqual(heading_indicator.heading, orientation.psi, 3)

class VerticalSpeedindicatorTests(TestCase):
    def test_get_climb_rate(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        vertial_speed_indicator = VerticalSpeedIndicator(fdmexec)

        velocities = Velocities(fdmexec)

        expected_climb_rate = velocities.climb_rate * ur.meters_per_second
        expected_climb_rate.ito(ur.feet_per_minute)

        self.assertAlmostEqual(vertial_speed_indicator.climb_rate, expected_climb_rate.magnitude, 3)

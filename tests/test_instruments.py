import math
from unittest import TestCase

from huginn import configuration
from huginn.fdm import FDMBuilder
from huginn.instruments import Instruments, GPS
from huginn.unit_conversions import convert_jsbsim_velocity

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

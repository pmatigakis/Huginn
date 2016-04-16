import math
from unittest import TestCase

from huginn import configuration
from huginn.fdm import FDMBuilder
from huginn.instruments import GPS
from huginn.unit_conversions import convert_feet_to_meters

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
        self.assertAlmostEqual(gps.airspeed, convert_feet_to_meters(fdmexec.GetAuxiliary().GetVtrueFPS()))
        self.assertAlmostEqual(gps.heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)))

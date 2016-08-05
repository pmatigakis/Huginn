from unittest import TestCase, main
from argparse import ArgumentTypeError

from huginn.cli import argtypes

class LatitudeArgtypeTests(TestCase):
    def test_valid_latitude(self):
        latitude = 12.34

        arg_latitude = argtypes.latitude(latitude)

        self.assertEqual(arg_latitude, latitude)

    def test_invalid_large_latitude(self):
        latitude = 91.0

        self.assertRaises(ArgumentTypeError, argtypes.latitude, latitude)

    def test_invalid_small_latitude(self):
        latitude = -91.0

        self.assertRaises(ArgumentTypeError, argtypes.latitude, latitude)

class LongitudeArgtypeTests(TestCase):
    def test_valid_longitude(self):
        longitude = 12.34

        arg_longitude = argtypes.longitude(longitude)

        self.assertEqual(arg_longitude, longitude)

    def test_invalid_large_longitude(self):
        longitude = 181.0

        self.assertRaises(ArgumentTypeError, argtypes.longitude, longitude)

    def test_invalid_small_longitude(self):
        longitude = -181.0

        self.assertRaises(ArgumentTypeError, argtypes.longitude, longitude)

class AltitudeArgtypeTests(TestCase):
    def test_valid_altitude(self):
        altitude = 1000.0

        arg_altitude = argtypes.altitude(altitude)

        self.assertEqual(arg_altitude, altitude)

    def test_invalid_altitude(self):
        altitude = -1000.0

        self.assertRaises(ArgumentTypeError, argtypes.altitude, altitude)

class HeadingArgtypeTests(TestCase):
    def test_valid_heading(self):
        heading = 90.0

        arg_heading = argtypes.heading(heading)

        self.assertEqual(arg_heading, heading)

    def test_invalid_large_heading(self):
        heading = 361.0

        self.assertRaises(ArgumentTypeError, argtypes.heading, heading)

    def test_invalid_small_heading(self):
        heading = -1.0

        self.assertRaises(ArgumentTypeError, argtypes.heading, heading)

class AirspeedArgtypeTests(TestCase):
    def test_valid_airspeed(self):
        airspeed = 30.0

        arg_airspeed = argtypes.altitude(airspeed)

        self.assertEqual(arg_airspeed, airspeed)

    def test_invalid_airspeed(self):
        airspeed = -1.0

        self.assertRaises(ArgumentTypeError, argtypes.airspeed, airspeed)

class UpdateRateArgtypeTests(TestCase):
    def test_valid_update_rate(self):
        update_rate = 1.0/300.0

        arg_update_rate = argtypes.update_rate(update_rate)

        self.assertEqual(arg_update_rate, update_rate)

    def test_invalid_update_rate(self):
        update_rate = -0.001

        self.assertRaises(ArgumentTypeError, argtypes.update_rate, update_rate)

class TestPortNumber(TestCase):
    def test_port_number(self):
        port_number_string = "1234"

        parsed_port_number = argtypes.port_number(port_number_string)

        self.assertEqual(parsed_port_number, 1234)

    def test_fail_to_parse_invalid_port_number(self):
        port_number_string = "sdfds"

        self.assertRaises(ArgumentTypeError, argtypes.port_number, port_number_string)

    def test_fail_to_parse_invalid_port_range(self):
        port_number_string = "123456789"

        self.assertRaises(ArgumentTypeError, argtypes.port_number, port_number_string)

class TestFDMDataEndpoint(TestCase):
    def test_fdm_data_endpoint(self):
        fdm_endpoint_string = "127.0.0.1,1234,0.01"

        fdm_host, fdm_port, fdm_dt = argtypes.fdm_data_endpoint(fdm_endpoint_string)

        self.assertEqual(fdm_host, "127.0.0.1")
        self.assertEqual(fdm_port, 1234)
        self.assertAlmostEqual(fdm_dt, 0.01, 3)

    def test_fail_to_parse_invalid_fdm_endpoint(self):
        fdm_endpoint_string = "sdfds,sdffsdf,sdfdsf"

        self.assertRaises(ArgumentTypeError, argtypes.fdm_data_endpoint, fdm_endpoint_string)

    def test_fail_to_parse_invalid_fdm_endpoint_port(self):
        fdm_endpoint_string = "127.0.0.1,123456789,0.01"

        self.assertRaises(ArgumentTypeError, argtypes.fdm_data_endpoint, fdm_endpoint_string)

    def test_fail_to_parse_invalid_fdm_endpoint_dt(self):
        fdm_endpoint_string = "127.0.0.1,1234,2342"

        self.assertRaises(ArgumentTypeError, argtypes.fdm_data_endpoint, fdm_endpoint_string)

    def test_fail_to_parse_invalid_fdm_endpoint_ip(self):
        fdm_endpoint_string = "df2342,1234,0.01"

        self.assertRaises(ArgumentTypeError, argtypes.fdm_data_endpoint, fdm_endpoint_string)

if __name__ == "__main__":
    main()

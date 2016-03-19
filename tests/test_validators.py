from unittest import TestCase
from argparse import ArgumentTypeError

from huginn.validators import port_number, fdm_data_endpoint,\
                              is_valid_latitude, is_valid_longitude,\
                              is_valid_heading

class TestPortNumber(TestCase):
    def test_port_number(self):
        port_number_string = "1234"

        parsed_port_number = port_number(port_number_string)

        self.assertEqual(parsed_port_number, 1234)

    def test_fail_to_parse_invalid_port_number(self):
        port_number_string = "sdfds"

        self.assertRaises(ArgumentTypeError, port_number, port_number_string)

    def test_fail_to_parse_invalid_port_range(self):
        port_number_string = "123456789"

        self.assertRaises(ArgumentTypeError, port_number, port_number_string)

class TestFDMDataEndpoint(TestCase):
    def test_fdm_data_endpoint(self):
        fdm_endpoint_string = "127.0.0.1,1234,0.01"

        fdm_host, fdm_port, fdm_dt = fdm_data_endpoint(fdm_endpoint_string)

        self.assertEqual(fdm_host, "127.0.0.1")
        self.assertEqual(fdm_port, 1234)
        self.assertAlmostEqual(fdm_dt, 0.01, 3)

    def test_fail_to_parse_invalid_fdm_endpoint(self):
        fdm_endpoint_string = "sdfds,sdffsdf,sdfdsf"

        self.assertRaises(ArgumentTypeError, fdm_data_endpoint, fdm_endpoint_string)

    def test_fail_to_parse_invalid_fdm_endpoint_port(self):
        fdm_endpoint_string = "127.0.0.1,123456789,0.01"

        self.assertRaises(ArgumentTypeError, fdm_data_endpoint, fdm_endpoint_string)

    def test_fail_to_parse_invalid_fdm_endpoint_dt(self):
        fdm_endpoint_string = "127.0.0.1,1234,2342"

        self.assertRaises(ArgumentTypeError, fdm_data_endpoint, fdm_endpoint_string)

    def test_fail_to_parse_invalid_fdm_endpoint_ip(self):
        fdm_endpoint_string = "df2342,1234,0.01"

        self.assertRaises(ArgumentTypeError, fdm_data_endpoint, fdm_endpoint_string)

class TestLatitudeValidator(TestCase):
    def test_valid_latitude(self):
        self.assertTrue(is_valid_latitude(10.0))

    def test_invalid_latitude_greater_that_90_degrees(self):
        self.assertFalse(is_valid_latitude(100.0))

    def test_invalid_latitude_less_that_minus_90_degrees(self):
        self.assertFalse(is_valid_latitude(-100.0))

class TestLongitudeValidator(TestCase):
    def test_valid_longitude(self):
        self.assertTrue(is_valid_longitude(-10.0))

    def test_invalid_longitude_greater_that_180_degrees(self):
        self.assertFalse(is_valid_longitude(190.0))

    def test_invalid_longitude_less_that_minus_100_degrees(self):
        self.assertFalse(is_valid_longitude(-190.0))

class TestHeadingValidator(TestCase):
    def test_valid_heading(self):
        self.assertTrue(is_valid_heading(60.0))

    def test_invalid_heading_greater_that_360_degrees(self):
        self.assertFalse(is_valid_heading(370.0))

    def test_invalid_heading_less_that_0_degrees(self):
        self.assertFalse(is_valid_heading(-10.0))

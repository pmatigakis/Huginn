from unittest import TestCase
from argparse import ArgumentTypeError

from huginn.validators import port_number, fdm_data_endpoint, telemetry_endpoint

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

class TestTelemetryEndpoint(TestCase):
    def test_telemetry_endpoint(self):
        telemetry_endpoint_string = "1234,0.01"

        telemetry_port, telemetry_update_rate = telemetry_endpoint(telemetry_endpoint_string)

        self.assertEqual(telemetry_port, 1234)
        self.assertAlmostEqual(telemetry_update_rate, 0.01, 3)

    def test_fail_to_parse_invalid_telemetry_endpoint(self):
        telemetry_endpoint_string = "sdffsdf,sdfdsf"

        self.assertRaises(ArgumentTypeError, telemetry_endpoint, telemetry_endpoint_string)

    def test_fail_to_parse_invalid_fdm_endpoint_port(self):
        telemetry_endpoint_string = "123456789,0.01"

        self.assertRaises(ArgumentTypeError, telemetry_endpoint, telemetry_endpoint_string)

    def test_fail_to_parse_invalid_fdm_endpoint_dt(self):
        telemetry_endpoint_string = "1234,2342"

        self.assertRaises(ArgumentTypeError, telemetry_endpoint, telemetry_endpoint_string)

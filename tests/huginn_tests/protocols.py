from unittest import TestCase

from huginn.protocols import encode_fdm_data, decode_fdm_data

dummy_fdm_data = {
    "accelerations/a-pilot-x-ft_sec2": 1.0,
    "accelerations/a-pilot-y-ft_sec2": 2.0,
    "accelerations/a-pilot-z-ft_sec2": 3.0,
    "velocities/p-rad_sec": 4.0,
    "velocities/q-rad_sec": 5.0,
    "velocities/r-rad_sec": 6.0,
    "atmosphere/P-psf": 7.0,
    "aero/qbar-psf": 8.0,
    "atmosphere/T-R": 9.0,
    "position/lat-gc-deg": 10.0,
    "position/long-gc-deg": 11.0,
    "position/h-sl-ft": 12.0,
    "velocities/vtrue-kts": 13.0,
    "attitude/heading-true-rad": 14.0
}

class EncodingAndDecodingFDMDataTests(TestCase):
    def test_encode_and_decode_fdm_data(self):
        encoded_fdm_data = encode_fdm_data(dummy_fdm_data)
        
        decoded_fdm_data = decode_fdm_data(encoded_fdm_data)
        
        for fdm_property in dummy_fdm_data:
            self.assertAlmostEqual(decoded_fdm_data[fdm_property], dummy_fdm_data[fdm_property], 5)
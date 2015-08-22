from unittest import TestCase
import json 

from huginn.http import JSONFDMDataEncoder
from huginn.fdm import fdm_data_properties

from test_protocols import get_fdmexec 

class TestJSONFDMDataEncoder(TestCase):
    def test_encode_fdm_data(self):
        fdmexec = get_fdmexec()
        
        encoder = JSONFDMDataEncoder(fdmexec)
        
        encoded_fdm_data = encoder.encode_fdm_data(fdm_data_properties)
        
        decoded_fdm_data = json.loads(encoded_fdm_data)
        
        self.assertEqual(decoded_fdm_data.get("result", None), "ok")
        
        for fdm_property in fdm_data_properties:
            self.assertAlmostEqual(fdmexec.get_property_value(fdm_property), decoded_fdm_data["fdm_data"][fdm_property], 3)
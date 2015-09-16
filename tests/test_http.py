from unittest import TestCase
import json 

from huginn.http import JSONFDMDataEncoder
from huginn.aircraft import Aircraft

from test_common import get_fdmexec 

class TestJSONFDMDataEncoder(TestCase):
    def test_encode_fdm_data(self):
        fdmexec = get_fdmexec()
        
        aircraft = Aircraft(fdmexec)
        
        encoder = JSONFDMDataEncoder(aircraft)
        
        encoded_fdm_data = encoder.encode_fdm_data()
        
        decoded_fdm_data = json.loads(encoded_fdm_data)
        
        self.assertEqual(decoded_fdm_data.get("result", None), "ok")
        
        self.assertAlmostEqual(aircraft.thermometer.temperature, decoded_fdm_data["fdm_data"]["temperature"], 3)
        self.assertAlmostEqual(aircraft.pitot_tube.pressure, decoded_fdm_data["fdm_data"]["dynamic_pressure"], 3)
        self.assertAlmostEqual(aircraft.pressure_sensor.pressure, decoded_fdm_data["fdm_data"]["static_pressure"], 3)
        self.assertAlmostEqual(aircraft.gps.latitude, decoded_fdm_data["fdm_data"]["latitude"], 3)
        self.assertAlmostEqual(aircraft.gps.longitude, decoded_fdm_data["fdm_data"]["longitude"], 3)
        self.assertAlmostEqual(aircraft.gps.altitude, decoded_fdm_data["fdm_data"]["altitude"], 3)
        self.assertAlmostEqual(aircraft.gps.airspeed, decoded_fdm_data["fdm_data"]["airspeed"], 3)
        self.assertAlmostEqual(aircraft.gps.heading, decoded_fdm_data["fdm_data"]["heading"], 3)
        self.assertAlmostEqual(aircraft.accelerometer.x_acceleration, decoded_fdm_data["fdm_data"]["x_acceleration"], 3)
        self.assertAlmostEqual(aircraft.accelerometer.y_acceleration, decoded_fdm_data["fdm_data"]["y_acceleration"], 3)
        self.assertAlmostEqual(aircraft.accelerometer.z_acceleration, decoded_fdm_data["fdm_data"]["z_acceleration"], 3)
        self.assertAlmostEqual(aircraft.gyroscope.roll_rate, decoded_fdm_data["fdm_data"]["roll_rate"], 3)
        self.assertAlmostEqual(aircraft.gyroscope.pitch_rate, decoded_fdm_data["fdm_data"]["pitch_rate"], 3)
        self.assertAlmostEqual(aircraft.gyroscope.yaw_rate, decoded_fdm_data["fdm_data"]["yaw_rate"], 3)
        self.assertAlmostEqual(aircraft.inertial_navigation_system.roll, decoded_fdm_data["fdm_data"]["roll"], 3)
        self.assertAlmostEqual(aircraft.inertial_navigation_system.pitch, decoded_fdm_data["fdm_data"]["pitch"], 3)
from unittest import TestCase
import json 

from huginn.aircraft import Aircraft
from huginn.http import FDMData

from test_common import get_fdmexec 

class TestFDMData(TestCase):
    def setUp(self):
        fdmexec = get_fdmexec()
        self.aircraft = Aircraft(fdmexec)
    
    def test_create_fdm_data_response(self):
        fdm_data_resource = FDMData(self.aircraft)
        
        fdm_data_response = fdm_data_resource.create_fdm_data_response()
        
        self.assertAlmostEqual(self.aircraft.thermometer.temperature, fdm_data_response["temperature"], 3)
        self.assertAlmostEqual(self.aircraft.pitot_tube.pressure, fdm_data_response["dynamic_pressure"], 3)
        self.assertAlmostEqual(self.aircraft.pressure_sensor.pressure, fdm_data_response["static_pressure"], 3)
        self.assertAlmostEqual(self.aircraft.gps.latitude, fdm_data_response["latitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.longitude, fdm_data_response["longitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.altitude, fdm_data_response["altitude"], 3)
        self.assertAlmostEqual(self.aircraft.gps.airspeed, fdm_data_response["airspeed"], 3)
        self.assertAlmostEqual(self.aircraft.gps.heading, fdm_data_response["heading"], 3)
        self.assertAlmostEqual(self.aircraft.accelerometer.x_acceleration, fdm_data_response["x_acceleration"], 3)
        self.assertAlmostEqual(self.aircraft.accelerometer.y_acceleration, fdm_data_response["y_acceleration"], 3)
        self.assertAlmostEqual(self.aircraft.accelerometer.z_acceleration, fdm_data_response["z_acceleration"], 3)
        self.assertAlmostEqual(self.aircraft.gyroscope.roll_rate, fdm_data_response["roll_rate"], 3)
        self.assertAlmostEqual(self.aircraft.gyroscope.pitch_rate, fdm_data_response["pitch_rate"], 3)
        self.assertAlmostEqual(self.aircraft.gyroscope.yaw_rate, fdm_data_response["yaw_rate"], 3)
        self.assertAlmostEqual(self.aircraft.inertial_navigation_system.roll, fdm_data_response["roll"], 3)
        self.assertAlmostEqual(self.aircraft.inertial_navigation_system.pitch, fdm_data_response["pitch"], 3)
        self.assertAlmostEqual(self.aircraft.engine.rpm, fdm_data_response["engine_rpm"], 3)
        self.assertAlmostEqual(self.aircraft.engine.thrust, fdm_data_response["engine_thrust"], 3)
        self.assertAlmostEqual(self.aircraft.engine.power, fdm_data_response["engine_power"], 3)
        self.assertAlmostEqual(self.aircraft.controls.aileron, fdm_data_response["aileron"], 3)
        self.assertAlmostEqual(self.aircraft.controls.elevator, fdm_data_response["elevator"], 3)
        self.assertAlmostEqual(self.aircraft.controls.rudder, fdm_data_response["rudder"], 3)
        self.assertAlmostEqual(self.aircraft.engine.throttle, fdm_data_response["throttle"], 3)
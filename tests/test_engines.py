from unittest import TestCase

from huginn.engines import Engine
from huginn.unit_conversions import convert_pounds_to_newtons
from test_protocols import get_fdmexec

class TestEngine(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
        
    def test_rpm(self):
        engine = Engine(self.fdmexec)
        
        rpm = engine.rpm
        
        expected_rpm = self.fdmexec.get_property_value("propulsion/engine/engine-rpm")
        
        self.assertAlmostEqual(rpm, expected_rpm, 3)
        
    def test_thrust(self):
        engine = Engine(self.fdmexec)
        
        thrust = engine.thrust
        
        expected_thrust = self.fdmexec.get_property_value("propulsion/engine/thrust-lbs")
        
        expected_thrust = convert_pounds_to_newtons(expected_thrust)
        
        self.assertAlmostEqual(thrust, expected_thrust, 3)
        
    def test_power(self):
        engine = Engine(self.fdmexec)
        
        engine_power = engine.power
        
        expected_engine_power = self.fdmexec.get_property_value("propulsion/engine/power-hp")
        
        self.assertAlmostEqual(engine_power, expected_engine_power, 3)
        
    def test_get_throttle(self):
        engine = Engine(self.fdmexec)
        
        throttle = engine.throttle
        
        expected_throttle = self.fdmexec.get_property_value("fcs/throttle-cmd-norm")
        
        self.assertAlmostEqual(throttle, expected_throttle, 3)
        
    def test_set_throttle(self):
        engine = Engine(self.fdmexec)
        
        engine.throttle = 0.678
        
        throttle = self.fdmexec.get_property_value("fcs/throttle-cmd-norm")
        
        self.assertAlmostEqual(throttle, 0.678, 3)
         
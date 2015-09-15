from unittest import TestCase

from huginn.aircraft import Controls

from test_protocols import get_fdmexec

class TestControls(TestCase):
    def setUp(self):
        self.fdmexec = get_fdmexec()
    
    def test_get_aileron(self):
        controls = Controls(self.fdmexec)
        
        aileron = controls.aileron
        
        expected_aileron = self.fdmexec.get_property_value("fcs/aileron-cmd-norm")
        
        self.assertAlmostEqual(aileron, expected_aileron, 3)
    
    def test_set_aileron(self):
        controls = Controls(self.fdmexec)
        
        controls.aileron = 0.678
        
        expected_aileron = self.fdmexec.get_property_value("fcs/aileron-cmd-norm")
        
        self.assertAlmostEqual(expected_aileron, 0.678, 3)
        
    def test_get_elevator(self):
        controls = Controls(self.fdmexec)
        
        elevator = controls.elevator
        
        expected_elevator = self.fdmexec.get_property_value("fcs/elevator-cmd-norm")
        
        self.assertAlmostEqual(elevator, expected_elevator, 3)
    
    def test_set_elevator(self):
        controls = Controls(self.fdmexec)
        
        controls.elevator = 0.378
        
        expected_elevator = self.fdmexec.get_property_value("fcs/elevator-cmd-norm")
        
        self.assertAlmostEqual(expected_elevator, 0.378, 3)
        
    def test_get_rudder(self):
        controls = Controls(self.fdmexec)
        
        rudder = controls.rudder
        
        expected_rudder = self.fdmexec.get_property_value("fcs/rudder-cmd-norm")
        
        self.assertAlmostEqual(rudder, expected_rudder, 3)
    
    def test_set_rudder(self):
        controls = Controls(self.fdmexec)
        
        controls.rudder = 0.178
        
        expected_rudder = self.fdmexec.get_property_value("fcs/rudder-cmd-norm")
        
        self.assertAlmostEqual(expected_rudder, 0.178, 3)
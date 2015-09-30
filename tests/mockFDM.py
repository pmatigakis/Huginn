class MockFDMExec(object):
    def __init__(self):
        self.properties = {"fcs/aileron-cmd-norm": 0.5555,
                           "fcs/elevator-cmd-norm": 0.6666,
                           "fcs/rudder-cmd-norm": 0x1111,
                           "propulsion/engine/engine-rpm": 2011.0,
                           "propulsion/engine/thrust-lbs": 750.0,
                           "propulsion/engine/power-hp": 27.0,
                           "fcs/throttle-cmd-norm": 0.76,
                           "position/lat-gc-deg": 23.34567,
                           "position/long-gc-deg": 45.65433,
                           "velocities/vtrue-kts": 65.3,
                           "position/h-sl-ft": 1200.35,
                           "attitude/heading-true-rad": 125.43,
                           "accelerations/a-pilot-x-ft_sec2": 12.34,
                           "accelerations/a-pilot-y-ft_sec2": 13.34,
                           "accelerations/a-pilot-z-ft_sec2": 14.34,
                           "velocities/p-rad_sec": 1.234,
                           "velocities/q-rad_sec": 2.234,
                           "velocities/r-rad_sec": 3.234,
                           "atmosphere/T-R": 12345.0,
                           "atmosphere/P-psf": 456.543,
                           "aero/qbar-psf": 12.88}
    
    def get_property_value(self, property_name):
        return self.properties[property_name]
    
    def set_property_value(self, property_name, value):
        pass
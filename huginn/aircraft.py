from huginn.sensors import (GPS, Accelerometer, Gyroscope, 
                            Thermometer, PressureSensor, PitotTube,
                            InertialNavigationSystem)
from huginn.engines import Engine

class Controls(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
    @property
    def aileron(self):
        return self.fdmexec.get_property_value("fcs/aileron-cmd-norm")
    
    @aileron.setter
    def aileron(self, value):
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0 
        
        self.fdmexec.set_property_value("fcs/aileron-cmd-norm", value)

    @property
    def elevator(self):
        return self.fdmexec.get_property_value("fcs/elevator-cmd-norm")
    
    @elevator.setter
    def elevator(self, value):
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0 
        
        self.fdmexec.set_property_value("fcs/elevator-cmd-norm", value)

    @property
    def rudder(self):
        return self.fdmexec.get_property_value("fcs/rudder-cmd-norm")
    
    @rudder.setter
    def rudder(self, value):
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0 
        
        self.fdmexec.set_property_value("fcs/rudder-cmd-norm", value)

class Aircraft(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.gps = GPS(fdmexec)
        self.accelerometer = Accelerometer(fdmexec)
        self.gyroscope = Gyroscope(fdmexec)
        self.thermometer = Thermometer(fdmexec)
        self.pressure_sensor = PressureSensor(fdmexec)
        self.pitot_tube = PitotTube(fdmexec)
        self.inertial_navigation_system = InertialNavigationSystem(fdmexec)
        self.engine = Engine(fdmexec)
        self.controls = Controls(fdmexec)
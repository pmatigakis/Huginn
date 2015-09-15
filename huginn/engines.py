from huginn.unit_conversions import convert_pounds_to_newtons

class Engine(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
    @property
    def rpm(self):
        return self.fdmexec.get_property_value("propulsion/engine/engine-rpm")
    
    @property
    def thrust(self):
        thrust_in_lbs = self.fdmexec.get_property_value("propulsion/engine/thrust-lbs")
        
        return convert_pounds_to_newtons(thrust_in_lbs)
    
    @property
    def power(self):
        return self.fdmexec.get_property_value("propulsion/engine/power-hp")
    
    @property
    def throttle(self):
        return self.fdmexec.get_property_value("fcs/throttle-cmd-norm")
    
    @throttle.setter
    def throttle(self, value):
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0
            
        self.fdmexec.set_property_value("fcs/throttle-cmd-norm", value)
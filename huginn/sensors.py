"""
The hugin.sensors module contains classes that simulate the aircraft's sensors
"""

from huginn.unit_conversions import convert_feet_to_meters

class Accelerometer(object):
    """The Accelerometer class returns the acceleration forces on the body
    frame."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def x(self):
        """Return the acceleration along the x axis in meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(1))

    @property
    def y(self):
        """Return the acceleration along the y axis in meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(2))

    @property
    def z(self):
        """Return the acceleration along the z axis in meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(3))

class Sensors(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.accelerometer = Accelerometer(fdmexec)

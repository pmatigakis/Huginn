"""
The hugin.sensors module contains classes that simulate the aircraft's sensors
"""
from math import degrees

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

class Gyroscope(object):
    """The Gyroscope class contains the angular velocities measured on the body axis."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def roll_rate(self):
        """The roll rate in degrees/sec"""
        return degrees(self.fdmexec.GetAuxiliary().GetEulerRates(1))

    @property
    def pitch_rate(self):
        """The pitch rate in degrees/sec"""
        return degrees(self.fdmexec.GetAuxiliary().GetEulerRates(2))

    @property
    def yaw_rate(self):
        """The yaw rate in degrees/sec"""
        return degrees(self.fdmexec.GetAuxiliary().GetEulerRates(3))

class Sensors(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.accelerometer = Accelerometer(fdmexec)
        self.gyroscope = Gyroscope(fdmexec)

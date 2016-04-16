"""
The hugin.sensors module contains classes that simulate the aircraft's
instruments
"""

from math import degrees

from huginn.unit_conversions import convert_feet_to_meters

class GPS(object):
    """The GPS class simulates the aircraft's GPS system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def latitude(self):
        """Returns the latitude in degrees"""
        return self.fdmexec.GetPropagate().GetLatitudeDeg()

    @property
    def longitude(self):
        """Returns the longitude in degrees"""
        return self.fdmexec.GetPropagate().GetLongitudeDeg()

    @property
    def altitude(self):
        """Returns the altitude in meters"""
        return self.fdmexec.GetPropagate().GetAltitudeASLmeters()

    @property
    def airspeed(self):
        """Returns the airspeed in meters per second"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetVtrueFPS())

    @property
    def heading(self):
        """Returns the heading in degrees"""
        return degrees(self.fdmexec.GetPropagate().GetEuler(3))

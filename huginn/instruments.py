"""
The hugin.instruments module contains classes that simulate the aircraft's
instruments
"""


from math import degrees

from huginn.unit_conversions import convert_jsbsim_velocity


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
        airspeed = self.fdmexec.GetAuxiliary().GetVtrueFPS()

        return convert_jsbsim_velocity(airspeed)

    @property
    def heading(self):
        """Returns the heading in degrees"""
        return degrees(self.fdmexec.GetPropagate().GetEuler(3))


class Instruments(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.gps = GPS(fdmexec)

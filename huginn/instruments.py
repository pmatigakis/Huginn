"""
The hugin.instruments module contains classes that simulate the aircraft's
instruments
"""


from huginn.fdm import Position, Velocities


class GPS(object):
    """The GPS class simulates the aircraft's GPS system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self._position = Position(fdmexec)
        self._velocities = Velocities(fdmexec)

    @property
    def latitude(self):
        """Returns the latitude in degrees"""
        return self._position.latitude

    @property
    def longitude(self):
        """Returns the longitude in degrees"""
        return self._position.longitude

    @property
    def altitude(self):
        """Returns the altitude in meters"""
        return self._position.altitude

    @property
    def airspeed(self):
        """Returns the airspeed in meters per second"""
        return self._velocities.true_airspeed

    @property
    def heading(self):
        """Returns the heading in degrees"""
        return self._position.heading


class Instruments(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.gps = GPS(fdmexec)

"""
The hugin.instruments module contains classes that simulate the aircraft's
instruments
"""
from math import pow, sqrt

from huginn.fdm import Position, Velocities, Atmosphere
from huginn.constants import a0, T0
from huginn.unit_conversions import convert_jsbsim_pressure


def true_airspeed(total_pressure, static_pressure, temperature):
    """Calculate the true airspeed

    Arguments:
    total_pressure: the total pressure in Pascal
    static_pressure: the static pressure in Pascal
    temperature: the temperature in kelvin

    returns the airspeed in knots
    """
    impact_pressure = total_pressure - static_pressure

    t_t0 = temperature / T0
    q_p = impact_pressure / static_pressure

    return a0 * sqrt(5.0 * (pow(q_p + 1.0, 2.0/7.0) - 1.0) * t_t0)


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


class AirspeedIndicator(object):
    """The AirspeedIndicator class simulates the aircraft air speed
    indicator"""

    def __init__(self, fdmexec):
        """Create a new AirspeedIndicator object

        Arguments:
        fdmexec: a JSBSim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self._atmosphere = Atmosphere(fdmexec)

    @property
    def airspeed(self):
        """Returns the airspeed in knots"""
        total_pressure = self.fdmexec.GetAuxiliary().GetTotalPressure()

        total_pressure = convert_jsbsim_pressure(total_pressure)

        return true_airspeed(total_pressure,
                             self._atmosphere.pressure,
                             self._atmosphere.temperature)


class Instruments(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.gps = GPS(fdmexec)
        self.airspeed_indicator = AirspeedIndicator(fdmexec)

"""
The hugin.instruments module contains classes that simulate the aircraft's
instruments
"""
from math import pow, sqrt, log

from huginn.fdm import Position, Velocities, Atmosphere, Orientation
from huginn.constants import a0, T0, g, M, R
from huginn.unit_conversions import convert_jsbsim_pressure, ur


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


def pressure_altitude(sea_level_pressure, pressure, temperature):
    return log(sea_level_pressure/pressure) * ((R * temperature) / (g * M))


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
    """The AirspeedIndicator class simulates the aircraft airspeed
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


class Altimeter(object):
    """The Altimeter class simulates the aircraft altimeter"""

    def __init__(self, fdmexec):
        """Create a new Altimeter object

        Arguments:
        fdmexec: A JSBSim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self._atmosphere = Atmosphere(fdmexec)
        self._pressure = 29.92130302799185 * ur.in_Hg

    @property
    def altitude(self):
        """Return the altitude in feet"""
        sea_level_pressure = self._pressure.to(ur.pascal)

        altitude = pressure_altitude(sea_level_pressure.magnitude,
                                     self._atmosphere.pressure,
                                     self._atmosphere.temperature)

        altitude = altitude * ur.meter
        altitude.ito(ur.foot)

        return altitude.magnitude

    @property
    def pressure(self):
        """Return the instrument's pressure setting in inHg"""
        return self._pressure.magnitude

    @pressure.setter
    def pressure(self, value):
        """Set the instrument's pressure setting

        Arguments:
        value: the pressure in inHg
        """
        self._pressure = value * ur.in_Hg


class AttitudeIndicator(object):
    """The AttitudeIndicator class simulates the attitude indicator
    instrument"""

    def __init__(self, fdmexec):
        """Create a new AttitudeIndicator object

        Arguments:
        fdmexec: a JSBSim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self._orientation = Orientation(fdmexec)

    @property
    def roll(self):
        """Return the roll angle ikn degrees"""
        return self._orientation.phi

    @property
    def pitch(self):
        """Return the pitch angle in degrees"""
        return self._orientation.theta


class HeadingIndicator(object):
    """The HeadingIndicator class simulates the heading indicator
    instrument"""

    def __init__(self, fdmexec):
        """Create a new HeadingIndicator object

        Arguments:
        fdmexec: a JSBSim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self._orientation = Orientation(fdmexec)

    @property
    def heading(self):
        """Return the heading in degrees"""
        return self._orientation.psi


class VerticalSpeedIndicator(object):
    """The VerticalSpeedIndicator simulates the aircraft's vertical speed
    indicator instrument"""

    def __init__(self, fdmexec):
        """Create a new VerticalSpeedIndicator object

        Arguments:
        fdmexec: a JSBSim FGFDMExec object
        """
        self.fdmexec = fdmexec
        self._velocities = Velocities(fdmexec)

    @property
    def climb_rate(self):
        """Return the climb rate in feet per minutes"""
        climb_rate = self._velocities.climb_rate * ur.meters_per_second
        climb_rate.ito(ur.feet_per_minute)

        return climb_rate.magnitude


class Instruments(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.gps = GPS(fdmexec)
        self.airspeed_indicator = AirspeedIndicator(fdmexec)
        self.altimeter = Altimeter(fdmexec)
        self.attitude_indicator = AttitudeIndicator(fdmexec)
        self.heading_indicator = HeadingIndicator(fdmexec)
        self.vertical_speed_indicator = VerticalSpeedIndicator(fdmexec)

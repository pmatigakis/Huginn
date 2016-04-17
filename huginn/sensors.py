"""
The hugin.sensors module contains classes that simulate the aircraft's sensors
"""
from math import degrees

from huginn.unit_conversions import convert_feet_to_meters,\
                                    convert_rankine_to_kelvin,\
                                    convert_psf_to_pascal

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

class Thermometer(object):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def temperature(self):
        """return the temperature in Kelvin"""
        return convert_rankine_to_kelvin(self.fdmexec.GetAtmosphere().GetTemperature())

class PressureSensor(object):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def pressure(self):
        """Returns the pressure in Pascal"""
        return convert_psf_to_pascal(self.fdmexec.GetAtmosphere().GetPressure())

class PitotTube(object):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def pressure(self):
        """Return the pressure in pascal"""
        return convert_psf_to_pascal(self.fdmexec.GetAuxiliary().GetTotalPressure())

class InertialNavigationSystem(object):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def roll(self):
        """Return the roll angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(1)

    @property
    def pitch(self):
        """Return the pitch angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(2)

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

class Sensors(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.accelerometer = Accelerometer(fdmexec)
        self.gyroscope = Gyroscope(fdmexec)
        self.thermometer = Thermometer(fdmexec)
        self.pressure_sensor = PressureSensor(fdmexec)
        self.pitot_tube = PitotTube(fdmexec)
        self.inertial_navigation_system = InertialNavigationSystem(fdmexec)

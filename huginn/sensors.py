"""
The hugin.sensors module contains classes that simulate the aircraft's sensors
"""
from math import degrees
from random import normalvariate

from huginn.unit_conversions import convert_feet_to_meters,\
                                    convert_rankine_to_kelvin,\
                                    convert_psf_to_pascal

class Accelerometer(object):
    """The Accelerometer class returns the acceleration forces on the body
    frame.


    This class simulates an accelerometer using the following model.

    acceleration = true_acceleration + bias + measurement_noise
    """
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.update_rate = 250.0
        self.bias_sigma = 0.02
        self.bias_mu = -0.2
        self.noise_sigma = 0.005
        self.noise_mu = 0.06
        self.bias = normalvariate(self.bias_mu, self.bias_sigma)
        self._measurement_noise = normalvariate(self.noise_mu, self.noise_sigma)
        self._update_at = fdmexec.GetSimTime() + (1.0/self.update_rate)

    @property
    def measurement_noise(self):
        """The measurement noise in meters/sec^2"""
        if self.fdmexec.GetSimTime() > self._update_at:
            self._measurement_noise = normalvariate(self.noise_mu, self.noise_sigma)

            self._update_at += self.fdmexec.GetSimTime() + (1.0/self.update_rate)

        return self._measurement_noise

    @property
    def true_x(self):
        """The true acceleration along the x axis in meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(1))

    @property
    def true_y(self):
        """The true acceleration along the x axis in meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(2))

    @property
    def true_z(self):
        """The true acceleration along the x axis in meters/sec^2"""
        return convert_feet_to_meters(self.fdmexec.GetAuxiliary().GetPilotAccel(3))

    @property
    def x(self):
        """Return the acceleration along the x axis in meters/sec^2"""
        return self.true_x + self.bias + self.measurement_noise

    @property
    def y(self):
        """Return the acceleration along the y axis in meters/sec^2"""
        return self.true_y + self.bias + self.measurement_noise

    @property
    def z(self):
        """Return the acceleration along the z axis in meters/sec^2"""
        return self.true_z + self.bias + self.measurement_noise

class Gyroscope(object):
    """The Gyroscope class contains the angular velocities measured on the body axis."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.update_rate = 100.0
        self.bias_sigma = 0.0005
        self.bias_mu = 0.002
        self.noise_sigma = 0.00001
        self.noise_mu = 0.0
        self.roll_rate_bias = normalvariate(self.bias_mu, self.bias_sigma)
        self.pitch_rate_bias = normalvariate(self.bias_mu, self.bias_sigma)
        self.yaw_rate_bias = normalvariate(self.bias_mu, self.bias_sigma)
        self._roll_rate_measurement_noise = normalvariate(self.noise_mu, self.noise_sigma)
        self._pitch_rate_measurement_noise = normalvariate(self.noise_mu, self.noise_sigma)
        self._yaw_rate_measurement_noise = normalvariate(self.noise_mu, self.noise_sigma)

        self._update_at = fdmexec.GetSimTime() + (1.0/self.update_rate)

    def __update_measurements(self):
        if self.fdmexec.GetSimTime() > self._update_at:
            self._roll_rate_measurement_noise = normalvariate(self.noise_mu, self.noise_sigma)
            self._pitch_rate_measurement_noise = normalvariate(self.noise_mu, self.noise_sigma)
            self._yaw_rate_measurement_noise = normalvariate(self.noise_mu, self.noise_sigma)

            self._update_at += self.fdmexec.GetSimTime() + (1.0/self.update_rate)

    @property
    def roll_rate_measurement_noise(self):
        """The roll rate measurement noise in regrees/sec"""
        self.__update_measurements()

        return self._roll_rate_measurement_noise 

    @property
    def pitch_rate_measurement_noise(self):
        """The pitch rate measurement noise in regrees/sec"""
        self.__update_measurements()

        return self._pitch_rate_measurement_noise

    @property
    def yaw_rate_measurement_noise(self):
        """The yaw rate measurement noise in regrees/sec"""
        self.__update_measurements()

        return self._yaw_rate_measurement_noise

    @property
    def true_roll_rate(self):
        """Return the actual roll rate in degrees/sec"""
        return degrees(self.fdmexec.GetAuxiliary().GetEulerRates(1))

    @property
    def true_pitch_rate(self):
        """Return the actual pitch rate in degrees/sec"""
        return degrees(self.fdmexec.GetAuxiliary().GetEulerRates(2))

    @property
    def true_yaw_rate(self):
        """Return the actual yaw rate in degrees/sec"""
        return degrees(self.fdmexec.GetAuxiliary().GetEulerRates(3))

    @property
    def roll_rate(self):
        """The roll rate in degrees/sec"""
        return self.true_roll_rate + self.roll_rate_bias + self.roll_rate_measurement_noise

    @property
    def pitch_rate(self):
        """The pitch rate in degrees/sec"""
        return self.true_pitch_rate + self.pitch_rate_bias + self.pitch_rate_measurement_noise

    @property
    def yaw_rate(self):
        """The yaw rate in degrees/sec"""
        return self.true_yaw_rate + self.yaw_rate_bias + self.yaw_rate_measurement_noise

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

"""
The hugin.sensors module contains classes that simulate the aircraft's sensors
"""


from random import normalvariate

from huginn.unit_conversions import (convert_feet_to_meters,
                                     convert_rankine_to_kelvin,
                                     convert_psf_to_pascal)

from huginn.fdm import Velocities, Orientation, Position


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

        self._measurement_noise = normalvariate(self.noise_mu,
                                                self.noise_sigma)

        self._update_at = fdmexec.GetSimTime() + (1.0/self.update_rate)

    @property
    def measurement_noise(self):
        """The measurement noise in meters/sec^2"""
        if self.fdmexec.GetSimTime() > self._update_at:
            self._measurement_noise = normalvariate(self.noise_mu,
                                                    self.noise_sigma)

            self._update_at += (self.fdmexec.GetSimTime() +
                                (1.0/self.update_rate))

        return self._measurement_noise

    @property
    def true_x(self):
        """The true acceleration along the x axis in meters/sec^2"""
        acceleration = self.fdmexec.GetAuxiliary().GetPilotAccel(1)

        return convert_feet_to_meters(acceleration)

    @property
    def true_y(self):
        """The true acceleration along the x axis in meters/sec^2"""
        acceleration = self.fdmexec.GetAuxiliary().GetPilotAccel(2)

        return convert_feet_to_meters(acceleration)

    @property
    def true_z(self):
        """The true acceleration along the x axis in meters/sec^2"""
        acceleration = self.fdmexec.GetAuxiliary().GetPilotAccel(3)

        return convert_feet_to_meters(acceleration)

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
    """The Gyroscope class contains the angular velocities measured on the
    body axis."""
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

        self._roll_rate_measurement_noise = normalvariate(self.noise_mu,
                                                          self.noise_sigma)

        self._pitch_rate_measurement_noise = normalvariate(self.noise_mu,
                                                           self.noise_sigma)

        self._yaw_rate_measurement_noise = normalvariate(self.noise_mu,
                                                         self.noise_sigma)

        self._update_at = fdmexec.GetSimTime() + (1.0/self.update_rate)

        self._velocities = Velocities(fdmexec)

    def _update_measurements(self):
        """This function checks if the simulation time is greater than the
        time that this sensor has to update it's measurements. If it is it
        updates the measurements"""
        if self.fdmexec.GetSimTime() > self._update_at:
            self._roll_rate_measurement_noise = normalvariate(
                self.noise_mu,
                self.noise_sigma
            )

            self._pitch_rate_measurement_noise = normalvariate(
                self.noise_mu,
                self.noise_sigma
            )

            self._yaw_rate_measurement_noise = normalvariate(
                self.noise_mu,
                self.noise_sigma
            )

            self._update_at += (self.fdmexec.GetSimTime() +
                                (1.0/self.update_rate))

    @property
    def roll_rate_measurement_noise(self):
        """The roll rate measurement noise in regrees/sec"""
        self._update_measurements()

        return self._roll_rate_measurement_noise

    @property
    def pitch_rate_measurement_noise(self):
        """The pitch rate measurement noise in regrees/sec"""
        self._update_measurements()

        return self._pitch_rate_measurement_noise

    @property
    def yaw_rate_measurement_noise(self):
        """The yaw rate measurement noise in regrees/sec"""
        self._update_measurements()

        return self._yaw_rate_measurement_noise

    @property
    def true_roll_rate(self):
        """Return the actual roll rate in degrees/sec"""
        return self._velocities.p

    @property
    def true_pitch_rate(self):
        """Return the actual pitch rate in degrees/sec"""
        return self._velocities.q

    @property
    def true_yaw_rate(self):
        """Return the actual yaw rate in degrees/sec"""
        return self._velocities.r

    @property
    def roll_rate(self):
        """The roll rate in degrees/sec"""
        return (self.true_roll_rate +
                self.roll_rate_bias +
                self.roll_rate_measurement_noise)

    @property
    def pitch_rate(self):
        """The pitch rate in degrees/sec"""
        return (self.true_pitch_rate +
                self.pitch_rate_bias +
                self.pitch_rate_measurement_noise)

    @property
    def yaw_rate(self):
        """The yaw rate in degrees/sec"""
        return (self.true_yaw_rate +
                self.yaw_rate_bias +
                self.yaw_rate_measurement_noise)


class Thermometer(object):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.update_rate = 50.0
        self.bias = 0.1
        self.sigma = 0.5
        self._update_at = fdmexec.GetSimTime() + (1.0/self.update_rate)
        self._measurement_noise = self.bias + normalvariate(0.0, self.sigma)

    @property
    def measurement_noise(self):
        """Returns the measurement noise in Kelvin"""
        if self.fdmexec.GetSimTime() > self._update_at:
            self._measurement_noise = self.bias + normalvariate(0.0,
                                                                self.sigma)

        return self._measurement_noise

    @property
    def true_temperature(self):
        """return the actual temperature in Kelvin"""
        temperature = self.fdmexec.GetAtmosphere().GetTemperature()

        return convert_rankine_to_kelvin(temperature)

    @property
    def temperature(self):
        """return the temperature in Kelvin"""
        return self.true_temperature + self.measurement_noise


class PressureSensor(object):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.update_rate = 250.0
        self.bias = 100.0
        self.sigma = 10.0
        self._update_at = fdmexec.GetSimTime() + (1.0/self.update_rate)
        self._measurement_noise = self.bias + normalvariate(0.0, self.sigma)

    @property
    def measurement_noise(self):
        """Returns the measurement noise in Pascal"""
        if self.fdmexec.GetSimTime() > self._update_at:
            self._measurement_noise = self.bias + normalvariate(0.0,
                                                                self.sigma)

        return self._measurement_noise

    @property
    def true_pressure(self):
        """Returns the true pressure in Pascal"""
        pressure = self.fdmexec.GetAtmosphere().GetPressure()

        return convert_psf_to_pascal(pressure)

    @property
    def pressure(self):
        """Returns the pressure in Pascal"""
        return self.true_pressure + self.measurement_noise


class PitotTube(object):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.update_rate = 250.0
        self.bias = 100.0
        self.sigma = 10.0
        self._update_at = fdmexec.GetSimTime() + (1.0/self.update_rate)
        self._measurement_noise = self.bias + normalvariate(0.0, self.sigma)

    @property
    def measurement_noise(self):
        """Returns the measurement noise in Pascal"""
        if self.fdmexec.GetSimTime() > self._update_at:
            noise = normalvariate(0.0, self.sigma)

            self._measurement_noise = self.bias + noise

        return self._measurement_noise

    @property
    def true_pressure(self):
        """Return the true pressure in pascal"""
        pressure = self.fdmexec.GetAuxiliary().GetTotalPressure()
        return convert_psf_to_pascal(pressure)

    @property
    def pressure(self):
        """Return the pressure in pascal"""
        return self.true_pressure + self.measurement_noise


class InertialNavigationSystem(object):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.update_rate = 5.0
        self.roll_bias = 1.0
        self.roll_sigma = 0.5
        self.pitch_bias = 0.7
        self.pitch_sigma = 0.2
        self.heading_bias = 2.1
        self.heading_sigma = 0.4
        self.latitude_bias = 0.0001
        self.latitude_sigma = 0.00005
        self.longitude_bias = 0.0001
        self.longitude_sigma = 0.00005
        self.airspeed_bias = 3.0
        self.airspeed_sigma = 1.0
        self.altitude_bias = 7.0
        self.altitude_sigma = 3.0

        self._roll_measurement_noise = normalvariate(self.roll_bias,
                                                     self.roll_sigma)

        self._pitch_measurement_noise = normalvariate(self.pitch_bias,
                                                      self.pitch_sigma)

        self._heading_measurement_noise = normalvariate(self.heading_bias,
                                                        self.heading_sigma)

        self._latitude_measurement_noise = normalvariate(self.latitude_bias,
                                                         self.latitude_sigma)

        self._longitude_measurement_noise = normalvariate(
            self.longitude_bias,
            self.longitude_sigma
        )

        self._altitude_measurement_noise = normalvariate(self.altitude_bias,
                                                         self.altitude_sigma)

        self._airspeed_measurement_noise = normalvariate(self.airspeed_bias,
                                                         self.airspeed_sigma)

        self._update_at = fdmexec.GetSimTime() + (1.0/self.update_rate)

        self._velocities = Velocities(fdmexec)
        self._position = Position(fdmexec)
        self._orientation = Orientation(fdmexec)

    def _update_measurement_noise(self):
        """Check if the measurements noise needs to update and update it"""
        if self.fdmexec.GetSimTime() > self._update_at:
            self._roll_measurement_noise = normalvariate(self.roll_bias,
                                                         self.roll_sigma)

            self._pitch_measurement_noise = normalvariate(self.pitch_bias,
                                                          self.pitch_sigma)

            self._heading_measurement_noise = normalvariate(
                self.heading_bias,
                self.heading_sigma
            )

            self._latitude_measurement_noise = normalvariate(
                self.latitude_bias,
                self.latitude_sigma
            )

            self._longitude_measurement_noise = normalvariate(
                self.longitude_bias,
                self.longitude_sigma
            )

            self._altitude_measurement_noise = normalvariate(
                self.altitude_bias,
                self.altitude_sigma
            )

            self._airspeed_measurement_noise = normalvariate(
                self.airspeed_bias,
                self.airspeed_sigma
            )

            self._update_at = (self.fdmexec.GetSimTime() +
                               (1.0/self.update_rate))

    @property
    def roll_measurement_noise(self):
        """Returns the roll measurement error in degrees"""
        self._update_measurement_noise()

        return self._roll_measurement_noise

    @property
    def pitch_measurement_noise(self):
        """Returns the pitch measurement error in degrees"""
        self._update_measurement_noise()

        return self._pitch_measurement_noise

    @property
    def heading_measurement_noise(self):
        """Returns the heading measurement error in degrees"""
        self._update_measurement_noise()

        return self._heading_measurement_noise

    @property
    def latitude_measurement_noise(self):
        """Returns the latitude measurement error in degrees"""
        self._update_measurement_noise()

        return self._latitude_measurement_noise

    @property
    def longitude_measurement_noise(self):
        """Returns the longitude measurement error in degrees"""
        self._update_measurement_noise()

        return self._longitude_measurement_noise

    @property
    def airspeed_measurement_noise(self):
        """Returns the airspeed measurement error in meters/second"""
        self._update_measurement_noise()

        return self._airspeed_measurement_noise

    @property
    def altitude_measurement_noise(self):
        """Returns the altitude measurement error in meters"""
        self._update_measurement_noise()

        return self._altitude_measurement_noise

    @property
    def roll(self):
        """Returns the roll in degrees"""
        return self.true_roll + self.roll_measurement_noise

    @property
    def pitch(self):
        """Returns the pitch in degrees"""
        return self.true_pitch + self.pitch_measurement_noise

    @property
    def heading(self):
        """Returns the heading in degrees"""
        return self.true_heading + self.heading_measurement_noise

    @property
    def latitude(self):
        """Returns the latitude in degrees"""
        return self.true_latitude + self.latitude_measurement_noise

    @property
    def longitude(self):
        """Returns the longitude in degrees"""
        return self.true_longitude + self.longitude_measurement_noise

    @property
    def altitude(self):
        """Returns the altitude in meters"""
        return self.true_altitude + self.altitude_measurement_noise

    @property
    def airspeed(self):
        """Returns the airspeed in meters/second"""
        return self.true_airspeed + self.airspeed_measurement_noise

    @property
    def true_roll(self):
        """Return the true roll angle in degrees"""
        return self._orientation.phi

    @property
    def true_pitch(self):
        """Return the true pitch angle in degrees"""
        return self._orientation.theta

    @property
    def true_latitude(self):
        """Returns the true latitude in degrees"""
        return self._position.latitude

    @property
    def true_longitude(self):
        """Returns the true longitude in degrees"""
        return self._position.longitude

    @property
    def true_altitude(self):
        """Returns the true altitude in meters"""
        return self._position.altitude

    @property
    def true_airspeed(self):
        """Returns the true airspeed in meters per second"""
        return self._velocities.true_airspeed

    @property
    def true_heading(self):
        """Returns the true heading in degrees"""
        return self._position.heading


class Sensors(object):
    """The Sensors class contains all of the aircraft sensors"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.accelerometer = Accelerometer(fdmexec)
        self.gyroscope = Gyroscope(fdmexec)
        self.thermometer = Thermometer(fdmexec)
        self.pressure_sensor = PressureSensor(fdmexec)
        self.pitot_tube = PitotTube(fdmexec)
        self.inertial_navigation_system = InertialNavigationSystem(fdmexec)

"""
The hugin.sensors module contains classes that simulate the aircraft's sensors
"""
from random import normalvariate
from abc import ABCMeta, abstractmethod

from huginn.unit_conversions import convert_jsbsim_pressure
from huginn.fdm import (Velocities, Orientation, Position, Accelerations,
                        Atmosphere)


class Sensor(object):
    """The Sensor class must be implemented by any object that simulates an
    aircraft sensor"""

    __metaclass__ = ABCMeta

    def __init__(self, fdmexec, update_rate):
        """initialize the Sensor object

        Arguments:
        fdmexec: an JSBSim FGFDMExec object
        update_rate: the sensor update rate in Hz
        """
        self.fdmexec = fdmexec
        self.update_rate = update_rate
        self._update_at = 0.0

        self._update_sensor()
        self._schedule_update()

    def _schedule_update(self):
        """Set the time when the sensor data will be updated"""
        self._update_at = self.fdmexec.GetSimTime() + (1.0/self.update_rate)

    def _needs_update(self):
        """Check if the sensor data needs to be updated because the time for
        which they are valid has passed"""
        return self.fdmexec.GetSimTime() > self._update_at

    @abstractmethod
    def _update_sensor(self):
        """This method must be implemented by any subclass of the Sensor
        object"""
        raise NotImplementedError()

    @staticmethod
    def sensor_property(f):
        """The sensor_measurement decorator is used to define with properties
        are sensor measurements and updated them according to the update
        rate"""
        @property
        def wrapper(self, *args, **kwargs):
            if self._needs_update():
                self._update_sensor()
                self._schedule_update()

            return f(self, *args, **kwargs)
        return wrapper


class Accelerometer(Sensor):
    """The Accelerometer class returns the acceleration forces on the body
    frame.

    This class simulates an accelerometer using the following model.

    acceleration = true_acceleration + bias + measurement_noise
    """
    def __init__(self, fdmexec, update_rate=250.0):
        self.x_noise_mu = 0.0
        self.x_noise_sigma = 0.09
        self.y_noise_mu = 0.0
        self.y_noise_sigma = 0.09
        self.z_noise_mu = 0.0
        self.z_noise_sigma = 0.09

        self._accelerations = Accelerations(fdmexec)

        super(Accelerometer, self).__init__(fdmexec, update_rate)

    def _update_sensor(self):
        self._x_measurement_noise = normalvariate(self.x_noise_mu,
                                                  self.x_noise_sigma)

        self._y_measurement_noise = normalvariate(self.y_noise_mu,
                                                  self.y_noise_sigma)

        self._z_measurement_noise = normalvariate(self.z_noise_mu,
                                                  self.z_noise_sigma)

        self._true_x = self._accelerations.x
        self._true_y = self._accelerations.y
        self._true_z = self._accelerations.z

    @Sensor.sensor_property
    def true_x(self):
        """The true acceleration along the x axis in meters/sec^2"""
        return self._true_x

    @Sensor.sensor_property
    def true_y(self):
        """The true acceleration along the x axis in meters/sec^2"""
        return self._true_y

    @Sensor.sensor_property
    def true_z(self):
        """The true acceleration along the x axis in meters/sec^2"""
        return self._true_z

    @Sensor.sensor_property
    def x(self):
        """Return the acceleration along the x axis in meters/sec^2"""
        return self.true_x + self.x_measurement_noise

    @Sensor.sensor_property
    def y(self):
        """Return the acceleration along the y axis in meters/sec^2"""
        return self.true_y + self.y_measurement_noise

    @Sensor.sensor_property
    def z(self):
        """Return the acceleration along the z axis in meters/sec^2"""
        return self.true_z + self.z_measurement_noise

    @Sensor.sensor_property
    def x_measurement_noise(self):
        """Return the noise on the x axis in meters/sec^2"""
        return self._x_measurement_noise

    @Sensor.sensor_property
    def y_measurement_noise(self):
        """Return the noise on the y axis in meters/sec^2"""
        return self._y_measurement_noise

    @Sensor.sensor_property
    def z_measurement_noise(self):
        """Return the noise on the z axis in meters/sec^2"""
        return self._z_measurement_noise


class Gyroscope(Sensor):
    """The Gyroscope class contains the angular velocities measured on the
    body axis."""
    def __init__(self, fdmexec, update_rate=100.0):
        self.roll_rate_noise_sigma = 0.0005
        self.roll_rate_noise_mu = 0.002
        self.pitch_rate_noise_sigma = 0.0005
        self.pitch_rate_noise_mu = 0.002
        self.yaw_rate_noise_sigma = 0.0005
        self.yaw_rate_noise_mu = 0.002

        self._velocities = Velocities(fdmexec)

        super(Gyroscope, self).__init__(fdmexec, update_rate)

    def _update_sensor(self):
        self._roll_rate_measurement_noise = normalvariate(
            self.roll_rate_noise_mu,
            self.roll_rate_noise_sigma
        )

        self._pitch_rate_measurement_noise = normalvariate(
            self.pitch_rate_noise_mu,
            self.pitch_rate_noise_sigma
        )

        self._yaw_rate_measurement_noise = normalvariate(
            self.yaw_rate_noise_mu,
            self.yaw_rate_noise_sigma
        )

        self._true_roll_rate = self._velocities.p
        self._true_pitch_rate = self._velocities.q
        self._true_yaw_rate = self._velocities.r

    @Sensor.sensor_property
    def true_roll_rate(self):
        """Return the actual roll rate in degrees/sec"""
        return self._true_roll_rate

    @Sensor.sensor_property
    def true_pitch_rate(self):
        """Return the actual pitch rate in degrees/sec"""
        return self._true_pitch_rate

    @Sensor.sensor_property
    def true_yaw_rate(self):
        """Return the actual yaw rate in degrees/sec"""
        return self._true_yaw_rate

    @Sensor.sensor_property
    def roll_rate(self):
        """The roll rate in degrees/sec"""
        return (self.true_roll_rate +
                self.roll_rate_measurement_noise)

    @Sensor.sensor_property
    def pitch_rate(self):
        """The pitch rate in degrees/sec"""
        return (self.true_pitch_rate +
                self.pitch_rate_measurement_noise)

    @Sensor.sensor_property
    def yaw_rate(self):
        """The yaw rate in degrees/sec"""
        return (self.true_yaw_rate +
                self.yaw_rate_measurement_noise)

    @Sensor.sensor_property
    def roll_rate_measurement_noise(self):
        """The roll rate noise in degrees/sec"""
        return self._roll_rate_measurement_noise

    @Sensor.sensor_property
    def pitch_rate_measurement_noise(self):
        """The pitch rate noise in degrees/sec"""
        return self._pitch_rate_measurement_noise

    @Sensor.sensor_property
    def yaw_rate_measurement_noise(self):
        """The yaw rate noise in degrees/sec"""
        return self._yaw_rate_measurement_noise


class Thermometer(Sensor):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec, update_rate=50.0):
        self.mu = 0.1
        self.sigma = 0.5

        self._atmosphere = Atmosphere(fdmexec)

        super(Thermometer, self).__init__(fdmexec, update_rate)

    def _update_sensor(self):
        self._measurement_noise = normalvariate(self.mu, self.sigma)

    @Sensor.sensor_property
    def measurement_noise(self):
        """Returns the measurement noise in Kelvin"""
        return self._measurement_noise

    @Sensor.sensor_property
    def true_temperature(self):
        """return the actual temperature in Kelvin"""
        return self._atmosphere.temperature

    @Sensor.sensor_property
    def temperature(self):
        """return the temperature in Kelvin"""
        return self.true_temperature + self.measurement_noise


class PressureSensor(Sensor):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec, update_rate=250.0):
        self.mu = 100.0
        self.sigma = 10.0

        self._atmosphere = Atmosphere(fdmexec)

        super(PressureSensor, self).__init__(fdmexec, update_rate)

    def _update_sensor(self):
        self._measurement_noise = normalvariate(self.mu, self.sigma)

    @Sensor.sensor_property
    def measurement_noise(self):
        """Returns the measurement noise in Pascal"""
        return self._measurement_noise

    @Sensor.sensor_property
    def true_pressure(self):
        """Returns the true pressure in Pascal"""
        return self._atmosphere.pressure

    @Sensor.sensor_property
    def pressure(self):
        """Returns the pressure in Pascal"""
        return self.true_pressure + self.measurement_noise


class PitotTube(Sensor):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self, fdmexec, update_rate=250.0):
        self.mu = 100.0
        self.sigma = 10.0

        super(PitotTube, self).__init__(fdmexec, update_rate)

    def _update_sensor(self):
        self._measurement_noise = normalvariate(self.mu, self.sigma)

    @Sensor.sensor_property
    def measurement_noise(self):
        """Returns the measurement noise in Pascal"""
        return self._measurement_noise

    @Sensor.sensor_property
    def true_pressure(self):
        """Return the true pressure in pascal"""
        pressure = self.fdmexec.GetAuxiliary().GetTotalPressure()

        return convert_jsbsim_pressure(pressure)

    @Sensor.sensor_property
    def pressure(self):
        """Return the pressure in pascal"""
        return self.true_pressure + self.measurement_noise


class InertialNavigationSystem(Sensor):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self, fdmexec, update_rate=5.0):
        self.roll_mu = 1.0
        self.roll_sigma = 0.5
        self.pitch_mu = 0.7
        self.pitch_sigma = 0.2
        self.heading_mu = 2.1
        self.heading_sigma = 0.4
        self.latitude_mu = 0.0001
        self.latitude_sigma = 0.00005
        self.longitude_mu = 0.0001
        self.longitude_sigma = 0.00005
        self.airspeed_mu = 3.0
        self.airspeed_sigma = 1.0
        self.altitude_mu = 7.0
        self.altitude_sigma = 3.0

        self._velocities = Velocities(fdmexec)
        self._position = Position(fdmexec)
        self._orientation = Orientation(fdmexec)

        super(InertialNavigationSystem, self).__init__(fdmexec, update_rate)

    def _update_sensor(self):
        self._roll_measurement_noise = normalvariate(self.roll_mu,
                                                     self.roll_sigma)

        self._pitch_measurement_noise = normalvariate(self.pitch_mu,
                                                      self.pitch_sigma)

        self._heading_measurement_noise = normalvariate(self.heading_mu,
                                                        self.heading_sigma)

        self._latitude_measurement_noise = normalvariate(self.latitude_mu,
                                                         self.latitude_sigma)

        self._longitude_measurement_noise = normalvariate(
            self.longitude_mu,
            self.longitude_sigma
        )

        self._altitude_measurement_noise = normalvariate(self.altitude_mu,
                                                         self.altitude_sigma)

        self._airspeed_measurement_noise = normalvariate(self.airspeed_mu,
                                                         self.airspeed_sigma)

    @Sensor.sensor_property
    def roll_measurement_noise(self):
        """Returns the roll measurement error in degrees"""
        return self._roll_measurement_noise

    @Sensor.sensor_property
    def pitch_measurement_noise(self):
        """Returns the pitch measurement error in degrees"""
        return self._pitch_measurement_noise

    @Sensor.sensor_property
    def heading_measurement_noise(self):
        """Returns the heading measurement error in degrees"""
        return self._heading_measurement_noise

    @Sensor.sensor_property
    def latitude_measurement_noise(self):
        """Returns the latitude measurement error in degrees"""
        return self._latitude_measurement_noise

    @Sensor.sensor_property
    def longitude_measurement_noise(self):
        """Returns the longitude measurement error in degrees"""
        return self._longitude_measurement_noise

    @Sensor.sensor_property
    def airspeed_measurement_noise(self):
        """Returns the airspeed measurement error in meters/second"""
        return self._airspeed_measurement_noise

    @Sensor.sensor_property
    def altitude_measurement_noise(self):
        """Returns the altitude measurement error in meters"""
        return self._altitude_measurement_noise

    @Sensor.sensor_property
    def roll(self):
        """Returns the roll in degrees"""
        return self.true_roll + self.roll_measurement_noise

    @Sensor.sensor_property
    def pitch(self):
        """Returns the pitch in degrees"""
        return self.true_pitch + self.pitch_measurement_noise

    @Sensor.sensor_property
    def heading(self):
        """Returns the heading in degrees"""
        return self.true_heading + self.heading_measurement_noise

    @Sensor.sensor_property
    def latitude(self):
        """Returns the latitude in degrees"""
        return self.true_latitude + self.latitude_measurement_noise

    @Sensor.sensor_property
    def longitude(self):
        """Returns the longitude in degrees"""
        return self.true_longitude + self.longitude_measurement_noise

    @Sensor.sensor_property
    def altitude(self):
        """Returns the altitude in meters"""
        return self.true_altitude + self.altitude_measurement_noise

    @Sensor.sensor_property
    def airspeed(self):
        """Returns the airspeed in meters/second"""
        return self.true_airspeed + self.airspeed_measurement_noise

    @Sensor.sensor_property
    def true_roll(self):
        """Return the true roll angle in degrees"""
        return self._orientation.phi

    @Sensor.sensor_property
    def true_pitch(self):
        """Return the true pitch angle in degrees"""
        return self._orientation.theta

    @Sensor.sensor_property
    def true_latitude(self):
        """Returns the true latitude in degrees"""
        return self._position.latitude

    @Sensor.sensor_property
    def true_longitude(self):
        """Returns the true longitude in degrees"""
        return self._position.longitude

    @Sensor.sensor_property
    def true_altitude(self):
        """Returns the true altitude in meters"""
        return self._position.altitude

    @Sensor.sensor_property
    def true_airspeed(self):
        """Returns the true airspeed in meters per second"""
        return self._velocities.true_airspeed

    @Sensor.sensor_property
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

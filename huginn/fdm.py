"""
The huginn.fdm module contains classes and functions that can be used to
initialize the flight dynamics model and create a model for a simulated
aircraft
"""


from math import degrees
import logging

from PyJSBSim import FGFDMExec

from huginn import configuration
from huginn.unit_conversions import (convert_jsbsim_acceleration,
                                     convert_jsbsim_angular_acceleration,
                                     convert_jsbsim_angular_velocity,
                                     convert_jsbsim_velocity,
                                     convert_jsbsim_pressure,
                                     convert_jsbsim_temperature,
                                     convert_jsbsim_density,
                                     convert_jsbsim_force,
                                     ur)


logger = logging.getLogger(__name__)


class FDMBuilder(object):
    """The FDMBuilder creates the flight dynamics model object that will be
    used by the simulator"""
    def __init__(self, data_path):
        self.data_path = data_path
        self.dt = configuration.DT

        self.aircraft = configuration.AIRCRAFT

        self.latitude = configuration.LATITUDE
        self.longitude = configuration.LONGITUDE
        self.altitude = configuration.ALTITUDE
        self.airspeed = configuration.AIRSPEED
        self.heading = configuration.HEADING

    def create_fdm(self):
        """Create the flight dynamics model"""

        fdmexec = FGFDMExec()

        logger.debug("Using jsbsim data at %s", self.data_path)

        fdmexec.SetRootDir(self.data_path)
        fdmexec.SetAircraftPath("")
        fdmexec.SetEnginePath(self.data_path + "/Engines")
        fdmexec.SetSystemsPath(self.data_path + "/Systems")

        logger.debug("JSBSim dt is %f", self.dt)
        fdmexec.Setdt(self.dt)

        fdmexec.LoadModel("Rascal")

        altitude = self.altitude * ur.meter
        altitude.ito(ur.foot)

        altitude_in_feet = altitude.magnitude

        airspeed = self.airspeed * ur.meters_per_second
        airspeed.ito(ur.knot)

        airspeed_in_knots = airspeed.magnitude

        logger.debug("Initial latitude: %f degrees", self.latitude)
        logger.debug("Initial longitude: %f degrees", self.longitude)
        logger.debug("Initial altitude: %f meters", self.altitude)
        logger.debug("Initial airspeed: %f meters/second", self.airspeed)
        logger.debug("Initial heading: %f degrees", self.heading)

        fdmexec.GetIC().SetLatitudeDegIC(self.latitude)
        fdmexec.GetIC().SetLongitudeDegIC(self.longitude)
        fdmexec.GetIC().SetAltitudeASLFtIC(altitude_in_feet)
        fdmexec.GetIC().SetPsiDegIC(self.heading)
        fdmexec.GetIC().SetVtrueKtsIC(airspeed_in_knots)

        if not fdmexec.RunIC():
            logger.error("Failed to run initial condition")
            return None

        # Run the simulation for 1 second in order to make sure that
        # everything is ok
        while fdmexec.GetSimTime() < 1.0:
            fdmexec.ProcessMessage()
            fdmexec.CheckIncrementalHold()

            if not fdmexec.Run():
                logger.error("Failed to execute initial run")
                return None

        fdmexec.PrintSimulationConfiguration()

        fdmexec.GetPropagate().DumpState()

        return fdmexec


class Accelerations(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def x(self):
        """Returns the acceleration along the x axis of the aircraft in
        meters/sec^2"""
        acceleration = self.fdmexec.GetAuxiliary().GetPilotAccel(1)

        return convert_jsbsim_acceleration(acceleration)

    @property
    def y(self):
        """Returns the acceleration along the y axis of the aircraft in
        meters/sec^2"""
        acceleration = self.fdmexec.GetAuxiliary().GetPilotAccel(2)

        return convert_jsbsim_acceleration(acceleration)

    @property
    def z(self):
        """Returns the acceleration along the z axis of the aircraft in
        meters/sec^2"""
        acceleration = self.fdmexec.GetAuxiliary().GetPilotAccel(3)

        return convert_jsbsim_acceleration(acceleration)

    @property
    def p_dot(self):
        """Returns the p value of the body axis angular acceleration in
        degress/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetPQRdot(1)

        return convert_jsbsim_angular_acceleration(acceleration)

    @property
    def q_dot(self):
        """Returns the q value of the body axis angular acceleration in
        degress/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetPQRdot(2)

        return convert_jsbsim_angular_acceleration(acceleration)

    @property
    def r_dot(self):
        """Returns the r value of the body axis angular acceleration in
        degress/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetPQRdot(3)

        return convert_jsbsim_angular_acceleration(acceleration)

    @property
    def u_dot(self):
        """Returns the u item of the the body axis acceleration in
        meters/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetUVWdot(1)

        return convert_jsbsim_acceleration(acceleration)

    @property
    def v_dot(self):
        """Returns the v item of the the body axis acceleration in
        meters/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetUVWdot(2)

        return convert_jsbsim_acceleration(acceleration)

    @property
    def w_dot(self):
        """Returns the w item of the the body axis acceleration in
        meters/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetUVWdot(3)

        return convert_jsbsim_acceleration(acceleration)

    @property
    def gravity(self):
        """Returns the acceleration of the gravity in meters/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetGravAccelMagnitude()

        return convert_jsbsim_acceleration(acceleration)


class Velocities(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def p(self):
        """Return the p item of the body angular rates in degrees/sec"""
        velocity = self.fdmexec.GetPropagate().GetPQR(1)

        return convert_jsbsim_angular_velocity(velocity)

    @property
    def q(self):
        """Return the q item of the body angular rates in degrees/sec"""
        velocity = self.fdmexec.GetPropagate().GetPQR(2)

        return convert_jsbsim_angular_velocity(velocity)

    @property
    def r(self):
        """Return the r item of the body angular rates in degrees/sec"""
        velocity = self.fdmexec.GetPropagate().GetPQR(3)

        return convert_jsbsim_angular_velocity(velocity)

    @property
    def true_airspeed(self):
        """Return the true airspeed in meters/second"""
        airspeed = self.fdmexec.GetAuxiliary().GetVtrueFPS()

        return convert_jsbsim_velocity(airspeed)

    @property
    def climb_rate(self):
        """Return the vertical velocity in meters/seconds"""
        # climb_rate = self.fdmexec.GetPropertyValue("velocities/v-down-fps")
        climb_rate = -self.fdmexec.GetPropagate().GetVel(3)

        return convert_jsbsim_velocity(climb_rate)

    @property
    def u(self):
        """Returns the u item of the body frame velocity vector in
        meters/sec"""
        velocity = self.fdmexec.GetPropagate().GetUVW(1)

        return convert_jsbsim_velocity(velocity)

    @property
    def v(self):
        """Returns the v item of the body frame velocity vector in
        meters/sec"""
        velocity = self.fdmexec.GetPropagate().GetUVW(2)

        return convert_jsbsim_velocity(velocity)

    @property
    def w(self):
        """Returns the w item of the body frame velocity vector in
        meters/sec"""
        velocity = self.fdmexec.GetPropagate().GetUVW(3)

        return convert_jsbsim_velocity(velocity)

    @property
    def calibrated_airspeed(self):
        """Returns the calibrated airspeed in meters/sec"""
        airspeed = self.fdmexec.GetAuxiliary().GetVcalibratedFPS()

        return convert_jsbsim_velocity(airspeed)

    @property
    def equivalent_airspeed(self):
        """Returns the equivalent airspeed in meters/sec"""
        airspeed = self.fdmexec.GetAuxiliary().GetVequivalentFPS()

        return convert_jsbsim_velocity(airspeed)

    @property
    def ground_speed(self):
        """Returns the ground speed in meters/sec"""
        airspeed = self.fdmexec.GetAuxiliary().GetVground()

        return convert_jsbsim_velocity(airspeed)


class Position(object):
    """The Position class contains data about the position of the aircraft"""
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
    def heading(self):
        """Returns the heading in degrees"""
        return degrees(self.fdmexec.GetPropagate().GetEuler(3))


class Orientation(object):
    """The Orientation class contains data about the orientation of the
    aircraft"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def phi(self):
        """Return the phi euler angle angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(1)

    @property
    def theta(self):
        """Return the theta euler angle angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(2)

    @property
    def psi(self):
        """Return the psi euler angle angle in degrees"""
        return self.fdmexec.GetPropagate().GetEulerDeg(3)


class Atmosphere(object):
    """The Atmosphere contains the fdm data about the atmosphere"""

    def __init__(self, fdmexec):
        """Create a new Atmosphere object

        Arguments:
        fdmexec: a JSBSim FGFDMExec object
        """
        self.fdmexec = fdmexec

    @property
    def pressure(self):
        """Returns the pressure at the current altitude. The value will be in
        Pascal"""
        pressure = self.fdmexec.GetAtmosphere().GetPressure()

        return convert_jsbsim_pressure(pressure)

    @property
    def sea_level_pressure(self):
        """Returns the pressure at the sea level. The value will be in
        Pascal"""
        pressure = self.fdmexec.GetAtmosphere().GetPressureSL()

        return convert_jsbsim_pressure(pressure)

    @property
    def temperature(self):
        """Returns the temperature in kelvin at the current altitude"""
        temperature = self.fdmexec.GetAtmosphere().GetTemperature()

        return convert_jsbsim_temperature(temperature)

    @property
    def sea_level_temperature(self):
        """Returns the temperature in kelvin at the sea level"""
        temperature = self.fdmexec.GetAtmosphere().GetTemperatureSL()

        return convert_jsbsim_temperature(temperature)

    @property
    def density(self):
        """Returns the atmospheric density at the current altitude in
        kg/meters^3"""
        density = self.fdmexec.GetAtmosphere().GetDensity()

        return convert_jsbsim_density(density)

    @property
    def sea_level_density(self):
        """Returns the atmospheric density at sea level in kg/meters^3"""
        density = self.fdmexec.GetAtmosphere().GetDensitySL()

        return convert_jsbsim_density(density)


class Forces(object):
    """The Forces objects contains the aerodynamics forces"""

    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def x_body(self):
        """Return the force along the x axis in the body frame. The value
        is in Newtons"""
        force = self.fdmexec.GetAerodynamics().GetForces(1)

        return convert_jsbsim_force(force)

    @property
    def y_body(self):
        """Return the force along the y axis in the body frame. The value
        is in Newtons"""
        force = self.fdmexec.GetAerodynamics().GetForces(2)

        return convert_jsbsim_force(force)

    @property
    def z_body(self):
        """Return the force along the z axis in the body frame. The value
        is in Newtons"""
        force = self.fdmexec.GetAerodynamics().GetForces(3)

        return convert_jsbsim_force(force)

    @property
    def x_wind(self):
        """Return the force along the x axis in the wind frame. The value
        is in Newtons"""
        force = self.fdmexec.GetAerodynamics().GetvFw(1)

        return convert_jsbsim_force(force)

    @property
    def y_wind(self):
        """Return the force along the y axis in the wind frame. The value
        is in Newtons"""
        force = self.fdmexec.GetAerodynamics().GetvFw(2)

        return convert_jsbsim_force(force)

    @property
    def z_wind(self):
        """Return the force along the z axis in the wind frame. The value
        is in Newtons"""
        force = self.fdmexec.GetAerodynamics().GetvFw(3)

        return convert_jsbsim_force(force)

    @property
    def x_total(self):
        """Return the total force along the x axis in the body frame. The
        value is in Newtons"""
        force = self.fdmexec.GetAccelerations().GetForces(1)

        return convert_jsbsim_force(force)

    @property
    def y_total(self):
        """Return the total force along the y axis in the body frame. The
        value is in Newtons"""
        force = self.fdmexec.GetAccelerations().GetForces(2)

        return convert_jsbsim_force(force)

    @property
    def z_total(self):
        """Return the total force along the z axis in the body frame. The
        value is in Newtons"""
        force = self.fdmexec.GetAccelerations().GetForces(3)

        return convert_jsbsim_force(force)


class InitialCondition(object):
    """The InitialCondition class gets/sets the simulator initial conditions"""

    def __init__(self, fdmexec):
        """Create a new InitialCondition object

        Arguments:
        fdmexec: a JSBSim FGFDMExec object
        """
        self.fdmexec = fdmexec

    @property
    def latitude(self):
        """Get the starting position latitude in degrees"""
        return self.fdmexec.GetIC().GetLatitudeDegIC()

    @latitude.setter
    def latitude(self, value):
        """Set the starting position latitude

        Arguments:
        value: the latitude in degrees
        """
        self.fdmexec.GetIC().SetLatitudeDegIC(value)

    @property
    def longitude(self):
        """Get the starting position longitude in degrees"""
        return self.fdmexec.GetIC().GetLongitudeDegIC()

    @longitude.setter
    def longitude(self, value):
        """Set the starting position longitude

        Arguments:
        value: the longitude in degrees
        """

        self.fdmexec.GetIC().SetLongitudeDegIC(value)

    @property
    def altitude(self):
        """Get the altitude in meters"""
        altitude = self.fdmexec.GetIC().GetAltitudeASLFtIC() * ur.foot

        altitude.ito(ur.meter)

        return altitude.magnitude

    @altitude.setter
    def altitude(self, value):
        """Set the starting altitude

        Arguments:
        value: the altitude in meters
        """
        altitude = value * ur.meter

        altitude.ito(ur.foot)

        self.fdmexec.GetIC().SetAltitudeASLFtIC(altitude.magnitude)

    @property
    def heading(self):
        """Get the heading in degrees"""
        return self.fdmexec.GetIC().GetPsiDegIC()

    @heading.setter
    def heading(self, value):
        """Set the heading

        Arguments:
        value: the heading in degrees
        """
        self.fdmexec.GetIC().SetPsiDegIC(value)

    @property
    def airspeed(self):
        """Get the airspeed in meters/second"""
        airspeed = self.fdmexec.GetIC().GetVtrueKtsIC() * ur.knot

        airspeed.ito(ur.meters_per_second)

        return airspeed.magnitude

    @airspeed.setter
    def airspeed(self, value):
        """Set the airspeed

        Arguments:
        value: the airspeed in meters/second
        """
        airspeed = value * ur.meters_per_second

        airspeed.ito(ur.knot)

        self.fdmexec.GetIC().SetVtrueKtsIC(airspeed.magnitude)


class FDM(object):
    """The FDM object is a wrapper around the JSBSim objects that contains the
    values of the flight dynamics model."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.accelerations = Accelerations(fdmexec)
        self.velocities = Velocities(fdmexec)
        self.position = Position(fdmexec)
        self.orientation = Orientation(fdmexec)
        self.atmosphere = Atmosphere(fdmexec)
        self.forces = Forces(fdmexec)
        self.initial_condition = InitialCondition(fdmexec)

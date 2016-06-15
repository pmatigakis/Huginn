"""
The huginn.fdm module contains classes and functions that can be used to
initialize the flight dynamics model and create a model for a simulated
aircraft
"""


from math import degrees
import logging

from PyJSBSim import FGFDMExec

from huginn import configuration
from huginn.unit_conversions import (convert_meters_to_feet,
                                     convert_meters_per_sec_to_knots,
                                     convert_feet_to_meters)


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

        self.logger = logging.getLogger("huginn")

    def create_fdm(self):
        """Create the flight dynamics model"""

        fdmexec = FGFDMExec()

        self.logger.debug("Using jsbsim data at %s", self.data_path)

        fdmexec.SetRootDir(self.data_path)
        fdmexec.SetAircraftPath("")
        fdmexec.SetEnginePath(self.data_path + "/Engines")
        fdmexec.SetSystemsPath(self.data_path + "/Systems")

        self.logger.debug("JSBSim dt is %f", self.dt)
        fdmexec.Setdt(self.dt)

        fdmexec.LoadModel("Rascal")

        altitude_in_feet = convert_meters_to_feet(self.altitude)
        airspeed_in_knots = convert_meters_per_sec_to_knots(self.airspeed)

        self.logger.debug("Initial latitude: %f degrees", self.latitude)
        self.logger.debug("Initial longitude: %f degrees", self.longitude)
        self.logger.debug("Initial altitude: %f meters", self.altitude)
        self.logger.debug("Initial airspeed: %f meters/second", self.airspeed)
        self.logger.debug("Initial heading: %f degrees", self.heading)

        fdmexec.GetIC().SetLatitudeDegIC(self.latitude)
        fdmexec.GetIC().SetLongitudeDegIC(self.longitude)
        fdmexec.GetIC().SetAltitudeASLFtIC(altitude_in_feet)
        fdmexec.GetIC().SetPsiDegIC(self.heading)
        fdmexec.GetIC().SetVtrueKtsIC(airspeed_in_knots)

        if not fdmexec.RunIC():
            self.logger.error("Failed to run initial condition")
            return None

        # Run the simulation for 1 second in order to make sure that
        # everything is ok
        while fdmexec.GetSimTime() < 1.0:
            fdmexec.ProcessMessage()
            fdmexec.CheckIncrementalHold()

            if not fdmexec.Run():
                self.logger.error("Failed to execute initial run")
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

        return convert_feet_to_meters(acceleration)

    @property
    def y(self):
        """Returns the acceleration along the y axis of the aircraft in
        meters/sec^2"""
        acceleration = self.fdmexec.GetAuxiliary().GetPilotAccel(2)

        return convert_feet_to_meters(acceleration)

    @property
    def z(self):
        """Returns the acceleration along the z axis of the aircraft in
        meters/sec^2"""
        acceleration = self.fdmexec.GetAuxiliary().GetPilotAccel(3)

        return convert_feet_to_meters(acceleration)

    @property
    def p_dot(self):
        """Returns the p value of the body axis angular acceleration in
        degress/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetPQRdot(1)

        return degrees(acceleration)

    @property
    def q_dot(self):
        """Returns the q value of the body axis angular acceleration in
        degress/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetPQRdot(2)

        return degrees(acceleration)

    @property
    def r_dot(self):
        """Returns the r value of the body axis angular acceleration in
        degress/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetPQRdot(3)

        return degrees(acceleration)

    @property
    def u_dot(self):
        """Returns the u item of the the body axis acceleration in
        meters/sec"""
        acceleration = self.fdmexec.GetAccelerations().GetUVWdot(1)

        return convert_feet_to_meters(acceleration)

    @property
    def v_dot(self):
        """Returns the v item of the the body axis acceleration in
        meters/sec"""
        acceleration = self.fdmexec.GetAccelerations().GetUVWdot(2)

        return convert_feet_to_meters(acceleration)

    @property
    def w_dot(self):
        """Returns the w item of the the body axis acceleration in
        meters/sec"""
        acceleration = self.fdmexec.GetAccelerations().GetUVWdot(3)

        return convert_feet_to_meters(acceleration)

    @property
    def gravity(self):
        """Returns the acceleration of the gravity in meters/sec^2"""
        acceleration = self.fdmexec.GetAccelerations().GetGravAccelMagnitude()

        return convert_feet_to_meters(acceleration)


class Velocities(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def p(self):
        """Return the p item of the body angular rates in degrees/sec"""
        return degrees(self.fdmexec.GetPropagate().GetPQR(1))

    @property
    def q(self):
        """Return the q item of the body angular rates in degrees/sec"""
        return degrees(self.fdmexec.GetPropagate().GetPQR(2))

    @property
    def r(self):
        """Return the r item of the body angular rates in degrees/sec"""
        return degrees(self.fdmexec.GetPropagate().GetPQR(3))

    @property
    def true_airspeed(self):
        """Return the true airspeed in meters/second"""
        airspeed = self.fdmexec.GetAuxiliary().GetVtrueFPS()

        return convert_feet_to_meters(airspeed)

    @property
    def climb_rate(self):
        """Return the vertical velocity in meters/seconds"""
        # climb_rate = self.fdmexec.GetPropertyValue("velocities/v-down-fps")
        climb_rate = -self.fdmexec.GetPropagate().GetVel(3)

        return convert_feet_to_meters(climb_rate)

    @property
    def u(self):
        """Returns the u item of the body frame velocity vector in
        meters/sec"""
        velocity = self.fdmexec.GetPropagate().GetUVW(1)

        return convert_feet_to_meters(velocity)

    @property
    def v(self):
        """Returns the v item of the body frame velocity vector in
        meters/sec"""
        velocity = self.fdmexec.GetPropagate().GetUVW(2)

        return convert_feet_to_meters(velocity)

    @property
    def w(self):
        """Returns the w item of the body frame velocity vector in
        meters/sec"""
        velocity = self.fdmexec.GetPropagate().GetUVW(3)

        return convert_feet_to_meters(velocity)

    @property
    def calibrated_airspeed(self):
        """Returns the calibrated airspeed in meters/sec"""
        airspeed = self.fdmexec.GetAuxiliary().GetVcalibratedFPS()

        return convert_feet_to_meters(airspeed)

    @property
    def equivalent_airspeed(self):
        """Returns the equivalent airspeed in meters/sec"""
        airspeed = self.fdmexec.GetAuxiliary().GetVequivalentFPS()

        return convert_feet_to_meters(airspeed)

    @property
    def ground_speed(self):
        """Returns the ground speed in meters/sec"""
        airspeed = self.fdmexec.GetAuxiliary().GetVground()

        return convert_feet_to_meters(airspeed)


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


class FDM(object):
    """The FDM object is a wrapper around the JSBSim objects that contains the
    values of the flight dynamics model."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.accelerations = Accelerations(fdmexec)
        self.velocities = Velocities(fdmexec)
        self.position = Position(fdmexec)
        self.orientation = Orientation(fdmexec)

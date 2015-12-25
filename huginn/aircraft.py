"""
The huginn.aircraft module contains classes that wrap the jsbsim object and
and provide access to the simulated components of the aircraft.
"""

from abc import ABCMeta, abstractmethod
from math import degrees

from huginn.unit_conversions import (convert_feet_to_meters,
                                     convert_rankine_to_kelvin,
                                     convert_psf_to_pascal,
                                     convert_libra_to_newtons)

class Component(object):
    """The Component class is the base for every part that simulates a part
    of an aircraft."""
    __metaclass__ = ABCMeta

    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @abstractmethod
    def run(self):
        """Update the component using data from JSBSim."""
        pass

class GPS(Component):
    """The GPS class simulates the aircraft's GPS system."""
    def __init__(self, fdmexec):
        Component.__init__(self, fdmexec)

        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        propagate = self.fdmexec.GetPropagate()

        self.latitude = propagate.GetLatitudeDeg()
        self.longitude = propagate.GetLongitudeDeg()

        self.altitude = propagate.GetAltitudeASLmeters()

        airspeed_in_fps = self.fdmexec.GetAuxiliary().GetVtrueFPS()
        self.airspeed = convert_feet_to_meters(airspeed_in_fps)
        #self.airspeed = convert_knots_to_meters_per_sec(airspeed_in_knots)

        self.heading = degrees(propagate.GetEuler().Entry(3))

class Accelerometer(Component):
    """The Accelerometer class returns the acceleration measures on the body
    frame."""
    def __init__(self, fdmexec):
        Component.__init__(self, fdmexec)

        self.x_acceleration = 0.0
        self.y_acceleration = 0.0
        self.z_acceleration = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        auxiliary = self.fdmexec.GetAuxiliary()

        self.x_acceleration = convert_feet_to_meters(auxiliary.GetPilotAccel(1))

        self.y_acceleration = convert_feet_to_meters(auxiliary.GetPilotAccel(2))

        self.z_acceleration = convert_feet_to_meters(auxiliary.GetPilotAccel(3))

class Gyroscope(Component):
    """The Gyroscope class contains the angular velocities measured on the body axis."""
    def __init__(self, fdmexec):
        Component.__init__(self, fdmexec)

        self.roll_rate = 0.0
        self.pitch_rate = 0.0
        self.yaw_rate = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        auxiliary = self.fdmexec.GetAuxiliary()

        self.roll_rate = degrees(auxiliary.GetEulerRates(1))

        self.pitch_rate = degrees(auxiliary.GetEulerRates(2))

        self.yaw_rate = degrees(auxiliary.GetEulerRates(3))

class Thermometer(Component):
    """The Thermometer class contains the temperature measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        Component.__init__(self, fdmexec)

        self.temperature = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        #self.temperature = self.fdmexec.GetAuxiliary().GetTAT_C()
        self.temperature = convert_rankine_to_kelvin(self.fdmexec.GetAtmosphere().GetTemperature())

class PressureSensor(Component):
    """The PressureSensor class contains the static presured measured by the
    aircraft's sensors."""
    def __init__(self, fdmexec):
        Component.__init__(self, fdmexec)

        self.pressure = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.pressure = convert_psf_to_pascal(self.fdmexec.GetAtmosphere().GetPressure())

class PitotTube(Component):
    """The PitosTure class simulates the aircraft's pitot system."""
    def __init__(self, fdmexec):
        Component.__init__(self, fdmexec)

        self.pressure = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        self.pressure = convert_psf_to_pascal(self.fdmexec.GetAuxiliary().GetTotalPressure())

class InertialNavigationSystem(Component):
    """The InertialNavigationSystem class is used to simulate the aircraft's
    inertial navigation system."""
    def __init__(self, fdmexec):
        Component.__init__(self, fdmexec)

        self.roll = 0.0
        self.pitch = 0.0
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        propagate = self.fdmexec.GetPropagate()

        euler_angles = propagate.GetEulerDeg()
        self.roll = euler_angles.Entry(1)

        self.pitch = euler_angles.Entry(2)

        self.heading = euler_angles.Entry(3)

        self.latitude = propagate.GetLatitudeDeg()
        self.longitude = propagate.GetLongitudeDeg()

        airspeed_in_fps = self.fdmexec.GetAuxiliary().GetVtrueFPS()
        self.airspeed = convert_feet_to_meters(airspeed_in_fps)

        self.altitude = propagate.GetAltitudeASLmeters()

class Controls(object):
    """The Controls class holds the aircraft control surfaces values"""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

    @property
    def aileron(self):
        """The aileron deflection."""
        return self.fdmexec.GetFCS().GetDaCmd()

    @aileron.setter
    def aileron(self, value):
        """Set the aileron deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.GetFCS().SetDaCmd(value)

    @property
    def elevator(self):
        """The elevator deflection."""
        return self.fdmexec.GetFCS().GetDeCmd()

    @elevator.setter
    def elevator(self, value):
        """Set the elevator deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.GetFCS().SetDeCmd(value)

    @property
    def rudder(self):
        """The rudder deflection."""
        return self.fdmexec.GetFCS().GetDrCmd()

    @rudder.setter
    def rudder(self, value):
        """Set the rudder deflection.

        This value must be between -1.0 and 1.0"""
        if value > 1.0:
            value = 1.0
        elif value < -1.0:
            value = -1.0

        self.fdmexec.GetFCS().SetDrCmd(value)

    @property
    def throttle(self):
        """The throttle setting."""
        return self.fdmexec.GetFCS().GetThrottleCmd(0)

    @throttle.setter
    def throttle(self, value):
        """Set the engine's throttle position.

        This value must be between 0.0 and 1.0."""
        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0

        for i in range(self.fdmexec.GetPropulsion().GetNumEngines()):
            self.fdmexec.GetFCS().SetThrottleCmd(i, value)

class Engine(Component):
    """The Engine class contains data about the state of the aircraft's engine."""
    def __init__(self, fdmexec):
        Component.__init__(self, fdmexec)

        self.thrust = 0.0
        self.throttle = 0.0

    def run(self):
        """Update the component using data from JSBSim."""
        engine = self.fdmexec.GetPropulsion().GetEngine(0)

        self.thrust = convert_libra_to_newtons(engine.GetThruster().GetThrust())

        self.throttle = self.fdmexec.GetFCS().GetThrottleCmd(0)

class Aircraft(object):
    """The Aircraft class is a wrapper around jsbsim that contains data about
    the aircraft state."""
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec

        self._fdmexec_state_listeners = []

        self.gps = GPS(fdmexec)
        self.accelerometer = Accelerometer(fdmexec)
        self.gyroscope = Gyroscope(fdmexec)
        self.thermometer = Thermometer(fdmexec)
        self.pressure_sensor = PressureSensor(fdmexec)
        self.pitot_tube = PitotTube(fdmexec)
        self.inertial_navigation_system = InertialNavigationSystem(fdmexec)
        self.engine = Engine(fdmexec)
        self.controls = Controls(fdmexec)

    def run(self):
        """Update the aircraft state using the data from JSBSim"""
        self.gps.run()
        self.accelerometer.run()
        self.gyroscope.run()
        self.thermometer.run()
        self.pressure_sensor.run()
        self.pitot_tube.run()
        self.inertial_navigation_system.run()
        self.engine.run()

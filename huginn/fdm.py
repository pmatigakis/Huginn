"""
The huginn.fdm module contains classes and functions that can be used to
initialize the flight dynamics model and create a model for a simulated
aircraft
"""
from math import degrees
from abc import ABCMeta, abstractmethod
import logging

from huginn import configuration
import huginn_jsbsim
from huginn.unit_conversions import convert_meters_to_feet,\
    convert_meters_per_sec_to_knots, convert_feet_to_meters,\
    convert_rankine_to_kelvin, convert_psf_to_pascal,\
    convert_libra_to_newtons

fdm_properties = [
    "simulation/sim-time-sec",
    "simulation/dt",
    "position/lat-gc-deg",
    "position/long-gc-deg",
    "position/h-sl-ft",
    "velocities/vtrue-kts",
    "velocities/v-north-fps",
    "velocities/v-east-fps",
    "velocities/v-down-fps",
    "velocities/u-fps",
    "velocities/v-fps",
    "velocities/w-fps",
    "velocities/p-rad_sec",
    "velocities/q-rad_sec",
    "velocities/r-rad_sec",
    "velocities/mach",
    "accelerations/a-pilot-x-ft_sec2",
    "accelerations/a-pilot-y-ft_sec2",
    "accelerations/a-pilot-z-ft_sec2",
    "accelerations/pdot-rad_sec2",
    "accelerations/qdot-rad_sec2",
    "accelerations/rdot-rad_sec2",
    "accelerations/udot-ft_sec2",
    "accelerations/vdot-ft_sec2",
    "accelerations/wdot-ft_sec2",
    "attitude/phi-rad",
    "attitude/theta-rad",
    "attitude/psi-rad",
    "attitude/roll-rad",
    "attitude/pitch-rad",
    "attitude/heading-true-rad",
    "propulsion/engine/engine-rpm",
    "propulsion/engine/thrust-lbs",
    "propulsion/engine/power-hp",
    "atmosphere/T-R",
    "atmosphere/T-sl-R",
    "atmosphere/P-psf",
    "atmosphere/P-sl-psf",
    "aero/qbar-psf",
    "fcs/elevator-cmd-norm",
    "fcs/aileron-cmd-norm",
    "fcs/rudder-cmd-norm",
    "fcs/throttle-cmd-norm"
]

fdm_data_properties = [
   "accelerations/a-pilot-x-ft_sec2",
   "accelerations/a-pilot-y-ft_sec2",
   "accelerations/a-pilot-z-ft_sec2",
   "velocities/p-rad_sec",
   "velocities/q-rad_sec",
   "velocities/r-rad_sec",
   "atmosphere/P-psf",
   "aero/qbar-psf",
   "atmosphere/T-R",
   "position/lat-gc-deg",
   "position/long-gc-deg",
   "position/h-sl-ft",
   "velocities/vtrue-kts",
   "attitude/heading-true-rad"
]

controls_properties = [
    "fcs/elevator-cmd-norm",
    "fcs/aileron-cmd-norm",
    "fcs/rudder-cmd-norm",
    "fcs/throttle-cmd-norm"
]

class FDM(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def reset_to_initial_conditions(self):
        pass

    @abstractmethod
    def update_aircraft(self, aircraft):
        pass

    @abstractmethod
    def get_dt(self):
        pass

    @abstractmethod
    def get_simulation_time(self):
        pass

    @abstractmethod
    def set_aircraft_controls(self, aileron, elevator, rudder, throttle):
        pass

class JSBSimFDM(FDM):
    def __init__(self, fdm, start_trimmed=False):
        FDM.__init__(self)
        self.fdm = fdm
        self.start_trimmed = start_trimmed

    def run(self):
        return self.fdm.run()

    def reset_to_initial_conditions(self):
        reset_result = self.fdm.reset(self.start_trimmed)

        self.fdm.start_engines()

        self.fdm.set_aileron(0.0)
        self.fdm.set_elevator(0.0)
        self.fdm.set_rudder(0.0)
        self.fdm.set_throttle(0.0)

        return reset_result

    def get_dt(self):
        return self.fdm.get_dt()

    def get_simulation_time(self):
        return self.fdm.get_sim_time()

    def update_aircraft(self, aircraft):
        self.update_gps(aircraft.gps)
        self.update_accelerometer(aircraft.accelerometer)
        self.update_gyroscope(aircraft.gyroscope)
        self.update_thermometer(aircraft.thermometer)
        self.update_pressure_sensor(aircraft.pressure_sensor)
        self.update_pitot_tube(aircraft.pitot_tube)
        self.update_inertial_navigation_system(aircraft.inertial_navigation_system)
        self.update_aircraft_controls(aircraft.controls)
        self.update_engine(aircraft.engine)

    def update_gps(self, gps):
        gps.latitude = self.fdm.get_latitude()
        gps.longitude = self.fdm.get_longitude()

        gps.altitude = self.fdm.get_altitude()

        airspeed_in_fps = self.fdm.get_airspeed()
        gps.airspeed = convert_feet_to_meters(airspeed_in_fps)
        #self.airspeed = convert_knots_to_meters_per_sec(airspeed_in_knots)

        gps.heading = degrees(self.fdm.get_heading())

    def update_accelerometer(self, accelerometer):
        accelerometer.x_acceleration = convert_feet_to_meters(self.fdm.get_x_acceleration())

        accelerometer.y_acceleration = convert_feet_to_meters(self.fdm.get_y_acceleration())

        accelerometer.z_acceleration = convert_feet_to_meters(self.fdm.get_z_acceleration())

    def update_gyroscope(self, gyroscope):
        gyroscope.roll_rate = degrees(self.fdm.get_roll_rate())

        gyroscope.pitch_rate = degrees(self.fdm.get_pitch_rate())

        gyroscope.yaw_rate = degrees(self.fdm.get_yaw_rate())

    def update_thermometer(self, thermometer):
        thermometer.temperature = convert_rankine_to_kelvin(self.fdm.get_temperature())

    def update_pressure_sensor(self, pressure_sensor):
        pressure_sensor.pressure = convert_psf_to_pascal(self.fdm.get_pressure())

    def update_pitot_tube(self, pitot_tube):
        pitot_tube.pressure = convert_psf_to_pascal(self.fdm.get_total_pressure())

    def update_inertial_navigation_system(self, ins):
        ins.roll = self.fdm.get_roll()

        ins.pitch = self.fdm.get_pitch()

        ins.heading = degrees(self.fdm.get_heading())

        ins.latitude = self.fdm.get_latitude()
        ins.longitude = self.fdm.get_longitude()

        airspeed_in_fps = self.fdm.get_airspeed()
        ins.airspeed = convert_feet_to_meters(airspeed_in_fps)

        ins.altitude = self.fdm.get_altitude()

    def update_aircraft_controls(self, controls):
        controls.elevator = self.fdm.get_elevator()
        controls.aileron = self.fdm.get_aileron()
        controls.rudder = self.fdm.get_rudder()
        controls.throttle = self.fdm.get_throttle()

    def update_engine(self, engine):
        engine.thrust = convert_libra_to_newtons(self.fdm.get_thrust())

        engine.throttle = self.fdm.get_throttle()

    def set_aircraft_controls(self, aileron, elevator, rudder, throttle):
        if aileron > 1.0:
            aileron = 1.0
        elif aileron < -1.0:
            aileron = -1.0

        self.fdm.set_aileron(aileron)

        if elevator > 1.0:
            elevator = 1.0
        elif elevator < -1.0:
            elevator = -1.0

        self.fdm.set_elevator(elevator)

        if rudder > 1.0:
            rudder = 1.0
        elif rudder < -1.0:
            rudder = -1.0

        self.fdm.set_rudder(rudder)

        if throttle > 1.0:
            throttle = 1.0
        elif throttle < 0.0:
            throttle = 0.0

        self.fdm.set_throttle(throttle)

class FDMBuilder(object):
    """The FDMBuilder created the flight dynamics model object that will be
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

        self.trim = False

    def create_fdm(self):
        """Create the flight dynamics model"""
        logger = logging.getLogger("huginn")

        fdm = huginn_jsbsim.FDM()

        logger.debug("Using jsbsim data at %s", self.data_path)

        fdm.set_data_path(self.data_path)

        logger.debug("JSBSim dt is %f", self.dt)
        fdm.set_dt(self.dt)

        logger.debug("Using aircraft %s", self.aircraft)
        fdm.load_model(self.aircraft)

        logger.debug("starting the aircraft's engines")
        fdm.start_engines()

        fdm.set_throttle(0.0)

        altitude_in_feet = convert_meters_to_feet(self.altitude)
        airspeed_in_knots = convert_meters_per_sec_to_knots(self.airspeed)

        logger.debug("Initial latitude: %f degrees", self.latitude)
        logger.debug("Initial longitude: %f degrees", self.longitude)
        logger.debug("Initial altitude: %f meters", self.altitude)
        logger.debug("Initial airspeed: %f meters/second", self.airspeed)
        logger.debug("Initial heading: %f degrees", self.heading)

        fdm.set_initial_condition(self.latitude, self.longitude, altitude_in_feet, airspeed_in_knots, self.heading)

        if not fdm.run_ic():
            logger.error("Failed to run initial condition")
            return None

        if self.trim:
            logger.debug("Trimming the aircraft")
            trim_result = fdm.trim()

            if not trim_result:
                logger.warning("Failed to trim the aircraft")

        # Run the simulation for 1 second in order to make sure that everything
        # is ok
        while True:
            if not fdm.run():
                logger.error("Failed to execute initial run")
                return None

            if fdm.get_sim_time() > 1.0:
                break

        fdm.print_simulation_configuration()

        fdm.dump_state()

        return JSBSimFDM(fdm, self.trim)

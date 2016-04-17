"""
This module contains classes that are used by Huginn's web server and web clients
"""

import requests
import json
import logging

from twisted.web.resource import Resource

class AircraftResource(Resource):
    """This class server as the root for the aircraft web resources."""
    isLeaf = False

    def __init__(self, aircraft):
        Resource.__init__(self)

        self.aircraft = aircraft

        self.putChild("gps", GPSData(self.aircraft))
        self.putChild("accelerometer", AccelerometerData(self.aircraft))
        self.putChild("gyroscope", GyroscopeData(self.aircraft))
        self.putChild("thermometer", ThermometerData(self.aircraft))
        self.putChild("pressure_sensor", PressureSensorData(self.aircraft))
        self.putChild("pitot_tube", PitotTubeData(self.aircraft))
        self.putChild("ins", InertialNavigationSystemData(self.aircraft))
        self.putChild("engine", EngineData(self.aircraft))
        self.putChild("flight_controls", FlightControlsData(self.aircraft))

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        aircraft_info = {"aircraft_type": self.aircraft.type}

        return json.dumps(aircraft_info)

class FlightDataResource(Resource):
    """This is the base class that can be used to create resource subclasses
    that return flight data"""
    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_flight_data(self):
        """This method must be overridden by the subclass. It should return a
        dictionary containing the requested flight data"""
        pass

    def render_GET(self, request):
        """Return the response with the flight data"""
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        flight_data = self.get_flight_data()

        return json.dumps(flight_data)

class GPSData(FlightDataResource):
    """This resource class will return the gps data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        gps_data = {
            "latitude": self.aircraft.instruments.gps.latitude,
            "longitude": self.aircraft.instruments.gps.longitude,
            "altitude": self.aircraft.instruments.gps.altitude,
            "airspeed": self.aircraft.instruments.gps.airspeed,
            "heading": self.aircraft.instruments.gps.heading
        }

        #print("latitude", gps_data["latitude"], self.aircraft.fdmexec.GetPropertyValue("position/lat-gc-deg"))
        #print("longitude", gps_data["longitude"],  self.aircraft.fdmexec.GetPropertyValue("position/long-gc-deg"))
        #print("airspeed", gps_data["airspeed"],  convert_knots_to_meters_per_sec(self.aircraft.fdmexec.GetPropertyValue("velocities/vtrue-kts")))
        #print("altitude", gps_data["altitude"],  convert_feet_to_meters(self.aircraft.fdmexec.GetPropertyValue("position/h-sl-ft")))
        #print("heading", gps_data["heading"],  degrees(self.aircraft.fdmexec.GetPropertyValue("attitude/heading-true-rad")))

        return gps_data

class AccelerometerData(FlightDataResource):
    """This resource class will return the accelerometer data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        accelerometer_data = {
            "x_acceleration": self.aircraft.sensors.accelerometer.x,
            "y_acceleration": self.aircraft.sensors.accelerometer.y,
            "z_acceleration": self.aircraft.sensors.accelerometer.z
        }

        #print("x_acc", accelerometer_data["x_acceleration"], convert_feet_to_meters(self.aircraft.fdmexec.GetPropertyValue("accelerations/a-pilot-x-ft_sec2")))
        #print("y_acc", accelerometer_data["y_acceleration"], convert_feet_to_meters(self.aircraft.fdmexec.GetPropertyValue("accelerations/a-pilot-y-ft_sec2")))
        #print("z_acc", accelerometer_data["z_acceleration"], convert_feet_to_meters(self.aircraft.fdmexec.GetPropertyValue("accelerations/a-pilot-z-ft_sec2")))

        return accelerometer_data

class GyroscopeData(FlightDataResource):
    """This resource class will return the gyroscope data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        gyroscope_data = {
            "roll_rate": self.aircraft.gyroscope.roll_rate,
            "pitch_rate": self.aircraft.gyroscope.pitch_rate,
            "yaw_rate": self.aircraft.gyroscope.yaw_rate,
        }

        #print("roll_rate", gyroscope_data["roll_rate"], degrees(self.aircraft.fdmexec.GetPropertyValue("velocities/p-rad_sec")))
        #print("pitch_rate", gyroscope_data["pitch_rate"], degrees(self.aircraft.fdmexec.GetPropertyValue("velocities/q-rad_sec")))
        #print("yaw_rate", gyroscope_data["yaw_rate"], degrees(self.aircraft.fdmexec.GetPropertyValue("velocities/r-rad_sec")))

        return gyroscope_data

class ThermometerData(FlightDataResource):
    """This resource class will return the thermometer data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        thermometer_data = {
            "temperature": self.aircraft.thermometer.temperature,
        }

        #print("temperature", thermometer_data["temperature"], convert_rankine_to_kelvin(self.aircraft.fdmexec.GetPropertyValue("atmosphere/T-R")))

        return thermometer_data

class PressureSensorData(FlightDataResource):
    """This resource class will return the pressure sensor data in json
    format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        pressure_sensor_data = {
            "static_pressure": self.aircraft.pressure_sensor.pressure,
        }

        #print("static_pressule", pressure_sensor_data["static_pressure"], convert_psf_to_pascal(self.aircraft.fdmexec.GetPropertyValue("atmosphere/P-psf")))

        return pressure_sensor_data

class PitotTubeData(FlightDataResource):
    """This resource class will return the pitot tube data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        pitot_tube_data = {
            "total_pressure": self.aircraft.pitot_tube.pressure,
        }

        #print("total pressure", pitot_tube_data["total_pressure"], convert_psf_to_pascal(self.aircraft.fdmexec.GetPropertyValue("aero/qbar-psf")))

        return pitot_tube_data

class InertialNavigationSystemData(FlightDataResource):
    """This resource class will return the inertial navigation system data in
    json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        inertial_navigation_system_data = {
            "latitude": self.aircraft.inertial_navigation_system.latitude,
            "longitude": self.aircraft.inertial_navigation_system.longitude,
            "altitude": self.aircraft.inertial_navigation_system.altitude,
            "airspeed": self.aircraft.inertial_navigation_system.airspeed,
            "heading": self.aircraft.inertial_navigation_system.heading,
            "roll": self.aircraft.inertial_navigation_system.roll,
            "pitch": self.aircraft.inertial_navigation_system.pitch,
        }

        #print("latitude", inertial_navigation_system_data["latitude"], self.aircraft.fdmexec.GetPropertyValue("position/lat-gc-deg"))
        #print("longitude", inertial_navigation_system_data["longitude"], self.aircraft.fdmexec.GetPropertyValue("position/long-gc-deg"))
        #print("airspeed", inertial_navigation_system_data["airspeed"],  convert_knots_to_meters_per_sec(self.aircraft.fdmexec.GetPropertyValue("velocities/vtrue-kts")))
        #print("altitude", inertial_navigation_system_data["altitude"],  convert_feet_to_meters(self.aircraft.fdmexec.GetPropertyValue("position/h-sl-ft")))
        #print("heading", inertial_navigation_system_data["heading"],  degrees(self.aircraft.fdmexec.GetPropertyValue("attitude/heading-true-rad")))
        #print("roll", inertial_navigation_system_data["roll"], degrees(self.aircraft.fdmexec.GetPropertyValue("attitude/roll-rad")))
        #print("pitch", inertial_navigation_system_data["pitch"], degrees(self.aircraft.fdmexec.GetPropertyValue("attitude/pitch-rad")))

        return inertial_navigation_system_data

class EngineData(FlightDataResource):
    """This resource class will return the engine data in json format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        engine_data = {
            "thrust": self.aircraft.engine.thrust,
            "throttle": self.aircraft.engine.throttle,
        }

        #print("thrust", engine_data["thrust"], convert_libra_to_newtons(self.aircraft.fdmexec.GetPropertyValue("propulsion/engine/thrust-lbs")))
        #print("throttle", engine_data["throttle"], self.aircraft.fdmexec.GetPropertyValue("fcs/throttle-cmd-norm"))

        return engine_data

class FlightControlsData(FlightDataResource):
    """This resource class will return the flight controls data in json
    format"""
    isLeaf = True

    def __init__(self, aircraft):
        FlightDataResource.__init__(self, aircraft)

    def get_flight_data(self):
        flight_controls_data = {
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }

        return flight_controls_data

class FDMData(FlightDataResource):
    """The FDMData resource returns data relative to the simulation"""
    isLeaf = True
    def __init__(self, fdmexec, aircraft):
        FlightDataResource.__init__(self, aircraft)
        self.fdmexec = fdmexec

    def get_flight_data(self):
        flight_data = {
            "time": self.fdmexec.GetSimTime(),
            "dt": self.fdmexec.GetDeltaT(),
            "latitude": self.aircraft.instruments.gps.latitude,
            "longitude": self.aircraft.instruments.gps.longitude,
            "altitude": self.aircraft.instruments.gps.altitude,
            "airspeed": self.aircraft.instruments.gps.airspeed,
            "heading": self.aircraft.instruments.gps.heading,
            "x_acceleration": self.aircraft.sensors.accelerometer.x,
            "y_acceleration": self.aircraft.sensors.accelerometer.y,
            "z_acceleration": self.aircraft.sensors.accelerometer.z,
            "roll_rate": self.aircraft.gyroscope.roll_rate,
            "pitch_rate": self.aircraft.gyroscope.pitch_rate,
            "yaw_rate": self.aircraft.gyroscope.yaw_rate,
            "temperature": self.aircraft.thermometer.temperature,
            "static_pressure": self.aircraft.pressure_sensor.pressure,
            "total_pressure": self.aircraft.pitot_tube.pressure,
            "roll": self.aircraft.inertial_navigation_system.roll,
            "pitch": self.aircraft.inertial_navigation_system.pitch,
            "thrust": self.aircraft.engine.thrust,
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }

        return flight_data

class SimulatorCommand(Resource):
    """The SimulatorCommand is the base class for the simulator commands that
    are called throught an http connection"""
    def __init__(self):
        Resource.__init__(self)

    def send_response(self, request, response_data):
        """Return the response in json format"""
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        return json.dumps(response_data)

class PauseSimulatorCommand(SimulatorCommand):
    """The PauseSimulatorCommand http command pauses the simulator"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        self.logger.debug("Pausing the simulator")
        self.simulator.pause()

        return self.send_response(request,
                                  {"command": "pause",
                                   "result": "ok"})

class ResumeSimulatorCommand(SimulatorCommand):
    """The PauseSimulatorCommand http command resumes the simulation"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        self.logger.debug("Resuming the simulator")
        self.simulator.resume()

        return self.send_response(request,
                                  {"command": "resume",
                                   "result": "ok"})

class ResetSimulatorCommand(SimulatorCommand):
    """The ResetSimulatorCommand http command resets the simulator"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        self.logger.debug("Reseting the simulator")

        reset_result = self.simulator.reset()
        if not reset_result:
            self.logger.error("Failed to reset the simulator")
            reactor.stop()  # @UndefinedVariable
            return self.send_response(request,
                                      {"command": "reset",
                                       "result": "error"})

        self.logger.debug("Pausing the simulator")
        self.simulator.pause()

        return self.send_response(request,
                                  {"command": "reset",
                                   "result": "ok"})

class StepSimulatorCommand(SimulatorCommand):
    """The StepSimulatorCommand http command executes a single simulation
    timestep"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        self.logger.debug("Executing a single simulation step")

        result = self.simulator.step()

        if not result:
            self.logger.error("The simulator has failed to run")
            reactor.stop()  # @UndefinedVariable
            return self.send_response(request,
                                      {"command": "step",
                                       "result": "error"})

        return self.send_response(request,
                                  {"command": "step",
                                   "result": "ok"})

class RunForSimulatorCommand(SimulatorCommand):
    """The RunForSimulatorCommand http command makes the simulator run for
    the given amount of time"""
    isLeaf = True

    def __init__(self, simulator):
        SimulatorCommand.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")

    def render_POST(self, request):
        """Execute the command"""
        time_to_run = float(request.args["time_to_run"][0])
        self.logger.debug("Running the simulation for %f seconds", time_to_run)

        result = self.simulator.run_for(time_to_run)

        if not result:
            self.logger.error("The simulator has failed to run for %f", time_to_run)
            reactor.stop()  # @UndefinedVariable
            return self.send_response(request,
                                      {"command": "run_for",
                                       "result": "error"})

        return self.send_response(request,
                                  {"command": "run_for",
                                   "result": "ok"})

class SimulatorControl(Resource):
    """The SimulatorControl resource is used to control the simulator.
    For the moment it is possible to pause, resume, reset, run a
    single time step and run the simulation for a specified time"""
    isLeaf = False

    def __init__(self, simulator):
        Resource.__init__(self)
        self.simulator = simulator
        self.logger = logging.getLogger("huginn")
        self.putChild("reset", ResetSimulatorCommand(simulator))
        self.putChild("pause", PauseSimulatorCommand(simulator))
        self.putChild("resume", ResumeSimulatorCommand(simulator))
        self.putChild("step", StepSimulatorCommand(simulator))
        self.putChild("run_for", RunForSimulatorCommand(simulator))

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def send_response(self, request, response_data):
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        return json.dumps(response_data)

    def render_GET(self, request):
        """The GET http method simply returns the state of the simulator in
        json format"""
        simulator_state = {
            "time": self.simulator.simulation_time,
            "dt": self.simulator.dt,
            "running": not self.simulator.is_paused()
        }

        return self.send_response(request, simulator_state)

class WebClient(object):
    """The WebClient is used to retrieve flight data from Huginn's web
    server"""
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def _get_host_url(self, page):
        return "http://%s:%d/aircraft/%s" % (self.host, self.port, page)

    def _get_json_data_from_endpoint(self, endpoint):
        response = requests.get(self._get_host_url(endpoint))

        data = json.loads(response.text)

        return data

    def get_gps_data(self):
        """Get the gps data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("gps")

    def get_accelerometer_data(self):
        """Get the accelerometer data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("accelerometer")

    def get_gyroscope_data(self):
        """Get the gyroscope data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("gyroscope")

    def get_thermometer_data(self):
        """Get the temperature data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("thermometer")

    def get_pressure_sensor_data(self):
        """Get the atmospheric pressure data from the simulator and return
        them as a dictionary"""
        return self._get_json_data_from_endpoint("pressure_sensor")

    def get_pitot_tube_data(self):
        """Get the pitot tube data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("pitot_tube")

    def get_ins_data(self):
        """Get the inertial navigation system  data from the simulator and
        return them as a dictionary"""
        return self._get_json_data_from_endpoint("ins")

    def get_engine_data(self):
        """Get the engine data from the simulator and return them as a
        dictionary"""
        return self._get_json_data_from_endpoint("engine")

    def get_flight_controls(self):
        """Get the flight controls data from the simulator and return them as
        a dictionary"""
        return self._get_json_data_from_endpoint("flight_controls")

class MapData(Resource):
    """The MapData resource returns the waypoints stored in the simulation
    server"""
    def __init__(self):
        Resource.__init__(self)
        self.waypoints = []

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        return json.dumps(self.waypoints)

    def render_POST(self, request):
        self.waypoints = json.loads(request.content.getvalue())

        request.responseHeaders.addRawHeader("content-type",
                                             "application/json")

        return json.dumps({"result": "ok"})

import json

from twisted.web.resource import Resource

class Index(Resource):
    isLeaf = False

    def __init__(self, fdmexec):
        Resource.__init__(self)

        self.fdmexec = fdmexec

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return "Huginn is running"

class GPSData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_gps_data(self):
        gps_data = {
            "latitude": self.aircraft.gps.latitude,
            "longitude": self.aircraft.gps.longitude,
            "altitude": self.aircraft.gps.altitude,
            "airspeed": self.aircraft.gps.airspeed,
            "heading": self.aircraft.gps.heading
        }

        return gps_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        gps_data = self.get_gps_data()

        return json.dumps(gps_data)

class AccelerometerData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_accelerometer_data(self):
        accelerometer_data = {
            "x_acceleration": self.aircraft.accelerometer.x_acceleration,
            "y_acceleration": self.aircraft.accelerometer.y_acceleration,
            "z_acceleration": self.aircraft.accelerometer.z_acceleration
        }

        return accelerometer_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        accelerometer_data = self.get_accelerometer_data()

        return json.dumps(accelerometer_data)

class GyroscopeData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_gyroscope_data(self):
        gyroscope_data = {
            "roll_rate": self.aircraft.gyroscope.roll_rate,
            "pitch_rate": self.aircraft.gyroscope.pitch_rate,
            "yaw_rate": self.aircraft.gyroscope.yaw_rate,
        }

        return gyroscope_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        gyroscope_data = self.get_gyroscope_data()

        return json.dumps(gyroscope_data)

class ThermometerData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_thermometer_data(self):
        thermometer_data = {
            "temperature": self.aircraft.thermometer.temperature,
        }

        return thermometer_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        thermometer_data = self.get_thermometer_data()

        return json.dumps(thermometer_data)

class PressureSensorData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_pressure_sensor_data(self):
        pressure_sensor_data = {
            "static_pressure": self.aircraft.pressure_sensor.pressure,
        }

        return pressure_sensor_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        pressure_sensor_data = self.get_pressure_sensor_data()

        return json.dumps(pressure_sensor_data)

class PitotTubeData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_pitot_tube_data(self):
        pitot_tube_data = {
            "dynamic_pressure": self.aircraft.pitot_tube.pressure,
        }

        return pitot_tube_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        pitot_tube_data = self.get_pitot_tube_data()

        return json.dumps(pitot_tube_data)

class InertialNavigationSystemData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_inertial_navigation_system_data(self):
        inertial_navigation_system_data = {
            "latitude": self.aircraft.inertial_navigation_system.latitude,
            "longitude": self.aircraft.inertial_navigation_system.longitude,
            "altitude": self.aircraft.inertial_navigation_system.altitude,
            "airspeed": self.aircraft.inertial_navigation_system.airspeed,
            "heading": self.aircraft.inertial_navigation_system.heading,
            "roll": self.aircraft.inertial_navigation_system.roll,
            "pitch": self.aircraft.inertial_navigation_system.pitch,
        }

        return inertial_navigation_system_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        inertial_navigation_system_data = self.get_inertial_navigation_system_data()

        return json.dumps(inertial_navigation_system_data)

class EngineData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_engine_data(self):
        engine_data = {
            "engine_rpm": self.aircraft.engine.rpm,
            "engine_thrust": self.aircraft.engine.thrust,
            "engine_power": self.aircraft.engine.power,
        }

        return engine_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        engine_data = self.get_engine_data()

        return json.dumps(engine_data)

class FlightControlsData(Resource):
    isLeaf = True

    def __init__(self, aircraft):
        Resource.__init__(self)
        self.aircraft = aircraft

    def get_flight_controls_data(self):
        flight_controls_data = {
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }

        return flight_controls_data

    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")

        flight_controls_data = self.get_flight_controls_data()

        return json.dumps(flight_controls_data)

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

class FDMData(Resource):
    isLeaf = True
    
    def __init__(self, aircraft):
        self.aircraft = aircraft
    
    def create_fdm_data_response(self):
        fdm_data = {
            "temperature": self.aircraft.thermometer.temperature,
            "dynamic_pressure": self.aircraft.pitot_tube.pressure,
            "static_pressure": self.aircraft.pressure_sensor.pressure,
            "latitude": self.aircraft.gps.latitude,
            "longitude": self.aircraft.gps.longitude,
            "altitude": self.aircraft.gps.altitude,
            "airspeed": self.aircraft.gps.airspeed,
            "heading": self.aircraft.gps.heading,
            "x_acceleration": self.aircraft.accelerometer.x_acceleration,
            "y_acceleration": self.aircraft.accelerometer.y_acceleration,
            "z_acceleration": self.aircraft.accelerometer.z_acceleration,
            "roll_rate": self.aircraft.gyroscope.roll_rate,
            "pitch_rate": self.aircraft.gyroscope.pitch_rate,
            "yaw_rate": self.aircraft.gyroscope.yaw_rate,
            "roll": self.aircraft.inertial_navigation_system.roll,
            "pitch": self.aircraft.inertial_navigation_system.pitch,
            "engine_rpm": self.aircraft.engine.rpm,
            "engine_thrust": self.aircraft.engine.thrust,
            "engine_power": self.aircraft.engine.power,
            "aileron": self.aircraft.controls.aileron,
            "elevator": self.aircraft.controls.elevator,
            "rudder": self.aircraft.controls.rudder,
            "throttle": self.aircraft.engine.throttle,
        }
        
        return fdm_data
    
    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")
        
        fdm_data = self.create_fdm_data_response()
        
        return json.dumps(fdm_data)
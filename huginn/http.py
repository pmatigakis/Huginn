import json

from twisted.web.resource import Resource

class JSONFDMDataEncoder(object):
    def __init__(self, aircraft):
        self.aircraft = aircraft
        
    def encode_fdm_data(self):
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
        }
        
        return json.dumps({"result": "ok", "fdm_data": fdm_data})
        
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
        self.fdm_data_encoder = JSONFDMDataEncoder(aircraft)
    
    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")
        
        encoded_fdm_data = self.fdm_data_encoder.encode_fdm_data()
        if encoded_fdm_data:
            return encoded_fdm_data
        else:
            return json.dumps({"result": "error"})
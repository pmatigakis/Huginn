import json

from twisted.web.resource import Resource

from huginn.fdm import fdm_properties

class JSONFDMDataEncoder(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
    def encode_fdm_data(self, fdm_properties):
        try:
            fdm_data = [(fdm_property, self.fdmexec.get_property_value(fdm_property))
                        for fdm_property in fdm_properties]
        
            fdm_data = dict(fdm_data)
        
            return json.dumps({"result": "ok", "fdm_data": fdm_data})
        except:
            return None

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
    
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.fdm_data_encoder = JSONFDMDataEncoder(fdmexec)
    
    def render_GET(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")
        
        encoded_fdm_data = self.fdm_data_encoder.encode_fdm_data(fdm_properties)
        if encoded_fdm_data:
            return encoded_fdm_data
        else:
            return json.dumps({"result": "error"})
    
class Controls(Resource):
    ifLeaf = True
    
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        
    def render_POST(self, request):
        request.responseHeaders.addRawHeader("content-type", "application/json")
        
        data = request.content.read()
        
        try:
            controls_data = json.loads(data)
        except:
            return json.dumps({"response": "error"})
        
        self.fdmexec.set_property_value("fcs/elevator-cmd-norm", controls_data["fcs/elevator-cmd-norm"])
        self.fdmexec.set_property_value("fcs/aileron-cmd-norm", controls_data["fcs/aileron-cmd-norm"])
        self.fdmexec.set_property_value("fcs/rudder-cmd-norm", controls_data["fcs/rudder-cmd-norm"])
        self.fdmexec.set_property_value("fcs/throttle-cmd-norm", controls_data["fcs/throttle-cmd-norm"])
        
        return json.dumps({"response": "ok"})
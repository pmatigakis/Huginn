from flask import Flask

from huginn.web.views import index, data

class HuginnWebServer(object):
    def __init__(self, huginn_host, huginn_port, 
                 web_server_host, web_server_port,
                 debug=True):
        
        
        self.app = Flask("huginn")

        self.host = web_server_host
        self.port = web_server_port

        self.debug = debug

        self.app.add_url_rule("/", "index", index)
        self.app.add_url_rule("/data", "data", data(huginn_host, huginn_port))

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)

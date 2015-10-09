"""
This module contains the web server class for the front-end of Huginn
"""

from flask import Flask

from huginn.web.views import index, FlightDataView

class HuginnWebServer(object):
    """This is the class that provides the front-end for Huginn."""
    def __init__(self, huginn_host, huginn_port,
                 web_server_host, web_server_port):
        self.app = Flask("huginn")

        self.host = web_server_host
        self.port = web_server_port

        self.debug = True

        #Add the views for the front-end
        self.app.add_url_rule("/", "index", index)
        self.app.add_url_rule("/data", "data", FlightDataView(huginn_host, huginn_port))

    def run(self):
        """Start the server."""
        self.app.run(host=self.host, port=self.port, debug=self.debug)

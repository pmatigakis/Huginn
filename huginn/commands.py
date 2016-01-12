from abc import ABCMeta, abstractmethod

import json
from requests import ConnectionError
from twisted.internet import reactor
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from twisted.internet.task import LoopingCall

from huginn import configuration
from huginn.http import WebClient
from huginn.control import SimulatorControlClient
from huginn.clients import MapClient
from huginn.io import CSVFDMDataWriter, FDMDataPrinter

class Command(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_parser(self, subparsers):
        pass

    def register_command(self, subparsers):
        parser = self.create_parser(subparsers)

        parser.set_defaults(func=self.run)

    @abstractmethod
    def run(self, args):
        pass

class DataCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def print_gps_data(self, web_client):
        data = web_client.get_gps_data()

        print("GPS data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def print_accelerometer_data(self, web_client):
        data = web_client.get_accelerometer_data()

        print("Accelerometer data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def print_gyroscope_data(self, web_client):
        data = web_client.get_gyroscope_data()

        print("Gyroscope data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def print_thermometer_data(self, web_client):
        data = web_client.get_thermometer_data()

        print("Thermometer data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def print_pressure_sensor_data(self, web_client):
        data = web_client.get_pressure_sensor_data()

        print("Pressure sensor data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def print_pitot_tube_data(self, web_client):
        data = web_client.get_pitot_tube_data()

        print("Pitot tube data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def print_ins_data(self, web_client):
        data = web_client.get_ins_data()

        print("Inertial navigation system data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def print_engine_data(self, web_client):
        data = web_client.get_engine_data()

        print("Engine data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def print_flight_controls_data(self, web_client):
        data = web_client.get_flight_controls()

        print("Flight controls data")
        print("========")

        for fdm_property in data:
            print('%s: %f' % (fdm_property, data[fdm_property]))

        print("")

    def create_parser(self, subparsers):
        parser = subparsers.add_parser("data", help="Print the FDM data")

        return parser

    def run(self, args):
        web_client = WebClient(args.host, args.web_port)

        try:
            self.print_gps_data(web_client)
            self.print_accelerometer_data(web_client)
            self.print_gyroscope_data(web_client)
            self.print_thermometer_data(web_client)
            self.print_pressure_sensor_data(web_client)
            self.print_pitot_tube_data(web_client)
            self.print_ins_data(web_client)
            self.print_engine_data(web_client)
            self.print_flight_controls_data(web_client)
        except ConnectionError:
            print("Failed to connect to Huginn's web server")

class ControlCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def create_parser(self, subparsers):
        parser = subparsers.add_parser("control", help="Control the simulator")

        parser.add_argument("command", action="store",
                            choices=["pause", "resume", "reset", "step", "run_for"],
                            help="the simulator control command")

        parser.add_argument("--time_to_run", action="store", default=0.1, help="The time in seconds to run the simulator")

        return parser

    def run(self, args):
        simulator_control_client = SimulatorControlClient(args.host, args.web_port)

        if args.command == "reset":
            result = simulator_control_client.reset()
        elif args.command == "pause":
            result = simulator_control_client.pause()
        elif args.command == "resume":
            result = simulator_control_client.resume()
        elif args.command == "step":
            result = simulator_control_client.step()
        elif args.command == "run_for":
            result = simulator_control_client.run_for(args.time_to_run)
        else:
            print("Invalid command %s" % args.command)
            exit(-1)

        if not result:
            print("Failed to execute command %s" % args.command)
            exit(-1)

class LoadWaypointsCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def create_parser(self, subparsers):
        parser = subparsers.add_parser("waypoints", help="Load a waypoint file to the simulator")

        parser.add_argument("waypoint_file", action="store", help="the file containing the waypoints")

        return parser

    def run(self, args):
        map_client = MapClient(args.host, args.web_port)

        result = map_client.load_from_csv(args.waypoint_file)

        if not result:
            print("Failed to load waypoints")

class RecordCommand(Command):
    def __init__(self):
        Command.__init__(self)
        self.output_file = None
        self.csv_telemetry_writer = None
        self.variables = ["time", "dt", "latitude", "longitude", "altitude",
            "airspeed", "heading", "x_acceleration", "y_acceleration",
            "z_acceleration", "roll_rate", "pitch_rate", "yaw_rate",
            "temperature", "static_pressure", "total_pressure",
            "roll", "pitch", "thrust", "aileron", "elevator","rudder",
            "throttle"]
        self.fdm_data_printer = FDMDataPrinter(["time", "altitude", "airspeed", "heading"])

    def create_parser(self, subparsers):
        parser = subparsers.add_parser("record", help="Record the fdm data")

        parser.add_argument("--port", default=configuration.WEB_SERVER_PORT, help="The simulator web server port")
        parser.add_argument("--dt", default=1.0, help="How often to request data from the simulator")
        parser.add_argument("output", help="the output file")

        return parser

    def request_fdm_data(self, args):
        agent = Agent(reactor)

        url = "http://%s:%d/fdm" % (args.host, args.port)

        d = agent.request("GET",
                          url,
                          Headers({}),
                          None)

        d.addCallback(self.process_fdm_data_response)

        return d

    def process_fdm_data_response(self, response):
        d = readBody(response)
        d.addCallback(self.save_fdm_data)
        return d

    def save_fdm_data(self, body):
        fdm_data = json.loads(body)

        self.csv_telemetry_writer.write_fdm_data(fdm_data)

        self.fdm_data_printer.print_fdm_data(fdm_data)

    def run(self, args):
        task = LoopingCall(self.request_fdm_data, args)
        task.start(args.dt)

        self.output_file = open(args.output, "w")

        self.csv_telemetry_writer = CSVFDMDataWriter(self.variables, self.output_file)
        self.csv_telemetry_writer.write_header()

        reactor.run()

        self.output_file.close()

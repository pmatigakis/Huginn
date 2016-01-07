from abc import ABCMeta, abstractmethod

from requests import ConnectionError
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

from huginn import configuration
from huginn.http import WebClient
from huginn.control import SimulatorControlClient
from huginn.clients import MapClient
from huginn.protocols import TelemetryClientFactory
from huginn.io import CSVTelemetryWriter, TelemetryPrinter


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

class TelemetryCommand(Command):
    def __init__(self):
        Command.__init__(self)

    def create_parser(self, subparsers):
        parser = subparsers.add_parser("telemetry", help="Record the flight telemetry")

        parser.add_argument("--port", default=configuration.TELEMETRY_PORT, help="Telemetry port")
        parser.add_argument("output", help="the output file")

        return parser

    def run(self, args):
        endpoint = TCP4ClientEndpoint(reactor, args.host, args.port)

        factory = TelemetryClientFactory()

        endpoint.connect(factory)

        with open(args.output, "w") as output_file:
            csv_telemetry_writer = CSVTelemetryWriter(output_file)
            factory.add_telemetry_listener(csv_telemetry_writer)

            telemetry_printer = TelemetryPrinter(
                variables=["time", "latitude", "longitude", "altitude", "airspeed",
                           "heading"]
            )

            factory.add_telemetry_listener(telemetry_printer)

            reactor.run()  # @UndefinedVariable

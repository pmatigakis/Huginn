#! python

from abc import ABCMeta, abstractmethod, abstractproperty
from os import path
import inspect
import signal
from xmlrpclib import ServerProxy
import logging

from huginn.web import app
from twisted.internet import reactor, task
from twisted.web import server
from flightsimlib import FGFDMExec

from huginn.protocols import FDMDataProtocol, ControlsProtocol, FDMDataClientProtocol, FDMControlsProtocol
from huginn.http import Index, FDMData, Controls
from huginn.rpc import FlightSimulatorRPC
import huginn

class Command(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def register_arguments(self, parser):
        pass
    
    @abstractmethod
    def execute(self, args):
        pass
    
    @abstractproperty
    def command_name(self):
        pass
    
    def setup_parser(self, subparsers):
        parser = subparsers.add_parser(self.command_name)
        
        self.register_arguments(parser)
        
        parser.set_defaults(command=self)
        
class StartSimulator(Command):
    DEFAULT_INTERFACES = {
        "rpc": 10500,
        "http": 8090,
        "fdm": 10300,
        "controls": 10301
    }

    command_name = "start"
    
    def init_logging(self):
        logging.basicConfig(format="%(asctime)s - %(module)s:%(levelname)s:%(message)s",
                            filename="huginn.log", 
                            filemode="a", 
                            level=logging.DEBUG)
    
    def init_fdm(self, dt, package_path):
        logging.debug("Initializing the flight dynamics model")
        
        fdmexec = FGFDMExec()
        
        jsbsim_data_path = path.join(package_path, "data/")
        
        logging.debug("Using jsbsim data at %s", jsbsim_data_path)
        
        fdmexec.set_root_dir(jsbsim_data_path)
        fdmexec.set_aircraft_path("aircraft")
        fdmexec.set_engine_path("engine")
        fdmexec.set_systems_path("systems")
    
        fdmexec.set_dt(dt)
    
        fdmexec.load_model("c172p")
    
        fdmexec.load_ic("reset01")
    
        fdmexec.set_property_value("fcs/throttle-cmd-norm", 0.65)
        fdmexec.set_property_value("fcs/mixture-cmd-norm", 0.87)
        fdmexec.set_property_value("propulsion/magneto_cmd", 3.0)
        fdmexec.set_property_value("propulsion/starter_cmd", 1.0)
    
        initial_condition_result = fdmexec.run_ic()
    
        if not initial_condition_result:
            logging.error("Failed to set the flight dynamics model's initial condition")
            print("Failed to set the flight dynamics model's initial condition")
            exit(-1)
    
        running = fdmexec.run()
        
        if not running:
            logging.error("Failed to make initial flight dynamics model run")
            print("Failed to make initial flight dynamics model run")
            exit(-1)
        
        while running and fdmexec.get_sim_time() < 0.1:
            fdmexec.process_message()
            fdmexec.check_incremental_hold()
    
            running = fdmexec.run()
            
        result = fdmexec.trim()    
        if not result:
            logging.error("Failed to trim the aircraft")
            print("Failed to trim the aircraft")
            exit(-1)
            
        return fdmexec

    def init_rpc_server(self, args, fdmexec):        
        rpc = FlightSimulatorRPC(fdmexec)
    
        rpc_port = args.rpc
        
        logging.debug("Starting the RPC server at port %d", rpc_port)
        
        reactor.listenTCP(rpc_port, server.Site(rpc))
    
    def init_web_server(self, args, fdmexec, package_path):
        index_page = Index(fdmexec)
        index_page.putChild("fdmdata", FDMData(fdmexec))
        index_page.putChild("controls", Controls(fdmexec))
        
        http_port = args.http
        
        logging.debug("Starting the web server at port %d", http_port)
        
        frontend = server.Site(index_page)
        reactor.listenTCP(http_port, frontend)
    
    def init_fdm_server(self, args, fdmexec):
        fdm_protocol = FDMDataProtocol(fdmexec)
        fdm_port = args.fdm
        
        logging.debug("Starting the flight dynamics model server at port %d", fdm_port)
        
        reactor.listenUDP(fdm_port, fdm_protocol)
    
        controls_protocol = ControlsProtocol(fdmexec) 
        controls_port = args.controls
        
        logging.debug("Starting the aircraft controls server at port %d", controls_port)
        
        reactor.listenUDP(controls_port, controls_protocol)

    def update_fdm(self, fdmexec):
        fdmexec.process_message()
        fdmexec.check_incremental_hold()
        running = fdmexec.run()
        
        if not running:
            logging.error("Failed to update the flight dynamics model")
            print("Failed to update the flight dynamics model")
            reactor.callFromThread(reactor.stop)
            
    def shutdown(self):
        logging.debug("Shutting down Huginn")
        
        reactor.callFromThread(reactor.stop)
        
    def register_arguments(self, parser):
        parser.add_argument("--properties", action="store_true", help="Print the property catalog")
        parser.add_argument("--rpc", action="store", default=self.DEFAULT_INTERFACES["rpc"], help="The XMLRPC port")
        parser.add_argument("--dt", action="store", default=0.0166, help="The simulation timestep")
        parser.add_argument("--http", action="store", default=self.DEFAULT_INTERFACES["http"], help="The web server port")
        parser.add_argument("--fdm", action="store", default=self.DEFAULT_INTERFACES["fdm"], help="The fdm data port")
        parser.add_argument("--controls", action="store", default=self.DEFAULT_INTERFACES["controls"], help="The controls port")
    
    def execute(self, args):
        self.init_logging()
        
        logging.info("Starting the Huginn flight simulator")
        
        dt = args.dt

        package_filename = inspect.getfile(huginn)
        package_path = path.dirname(package_filename)

        fdmexec = self.init_fdm(dt, package_path)

        if args.properties:
            fdmexec.print_property_catalog()
            exit()
            
        self.init_rpc_server(args, fdmexec)
    
        self.init_web_server(args, fdmexec, package_path)

        self.init_fdm_server(args, fdmexec)

        fdm_updater = task.LoopingCall(self.update_fdm, fdmexec)
        fdm_updater.start(dt)

        signal.signal(signal.SIGTERM, self.shutdown)

        fdmexec.hold()

        logging.debug("Starting the event loop")
        reactor.run()
        logging.info("The simulator has shut down")
        
class PrintFDMData(Command):
    FDM_HOST = "127.0.0.1"
    FDM_PORT = 10300
    
    command_name = "data"
    
    def register_arguments(self, parser):
        parser.add_argument("--host", action="store", default=self.FDM_HOST, help="the simulator ip address")
        parser.add_argument("--port", action="store", default=self.FDM_PORT, type=int, help="the simulator port")
        
    def execute(self, args):
        protocol = FDMDataClientProtocol(args.host, args.port)
        reactor.listenUDP(0, protocol)
        reactor.run()
        
class SimulatorControl(Command):
    RPC_HOST = "127.0.0.1"
    RPC_PORT = 10500
    
    command_name = "control"

    def reset_command(self, proxy):
        return proxy.reset()
    
    def pause_command(self, proxy):
        return proxy.pause()
    
    def unpause_command(self, proxy):
        return proxy.unpause()

    def register_arguments(self, parser):
        parser.add_argument("--host", action="store", default=self.RPC_HOST, help="The simulator host address")
        parser.add_argument("--port", action="store", default=self.RPC_PORT, type=int, help="The simulator port")
        
        subparsers = parser.add_subparsers()
        
        reset = subparsers.add_parser("reset")
        reset.set_defaults(func=self.reset_command)
        
        pause = subparsers.add_parser("pause")
        pause.set_defaults(func=self.pause_command)
        
        unpause = subparsers.add_parser("unpause")
        unpause.set_defaults(func=self.unpause_command)

    def execute(self, args):
        proxy = ServerProxy("http://%s:%s/" % (args.host, args.port))

        args.func(proxy)
        
class StartWebServer(Command):
    HTTP_HOST = "127.0.0.1"
    HTTP_PORT = 8080
    FDM_HOST = "127.0.0.1"
    FDM_PORT = 8090

    command_name = "web"
    
    def register_arguments(self, parser):
        parser.add_argument("--host", default=self.HTTP_HOST, help="The server ip address")
        parser.add_argument("--port", default=self.HTTP_PORT, type=int, help="The server port")
        parser.add_argument("--fdm_host", default=self.FDM_HOST, help="The fdm server ip address")
        parser.add_argument("--fdm_port", default=self.FDM_PORT, type=int, help="The fdm server port")
        parser.add_argument("--debug", action="store_true", help="Run in debug mode")

    def execute(self, args):
        app.config["FDM_HOST"] = args.fdm_host
        app.config["FDM_PORT"] = args.fdm_port
    
        app.run(host=args.host, port=args.port, debug=args.debug)

class SetControls(Command):
    FDM_HOST = "127.0.0.1"
    CONTROLS_PORT = 10301
    
    command_name = "controls"
    
    def register_arguments(self, parser):
        parser.add_argument("--host", default=self.FDM_HOST, help="the simulator ip address")
        parser.add_argument("--port", default=self.CONTROLS_PORT, type=int, help="the simulator port")
    
        parser.add_argument("aileron", type=float, help="aileron value")
        parser.add_argument("elevator", type=float, help="elevator value")
        parser.add_argument("rudder", type=float, help="rudder value")
        parser.add_argument("throttle", type=float, help="throttle value")

    def execute(self, args):
        controls = FDMControlsProtocol(args.host,
                                       args.port,
                                       args.aileron,
                                       args.elevator,
                                       args.rudder,
                                       args.throttle)
    
        reactor.listenUDP(0, controls)
        reactor.run()
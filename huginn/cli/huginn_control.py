from argparse import ArgumentParser

from huginn import configuration
from huginn.control import SimulatorControlClient

def get_arguments():
    parser = ArgumentParser(description="Huginn simulator control script")

    parser.add_argument("command", action="store",
                        choices=["pause", "resume", "reset", "step", "run_for"],
                        help="the simulator control command")

    parser.add_argument("--time_to_run", action="store", default=0.1,
                        help="The time in seconds to run the simulator")

    parser.add_argument("--host", action="store", default="127.0.0.1", help="the simulator ip address")
    parser.add_argument("--web_port", action="store", default=configuration.WEB_SERVER_PORT, type=int, help="the simulator http port")

    return parser.parse_args()

def main():
    args = get_arguments()

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

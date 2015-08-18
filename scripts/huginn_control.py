from argparse import ArgumentParser
from xmlrpclib import ServerProxy

from huginn.configuration import HUGINN_HOST, RPC_PORT

def reset_command(proxy):
    return proxy.reset()

def pause_command(proxy):
    return proxy.pause()

def resume_command(proxy):
    return proxy.resume()

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator control")
    
    parser.add_argument("--host", action="store", default=HUGINN_HOST, help="the simulator ip address")
    parser.add_argument("--port", action="store", default=RPC_PORT, type=int, help="the flight dynamics RPC port")
    
    subparsers = parser.add_subparsers()
        
    reset = subparsers.add_parser("reset")
    reset.set_defaults(func=reset_command)
        
    pause = subparsers.add_parser("pause")
    pause.set_defaults(func=pause_command)
        
    unpause = subparsers.add_parser("resume")
    unpause.set_defaults(func=resume_command)

    return parser.parse_args()
    
def main():
    args = get_arguments()
    
    proxy = ServerProxy("http://%s:%s/" % (args.host, args.port))

    args.func(proxy)

if __name__ == "__main__":
    main()
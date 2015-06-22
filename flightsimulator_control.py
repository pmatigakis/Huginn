#! python

from xmlrpclib import ServerProxy
from argparse import  ArgumentParser

def reset_command(proxy):
    return proxy.reset()

def pause_command(proxy):
    return proxy.pause()

def unpause_command(proxy):
    return proxy.unpause()

def get_arguments():
    parser = ArgumentParser(description="Flight simulator control client")
    
    parser.add_argument("host", help="The simulator host address")
    parser.add_argument("port", type=int, help="The simulator port")
    
    subparsers = parser.add_subparsers()
    
    reset = subparsers.add_parser("reset")
    reset.set_defaults(func=reset_command)
    
    pause = subparsers.add_parser("pause")
    pause.set_defaults(func=pause_command)
    
    unpause = subparsers.add_parser("unpause")
    unpause.set_defaults(func=unpause_command)
    
    return parser.parse_args()

def main():
    args = get_arguments()

    proxy = ServerProxy("http://%s:%s/" % (args.host, args.port))

    args.func(proxy)

if __name__ == "__main__":
    main()
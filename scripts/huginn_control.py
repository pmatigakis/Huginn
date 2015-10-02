from argparse import ArgumentParser
import json

import requests

from huginn.configuration import HUGINN_HOST, WEB_SERVER_PORT


def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator control")
    
    parser.add_argument("--host", action="store", default=HUGINN_HOST, help="the simulator ip address")
    parser.add_argument("--port", action="store", default=WEB_SERVER_PORT, type=int, help="the flight dynamics RPC port")
    parser.add_argument("command", action="store",
                        choices=["pause", "resume", "reset"], 
                        help="the simulator control command")

    return parser.parse_args()

def main():
    args = get_arguments()
    
    response = requests.post("http://%s:%d/simulator" % (args.host, args.port),
                             data={"command": args.command})

    response_data = json.loads(response.text)

    if response_data["result"] != "ok":
        print("ERROR: %s" % response_data["reason"]) 

if __name__ == "__main__":
    main()
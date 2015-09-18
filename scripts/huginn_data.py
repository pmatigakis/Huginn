from argparse import ArgumentParser
import requests
import json

from huginn.configuration import WEB_SERVER_PORT, HUGINN_HOST


def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator data viewer")
    
    parser.add_argument("--host", action="store", default=HUGINN_HOST, help="the simulator ip address")
    parser.add_argument("--port", action="store", default=WEB_SERVER_PORT, type=int, help="the flight dynamics model http port")

    return parser.parse_args()

def main():
    args = get_arguments()

    response = requests.get("http://%s:%d/fdmdata" % (args.host, args.port))
    
    data = json.loads(response.text)

    if data["result"] != "ok":
        print("Failed to get the fdm data from the web server")
        exit(-1)

    for fdm_property in data["fdm_data"]:
        print('%s: %f' % (fdm_property, data["fdm_data"][fdm_property]))

if __name__ == "__main__":
    main()
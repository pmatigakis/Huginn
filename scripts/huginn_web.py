#!/usr/bin/env python

from argparse import ArgumentParser

from huginn.web import app
from huginn import configuration

def get_arguments():
    parser = ArgumentParser(description="Web front end for Huginn")

    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--host", action="store", default="127.0.0.1", help="The host address")
    parser.add_argument("--port", action="store", default=5000, help="The port to listen on")
    parser.add_argument("--huginn_host", action="store", default="127.0.0.1", help="The simulator host address")
    parser.add_argument("--huginn_web_port", action="store", default=configuration.WEB_SERVER_PORT, help="The huginn web server port")

    return parser.parse_args()

def main():
    args = get_arguments()

    #TODO: add something better here
    app.secret_key = "asadasdasdasdasdasdas"

    app.config["huginn_host"] = args.huginn_host
    app.config["huginn_web_port"] = args.huginn_web_port

    app.run(host=args.host,
            port=args.port,
            debug=args.debug)

if __name__ == "__main__":
    main()

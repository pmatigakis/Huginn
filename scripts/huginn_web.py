from argparse import ArgumentParser

from huginn.web import app
from huginn.configuration import HUGINN_HOST, HTTP_PORT, WEB_SERVER_PORT

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator web server")
    
    parser.add_argument("--host", default=HUGINN_HOST, help="The server ip address")
    parser.add_argument("--port", default=HTTP_PORT, type=int, help="The server port")
    parser.add_argument("--fdm_port", default=WEB_SERVER_PORT, type=int, help="The fdm server http port")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")

    return parser.parse_args()

def main():
    args = get_arguments()
    
    app.config["FDM_HOST"] = args.host
    app.config["FDM_PORT"] = args.fdm_port
    
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
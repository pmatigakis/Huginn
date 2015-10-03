from argparse import ArgumentParser

from huginn.web.servers import HuginnWebServer
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
    
    web_server = HuginnWebServer(args.host, args.fdm_port, args.host, args.port, debug=True)

    web_server.run()

if __name__ == "__main__":
    main()
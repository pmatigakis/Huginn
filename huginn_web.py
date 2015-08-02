from argparse import ArgumentParser

from huginn.web import app

HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8080

FDM_HOST = "127.0.0.1"
FDM_PORT = 8090

def get_arguments():
    parser = ArgumentParser(description="Huginn web server")
    
    parser.add_argument("--host", default=HTTP_HOST, help="The server ip address")
    parser.add_argument("--port", default=HTTP_PORT, type=int, help="The server port")
    parser.add_argument("--fdm_host", default=FDM_HOST, help="The fdm server ip address")
    parser.add_argument("--fdm_port", default=FDM_PORT, type=int, help="The fdm server port")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    return parser.parse_args()

def main():
    args = get_arguments()
    
    app.config["FDM_HOST"] = args.fdm_host
    app.config["FDM_PORT"] = args.fdm_port
    
    app.run(host=args.host, port=args.port, debug=args.debug)
    
if __name__ == "__main__":
    main()
from argparse import ArgumentParser

from huginn.commands import StartSimulator, PrintFDMData, SimulatorControl, StartWebServer, SetControls

def parse_arguments(commands):
    parser = ArgumentParser(description="Huginn flight simulator command line interface")
    
    subparsers = parser.add_subparsers()
    
    for command in commands:
        command_instance = command()
        
        command_instance.setup_parser(subparsers)
    
    return parser.parse_args()

def main():    
    commands = [StartSimulator,
                PrintFDMData,
                SimulatorControl,
                StartWebServer,
                SetControls]
    
    args = parse_arguments(commands)

    args.command.execute(args)

if __name__ == "__main__":
    main()
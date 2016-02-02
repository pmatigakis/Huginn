#!/usr/bin/env python

from argparse import ArgumentParser

from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

from huginn.serialport import AutopilotBoardAdapter, AircraftControlsListener
from huginn.protocols import ControlsClient, FDMDataClient
from huginn import configuration

class ControlDataPrinter(AircraftControlsListener):
    def controls_received(self, aileron, elevator, rudder, throttle):
        print("aileron: %f, elevator: %f, rudder: %f, throtle: %f" % (aileron, elevator, rudder, throttle))

def get_arguments():
    parser = ArgumentParser(description="Huginn serial port interface utility")

    parser.add_argument("port", action="store", help="The serial port device to use")
    parser.add_argument("--baud", action="store", default=57600, help="The baudrate to use")
    parser.add_argument("--host", action="store", default="127.0.0.1", help="The address to Huginn")
    parser.add_argument("--controls_port", action="store", default=configuration.CONTROLS_PORT, help="The Huginn control port")
    parser.add_argument("--fdm_port", action="store", default=configuration.FDM_CLIENT_PORT, help="The port that this utility listen to for fdm data")

    return parser.parse_args()

def main():
    args = get_arguments()

    fdm_data_client = FDMDataClient()
    controls_client = ControlsClient(args.host, args.controls_port)

    protocol = AutopilotBoardAdapter(controls_client)

    fdm_data_client.add_fdm_data_listener(protocol)

    protocol.add_controls_listener(ControlDataPrinter())
    
    s = SerialPort(protocol,"/dev/ttyACM0", reactor, args.baud)
    reactor.listenUDP(0, controls_client)
    reactor.listenUDP(args.fdm_port, fdm_data_client)

    reactor.run()

if __name__ == "__main__":
    main()

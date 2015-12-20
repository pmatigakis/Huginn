#!/usr/bin/env python

from argparse import ArgumentParser
from requests import ConnectionError

from huginn.configuration import WEB_SERVER_PORT
from huginn.http import WebClient

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator data viewer")

    parser.add_argument("--host", action="store", default="127.0.0.1", help="the simulator ip address")
    parser.add_argument("--port", action="store", default=WEB_SERVER_PORT, type=int, help="the flight dynamics model http port")

    return parser.parse_args()

def print_gps_data(web_client):
    data = web_client.get_gps_data()

    print("GPS data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_accelerometer_data(web_client):
    data = web_client.get_accelerometer_data()

    print("Accelerometer data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_gyroscope_data(web_client):
    data = web_client.get_gyroscope_data()

    print("Gyroscope data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_thermometer_data(web_client):
    data = web_client.get_thermometer_data()

    print("Thermometer data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_pressure_sensor_data(web_client):
    data = web_client.get_pressure_sensor_data()

    print("Pressure sensor data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_pitot_tube_data(web_client):
    data = web_client.get_pitot_tube_data()

    print("Pitot tube data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_ins_data(web_client):
    data = web_client.get_ins_data()

    print("Inertial navigation system data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_engine_data(web_client):
    data = web_client.get_engine_data()

    print("Engine data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_flight_controls_data(web_client):
    data = web_client.get_flight_controls()

    print("Flight controls data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def main():
    args = get_arguments()

    web_client = WebClient(args.host, args.port)

    try:
        print_gps_data(web_client)
        print_accelerometer_data(web_client)
        print_gyroscope_data(web_client)
        print_thermometer_data(web_client)
        print_pressure_sensor_data(web_client)
        print_pitot_tube_data(web_client)
        print_ins_data(web_client)
        print_engine_data(web_client)
        print_flight_controls_data(web_client)
    except ConnectionError:
        print("Failed to connect to Huginn's web server")

if __name__ == "__main__":
    main()
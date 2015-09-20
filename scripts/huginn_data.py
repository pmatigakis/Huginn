from argparse import ArgumentParser
import requests
import json

from huginn.configuration import WEB_SERVER_PORT, HUGINN_HOST

def get_arguments():
    parser = ArgumentParser(description="Huginn flight simulator data viewer")

    parser.add_argument("--host", action="store", default=HUGINN_HOST, help="the simulator ip address")
    parser.add_argument("--port", action="store", default=WEB_SERVER_PORT, type=int, help="the flight dynamics model http port")

    return parser.parse_args()

def print_gps_data(host, port):
    response = requests.get("http://%s:%d/gps" % (host, port))

    data = json.loads(response.text)

    print("GPS data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_accelerometer_data(host, port):
    response = requests.get("http://%s:%d/accelerometer" % (host, port))

    data = json.loads(response.text)

    print("Accelerometer data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_gyroscope_data(host, port):
    response = requests.get("http://%s:%d/gyroscope" % (host, port))

    data = json.loads(response.text)

    print("Gyroscope data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_thermometer_data(host, port):
    response = requests.get("http://%s:%d/thermometer" % (host, port))

    data = json.loads(response.text)

    print("Thermometer data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_pressure_sensor_data(host, port):
    response = requests.get("http://%s:%d/pressure_sensor" % (host, port))

    data = json.loads(response.text)

    print("Pressure sensor data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_pitot_tube_data(host, port):
    response = requests.get("http://%s:%d/pitot_tube" % (host, port))

    data = json.loads(response.text)

    print("Pitot tube data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_ins_data(host, port):
    response = requests.get("http://%s:%d/ins" % (host, port))

    data = json.loads(response.text)

    print("Inertial navigation system data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_engine_data(host, port):
    response = requests.get("http://%s:%d/engine" % (host, port))

    data = json.loads(response.text)

    print("Engine data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def print_flight_controls_data(host, port):
    response = requests.get("http://%s:%d/flight_controls" % (host, port))

    data = json.loads(response.text)

    print("Flight controls data")
    print("========")

    for fdm_property in data:
        print('%s: %f' % (fdm_property, data[fdm_property]))

    print("")

def main():
    args = get_arguments()

    print_gps_data(args.host, args.port)
    print_accelerometer_data(args.host, args.port)
    print_gyroscope_data(args.host, args.port)
    print_thermometer_data(args.host, args.port)
    print_pressure_sensor_data(args.host, args.port)
    print_pitot_tube_data(args.host, args.port)
    print_ins_data(args.host, args.port)
    print_engine_data(args.host, args.port)
    print_flight_controls_data(args.host, args.port)

if __name__ == "__main__":
    main()
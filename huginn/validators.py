import re
from argparse import ArgumentTypeError

def port_number(value):
    try:
        port_number = int(value)
    except ValueError:
        raise ArgumentTypeError("%s is not a valid port number" % value)
    
    if port_number < 1 or port_number > 65535:
        raise ArgumentTypeError("Given port number must be in the range 1-65535")
    
    return port_number

def fdm_data_endpoint(value):    
    match = re.match(r"^(\d+\.\d+.\d+.\d+),(\d+),(\d+\.\d+)$", value.strip())

    if not match:
        raise ArgumentTypeError("The fdm data endpoint must be in the form IP,PORT,DT")
    
    ip = match.group(1)
    port = port_number(match.group(2))
    dt = float(match.group(3))

    return ip, port, dt

def telemetry_endpoint(value):
    match = re.match(r"^(\d+),(\d+\.\d+)$", value.strip())

    if not match:
        raise ArgumentTypeError("The telemetry endpoint must be in the form PORT,DT")
    
    port = port_number(match.group(1))
    dt = float(match.group(2))

    return port, dt

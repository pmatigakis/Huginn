"""
the huginn.validators module contains functions that are using to validate
input arguments
"""

import re
from argparse import ArgumentTypeError

def port_number(value):
    """Check if the given value is a valid port number"""
    try:
        parsed_port_number = int(value)
    except ValueError:
        raise ArgumentTypeError("%s is not a valid port number" % value)

    if parsed_port_number < 1 or parsed_port_number > 65535:
        raise ArgumentTypeError("Given port number must be in the range 1-65535")

    return parsed_port_number

def fdm_data_endpoint(value):
    """Check if the given value if a valid fdm data endpoint address"""
    match = re.match(r"^(\d+\.\d+.\d+.\d+),(\d+),(\d+\.\d+)$", value.strip())

    if not match:
        raise ArgumentTypeError("The fdm data endpoint must be "
                                "in the form IP,PORT,DT")

    ip = match.group(1)
    port = port_number(match.group(2))
    dt = float(match.group(3))

    return ip, port, dt

def is_valid_latitude(latitude):
    """Check if the given argument is within the range -90 to 90 degrees

    Arguments:
    latitude: check is this latitude is valid"""
    if latitude > 90.0 or latitude < -90.0:
        return False

    return True

def is_valid_longitude(longitude):
    """Check if the given argument is within the range -180 to 180 degrees

    Arguments:
    longitude: check is this longitude is valid"""
    if longitude > 180.0 or longitude < -180.0:
        return False

    return True

def is_valid_heading(heading):
    """Check if the given argument is within the range 0.0 to 360 degrees

    Arguments:
    heading: check is this heading is valid"""
    if heading > 360.0 or heading < 0.0:
        return False

    return True

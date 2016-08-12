from argparse import ArgumentTypeError
import re


def latitude(value):
    """Latitude cli argument type

    Arguments:
    value: the latitude

    Return the latitude or raises ArgumentTypeError if the latitude is not
    valid
    """
    try:
        value = float(value)
    except ValueError:
        raise ArgumentTypeError("{} is not a number".format(value))

    if value > 90.0 or value < -90.0:
        raise ArgumentTypeError("Invalid latitude")

    return value


def longitude(value):
    """Longitude cli argument type

    Arguments:
    value: the longitude

    Return the longitude or raises ArgumentTypeError if the longitude is not
    valid
    """
    try:
        value = float(value)
    except ValueError:
        raise ArgumentTypeError("{} is not a number".format(value))

    if value > 180.0 or value < -180.0:
        raise ArgumentTypeError("Invalid longitude")

    return value


def altitude(value):
    """Altitude cli argument type

    Arguments:
    value: the altitude

    Return the altitude or raises ArgumentTypeError if the altitude is not
    valid
    """
    try:
        value = float(value)
    except ValueError:
        raise ArgumentTypeError("{} is not a number".format(value))

    if value < 0.0:
        raise ArgumentTypeError("Invalid altitude")

    return value


def heading(value):
    """Heading cli argument type

    Arguments:
    value: the heading

    Return the heading or raises ArgumentTypeError if the heading is not
    valid
    """
    try:
        value = float(value)
    except ValueError:
        raise ArgumentTypeError("{} is not a number".format(value))

    if value < 0.0 or value > 360.0:
        raise ArgumentTypeError("Invalid heading")

    return value


def airspeed(value):
    """Airspeed cli argument type

    Arguments:
    value: the heading

    Return the heading or raises ArgumentTypeError if the heading is not
    valid
    """
    try:
        value = float(value)
    except ValueError:
        raise ArgumentTypeError("{} is not a number".format(value))

    if value < 0.0:
        raise ArgumentTypeError("Invalid airspeed")

    return value


def update_rate(value):
    """Simulator update rate cli argument type

    Arguments:
    value: the update rate

    Return the update rate or raises ArgumentTypeError if the update rate is
    not valid
    """
    try:
        value = float(value)
    except ValueError:
        raise ArgumentTypeError("{} is not a number".format(value))

    if value < 0.00001:
        raise ArgumentTypeError("Invalid update rate")

    return value


def port_number(value):
    """Check if the given value is a valid port number"""
    try:
        parsed_port_number = int(value)
    except ValueError:
        raise ArgumentTypeError("%s is not a valid port number" % value)

    if parsed_port_number < 1 or parsed_port_number > 65535:
        raise ArgumentTypeError("Given port number must be in the range "
                                "1-65535")

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

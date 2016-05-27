"""
the huginn.unit_conversions module contains function that perform conversions
between different measurement unit types
"""


def convert_feet_to_meters(feet):
    """Convert from feet to meters"""
    return feet * 0.3048


def convert_meters_to_feet(meters):
    """Convert from meters to feet"""
    return meters / 0.3048


def convert_knots_to_meters_per_sec(knots):
    """Convert from knots to meters per second"""
    return knots * 0.514444


def convert_meters_per_sec_to_knots(mps):
    """Convert from meters per second to knots"""
    return mps / 0.514444


def convert_rankine_to_kelvin(temperature):
    """Convert from degrees rankine to kelvin"""
    return temperature * (5.0/9.0)


def convert_psf_to_pascal(pressure):
    """convert from pounds per sware foot to Pascal"""
    return pressure * 47.8802588889


def convert_pounds_to_newtons(pounds):
    """Convert pounds to Newtons"""
    return pounds * 4.44822162


def convert_libra_to_newtons(libra):
    """Convert from libres to newtons"""
    return libra * 3.16754795925

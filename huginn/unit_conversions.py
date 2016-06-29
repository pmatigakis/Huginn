"""
the huginn.unit_conversions module contains function that perform conversions
between different measurement unit types
"""


from pint import UnitRegistry


ur = UnitRegistry()

ur.define("pound_foot = pound / foot = lbsft = pound_feet")
ur.define("newton_meter = 0.737562149277 * pound_foot  = N_m")
ur.define("feet_per_second = feet / second = fps")
ur.define("meters_per_second = meter / second = mps")
ur.define("feet_per_minute = foot / minute = fpm")
ur.define("pound_force_per_square_foot = pound * gravity / foot ** 2 = psf")
ur.define("slug = 14.5939 * kilogram")
ur.define("slug_per_cubic_feet = slug / (foot ** 3.0)")
ur.define("kilogram_per_cubic_meter = kilogram / (meter ** 3.0)")


def convert_jsbsim_acceleration(acceleration):
    """Convert the acceleration from the units used in JSBSim to
    meters/sec^2"""
    acceleration = acceleration * (ur.foot / (ur.second ** 2.0))

    acceleration.ito(ur.meter / (ur.second ** 2.0))

    return acceleration.magnitude


def convert_jsbsim_angular_acceleration(acceleration):
    """Convert the angular acceleration from the units used in JSBSim to
    degrees/sec^2"""
    acceleration = acceleration * (ur.radian / (ur.second ** 2.0))

    acceleration.ito(ur.degree / (ur.second ** 2.0))

    return acceleration.magnitude


def convert_jsbsim_angular_velocity(velocity):
    """Convert the angular velocity from the units used in JSBSim to
    degrees/sec"""
    velocity = velocity * (ur.radian / ur.second)

    velocity.ito(ur.degree / ur.second)

    return velocity.magnitude


def convert_jsbsim_velocity(velocity):
    """Convert the velocity from the units used in JSBSim to meters/sec"""
    velocity = velocity * ur.feet_per_second

    velocity.ito(ur.meters_per_second)

    return velocity.magnitude


def convert_jsbsim_pressure(pressure):
    """Convert the pressure from the units used in JSBSim to pascal"""
    pressure = pressure * ur.pound_force_per_square_foot

    pressure.ito(ur.pascal)

    return pressure.magnitude


def convert_jsbsim_temperature(temperature):
    """Convert the temperature from the units used in JSBSim to Kelvin"""
    temperature = temperature * ur.rankine

    temperature.ito(ur.kelvin)

    return temperature.magnitude


def convert_jsbsim_density(density):
    """Convert the density from the units used in JSBSim to kg/meters^3"""
    density = density * ur.slug_per_cubic_feet

    density.ito(ur.kilogram_per_cubic_meter)

    return density.magnitude


def convert_jsbsim_force(force):
    """Convert the force from the units used in JSBSim to Newtons"""
    force = force * ur.force_pound

    force.ito(ur.newton)

    return force.magnitude

from marshmallow import Schema, fields


class AccelerationsSchema(Schema):
    x = fields.Float()
    y = fields.Float()
    z = fields.Float()
    p_dot = fields.Float()
    q_dot = fields.Float()
    r_dot = fields.Float()
    u_dot = fields.Float()
    v_dot = fields.Float()
    w_dot = fields.Float()
    gravity = fields.Float()


class VelocitiesSchema(Schema):
    p = fields.Float()
    q = fields.Float()
    r = fields.Float()
    u = fields.Float()
    v = fields.Float()
    w = fields.Float()
    true_airspeed = fields.Float()
    climb_rate = fields.Float()
    calibrated_airspeed = fields.Float()
    equivalent_airspeed = fields.Float()
    ground_speed = fields.Float()


class OrientationSchema(Schema):
    phi = fields.Float()
    theta = fields.Float()
    psi = fields.Float()


class AtmosphereShema(Schema):
    pressure = fields.Float()
    sea_level_pressure = fields.Float()
    temperature = fields.Float()
    sea_level_temperature = fields.Float()
    density = fields.Float()
    sea_level_density = fields.Float()

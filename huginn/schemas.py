from marshmallow import Schema, fields


class AccelerationsSchema(Schema):
    x = fields.Float()
    y = fields.Float()
    z = fields.Float()


class VelocitiesSchema(Schema):
    roll_rate = fields.Float()
    pitch_rate = fields.Float()
    yaw_rate = fields.Float()
    airspeed = fields.Float()
    climb_rate = fields.Float()

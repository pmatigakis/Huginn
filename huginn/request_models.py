from flask_restful import fields

# the waypoint model contains the data of a waypoint
waypoint = {
    "name": fields.String,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "altitude": fields.Float
}

from flask_restful import reqparse

from huginn.cli import argtypes

# the waypoint request parser is used to parse the waypoint data from a web
# request
waypoint = reqparse.RequestParser()
waypoint.add_argument("latitude", required=True,
                      location="json", type=argtypes.latitude)
waypoint.add_argument("longitude", required=True,
                      location="json", type=argtypes.longitude)
waypoint.add_argument("altitude", required=True,
                      location="json", type=argtypes.altitude)

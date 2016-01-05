import csv
from math import radians, sin, cos, asin, sqrt, atan2, pi, fmod, degrees

from twisted.internet import reactor, task

from huginn.protocols import FDMDataClient, FDMDataListener, ControlsClient 

def haversine_distance(latitude1, longitude1, latitude2, longitude2):
    R = 6372.8 # Earth radius in kilometers
    dLat = radians(latitude2 - latitude1)
    dLon = radians(longitude2 - longitude1)
    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    a = sin(dLat/2.0)**2.0 + cos(lat1)*cos(lat2)*sin(dLon/2.0)**2.0
    c = 2.0*asin(sqrt(a))

    return 1000.0 * (R * c)

def bearing(latitude1, longitude1, latitude2, longitude2):
    dLon = radians(longitude2 - longitude1)
    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    a = sin(dLon) * cos(lat2)
    b = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)

    return degrees(fmod(atan2(a, b), 2.0 * pi))

class PID(object):
    def __init__(self, kp, ki, kd, dt, max_error):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.max_error = max_error

        self.last_error = 0.0
        self.error_sum = 0.0

    def run(self, error):
        self.error_sum += error

        if self.error_sum > self.max_error:
            self.error_sum = self.max_error

        if self.error_sum < -self.max_error:
            self.error_sum = -self.max_error

        result =  error * self.kp + self.ki * self.error_sum * self.dt + self.kd * self.last_error / self.dt;

        self.last_error = error

        return result

class Autopilot(FDMDataListener):
    def __init__(self, controls_client, waypoints):
        self.controls_client = controls_client

        self.waypoints = waypoints

        self.current_waypoint_index = 0

        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.airspeed = 0.0
        self.heading = 0.0
        self.roll = 0.0
        self.pitch = 0.0

        self.aileron = 0.0
        self.elevator = 0.0
        self.rudder = 0.0
        self.throttle = 0.0

        self.throttle_pid = PID(0.1, 0.05, 0.01, 0.1, 10.0)
        self.pitch_pid = PID(1.0, 0.0, 0.0, 0.1, 50.0)
        self.elevator_pid = PID(0.001, 0.0005, 0.005, 0.1, 10.0) 
        self.roll_pid = PID(1.0, 0.0, 0.0, 0.1, 50.0)
        self.aileron_pid = PID(0.001, 0.0005, 0.005, 0.1, 10.0)

    def set_target(self, latitude, longitude, altitude, airspeed):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.airspeed = airspeed

    def distance_from_target(self):
        target_latitude, target_longitude, target_altitude, target_airspeed = self.waypoints[self.current_waypoint_index]

        return haversine_distance(self.latitude, self.longitude, target_latitude, target_longitude)

    def bearing_to_waypoint(self):
        target_latitude, target_longitude, target_altitude, target_airspeed = self.waypoints[self.current_waypoint_index]

        return bearing(self.latitude, self.longitude, target_latitude, target_longitude)

    def update_throttle(self):
        target_airspeed = self.waypoints[self.current_waypoint_index][3]

        airspeed_error = target_airspeed - self.airspeed

        self.throttle = self.throttle_pid.run(airspeed_error)

        if self.throttle > 1.0:
            self.throttle = 1.0
        elif self.throttle < 0.0:
            self.throttle = 0.0 

    def update_aileron(self):
        target_bearing = self.bearing_to_waypoint()

        if target_bearing > 0.0:        
            target_heading = target_bearing
        else:
            target_heading = 360 + target_bearing

        #heading_error = target_bearing - self.heading
        heading_error = target_heading - self.heading

        #FIXME: this is ugly
        if heading_error > 180.0:
            heading_error = -(heading_error - 180.0 + self.heading)

        target_roll = self.roll_pid.run(heading_error)

        if target_roll > 20.0:
            target_roll = 20.0
        elif target_roll < -20.0:
            target_roll = -20.0

        roll_error = target_roll - self.roll

        self.aileron = self.aileron_pid.run(roll_error)

        if self.aileron > 1.0:
            self.aileron = 1.0
        elif self.aileron < -1.0:
            self.aileron = -1.0

    def update_elevator(self):
        target_altitude = self.waypoints[self.current_waypoint_index][2]

        altitude_error = target_altitude - self.altitude 

        target_pitch = self.pitch_pid.run(altitude_error)

        if target_pitch > 20.0:
            target_pitch = 20.0
        elif target_pitch < -20.0:
            target_pitch = -20.0

        pitch_error = target_pitch - self.pitch 

        self.elevator = -self.elevator_pid.run(pitch_error)

        if self.elevator > 1.0:
            self.elevator = 1.0
        elif self.elevator < -1.0:
            self.elevator = -1.0

    def update_rudder(self):
        self.rudder = 0.0

    def run(self):
        if self.distance_from_target() < 50.0:
            self.current_waypoint_index += 1
            self.current_waypoint_index %= len(self.waypoints)
        
        self.update_throttle()
        self.update_elevator()
        self.update_aileron()
        self.update_rudder()

    def print_log(self):
        waypoint = self.waypoints[self.current_waypoint_index]

        print("Going to %f %f" % (waypoint[0], waypoint[1]))
        print("waypoint index %d" % self.current_waypoint_index)
        print("distance from waypoint %f" % self.distance_from_target())
        print("bearing to target %f" % self.bearing_to_waypoint())
        print("course %f" % self.heading)
        print("aIleron %f" % self.aileron)
        print("elevator %f" % self.elevator)
        print("rudder %f" % self.rudder)
        print("throttle %f" % self.throttle)
        print("")

    def fdm_data_received(self, fdm_data):
        self.latitude = fdm_data.gps.latitude
        self.longitude = fdm_data.gps.longitude
        self.altitude = fdm_data.gps.altitude
        self.airspeed = fdm_data.gps.airspeed
        self.heading = fdm_data.gps.heading

        self.roll = fdm_data.ins.roll
        self.pitch = fdm_data.ins.pitch

        self.run()

        self.controls_client.transmit_controls(self.aileron,
                                               self.elevator,
                                               self.rudder,
                                               self.throttle)

controls_client = ControlsClient("127.0.0.1", 10301)
reactor.listenUDP(0, controls_client)

altitude = 300.0
airspeed = 30.0

waypoints = []

with open("waypoints.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")

    for row in reader:
        waypoint = [float(row[1]), float(row[2]), altitude, airspeed]
        waypoints.append(waypoint)

autopilot = Autopilot(controls_client, waypoints)

fdm_data_client = FDMDataClient()
fdm_data_client.add_fdm_data_listener(autopilot)
reactor.listenUDP(10302, fdm_data_client)

log_updater = task.LoopingCall(autopilot.print_log)
log_updater.start(1.0)

reactor.run()
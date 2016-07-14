from math import degrees

from huginn.protocols import SimulatorDataListener
from huginn.protobuf import fdm_pb2

class MockAuxiliary(object):
    def __init__(self):
        self.v_true = 375.453302
        self.total_pressure = 12233.2
        self.euler_rates = [1.1, 2.2, 3.3]
        self.accelerations = [0.1, 0.2, 0.3]

    def GetVtrueFPS(self):
        return self.v_true

    def GetTotalPressure(self):
        return self.total_pressure

    def GetEulerRates(self, index):
        return self.euler_rates[index-1]

    def GetPilotAccel(self, index):
        return self.accelerations[index-1]

class MockEuler(object):
    def __init__(self):
        self.entries = [0.1, 0.2, 0.3]

    def Entry(self, index):
        return self.entries[index-1]

class MockPropagate(object):
    def __init__(self):
        self.latitude = 37.34567
        self.longitude = 21.63457
        self.altitude = 10000.0
        self.euler = MockEuler() 

    def GetLatitudeDeg(self):
        return self.latitude

    def GetLongitudeDeg(self):
        return self.longitude

    def GetAltitudeASLmeters(self):
        return self.altitude

    def GetEuler(self):
        return self.euler

    def GetEulerDeg(self):
        mock_euler_deg = MockEuler()
        mock_euler_deg.entries[0] = degrees(self.euler.entries[0])
        mock_euler_deg.entries[1] = degrees(self.euler.entries[1])
        mock_euler_deg.entries[2] = degrees(self.euler.entries[2])
        
        return mock_euler_deg

    def DumpState(self):
        pass

class MockFCS(object):
    def __init__(self):
        self.aileron_cmd = 0.55
        self.elevator_cmd = 0.23
        self.rudder_cmd = 0.7
        self.throttle_cmd  = 0.86

    def GetDaCmd(self):
        return self.aileron_cmd

    def GetDeCmd(self):
        return self.elevator_cmd

    def GetDrCmd(self):
        return self.rudder_cmd

    def GetThrottleCmd(self, index):
        return self.throttle_cmd

    def SetThrottleCmd(self, idex, throttle_cmd):
        self.throttle_cmd = throttle_cmd

    def SetDeCmd(self, elevator):
        self.elevator_cmd = elevator

    def SetDrCmd(self, rudder_cmd):
        self.rudder_cmd = rudder_cmd

    def SetDaCmd(self, aileron_cmd):
        self.aileron_cmd = aileron_cmd

class MockAtmosphere(object):
    def __init__(self):
        self.temperature = 567.32
        self.pressure = 456.39

    def GetTemperature(self):
        return self.temperature

    def GetPressure(self):
        return self.pressure

class MockThruster(object):
    def __init__(self):
        self.thrust = 3452.87

    def GetThrust(self):
        return self.thrust

class MockEngine(object):
    def __init__(self):
        self.thruster = MockThruster()
        self.throttle = 0.48

    def GetThruster(self):
        return self.thruster

class MockPropulsion(object):
    def __init__(self):
        self.engine = MockEngine()

    def GetEngine(self, index):
        return self.engine 

    def GetNumEngines(self):
        return 1

class MockFDMExec(object):
    def __init__(self):
        self.propagate = MockPropagate()
        self.auxiliary = MockAuxiliary()
        self.fcs = MockFCS()
        self.atmosphere = MockAtmosphere()
        self.propulsion = MockPropulsion()
        self.sim_time = 32.45
        self.dt = 1.0 / 160.0

        self.properties = {
            "simulation/sim-time-sec": self.sim_time,
            "atmosphere/P-psf": 456.39,
            "atmosphere/T-R": 567.32,
            "aero/qbar-psf": 12233.2,
            "velocities/p-rad_sec": 1.1,
            "velocities/q-rad_sec": 2.2,
            "velocities/r-rad_sec": 3.3,
            "attitude/heading-true-rad": 0.3,
            "position/long-gc-deg": 21.63457,
            "position/lat-gc-deg": 37.34567,
            "position/h-sl-ft": 32808.4,
            "velocities/vtrue-kts": 222.45,
            "propulsion/engine/thrust-lbs": 3452.87,
            "fcs/throttle-cmd-norm": 0.86,
            "fcs/rudder-cmd-norm": 0.7,
            "fcs/elevator-cmd-norm": 0.23,
            "fcs/aileron-cmd-norm": 0.55,
            "accelerations/a-pilot-x-ft_sec2": 0.1,
            "accelerations/a-pilot-y-ft_sec2": 0.2,
            "accelerations/a-pilot-z-ft_sec2": 0.3
        }

    def GetPropulsion(self):
        return self.propulsion

    def GetAtmosphere(self):
        return self.atmosphere

    def GetAuxiliary(self):
        return self.auxiliary

    def GetPropagate(self):
        return self.propagate

    def GetSimTime(self):
        return self.sim_time

    def GetDeltaT(self):
        return self.dt

    def GetFCS(self):
        return self.fcs

    def Resume(self):
        pass

    def RunIC(self):
        return True

    def Run(self):
        self.sim_time += self.dt
        
        self.properties["simulation/sim-time-sec"] = self.sim_time
        
        return True

    def ProcessMessage(self):
        pass

    def CheckIncrementalHold(self):
        pass

    def Hold(self):
        pass

    def GetPropertyValue(self, property_name):
        return self.properties[property_name]

    def ResetToInitialConditions(self, mode):
        pass
    
    def PrintSimulationConfiguration(self):
        pass

class MockFDMModel(object):
    def __init__(self):
        self.properties = {"fcs/aileron-cmd-norm": 0.5555,
                           "fcs/elevator-cmd-norm": 0.6666,
                           "fcs/rudder-cmd-norm": 0x1111,
                           "propulsion/engine/engine-rpm": 2011.0,
                           "propulsion/engine/thrust-lbs": 750.0,
                           "propulsion/engine/power-hp": 27.0,
                           "fcs/throttle-cmd-norm": 0.76,
                           "position/lat-gc-deg": 23.34567,
                           "position/long-gc-deg": 45.65433,
                           "velocities/vtrue-kts": 65.3,
                           "position/h-sl-ft": 1200.35,
                           "attitude/heading-true-rad": 125.43,
                           "accelerations/a-pilot-x-ft_sec2": 12.34,
                           "accelerations/a-pilot-y-ft_sec2": 13.34,
                           "accelerations/a-pilot-z-ft_sec2": 14.34,
                           "velocities/p-rad_sec": 1.234,
                           "velocities/q-rad_sec": 2.234,
                           "velocities/r-rad_sec": 3.234,
                           "atmosphere/T-R": 12345.0,
                           "atmosphere/P-psf": 456.543,
                           "aero/qbar-psf": 12.88,
                           "attitude/roll-rad": 1.456,
                           "attitude/pitch-rad": 2.567,
                           "simulation/dt": 0.01,
                           "simulation/sim-time-sec": 100.2}
    
    def get_property_value(self, property_name):
        return self.properties[property_name]
    
    def set_property_value(self, property_name, value):
        pass
    
    def resume(self):
        pass

    def pause(self):
        pass

    def reset(self):
        pass

    def run(self):
        pass
    
class MockRequest(object):
    def __init__(self):
        self.args = {}

class MockSimulatorDataDatagram(object):
    def __init__(self):
        self.simulation_time = 10.234
        self.latitude = 35.00000
        self.longitude = 24.00000
        self.altitude = 1000.0
        self.airspeed = 40.0
        self.heading = 160.0
        self.x_acceleration = 0.2
        self.y_acceleration = 0.1
        self.z_acceleration = 9.0
        self.roll_rate = 0.5
        self.pitch_rate = 1.0
        self.yaw_rate = 0.3
        self.temperature = 200.0
        self.static_pressure = 90000.0
        self.total_pressure = 91000.0
        self.roll = 12.0
        self.pitch = 15.0
        self.thrust = 600.0
        self.aileron = 0.6
        self.elevator = 0.7
        self.rudder = 0.8
        self.throttle = 0.9
        self.fdm_x_acceleration = 0.33
        self.fdm_y_acceleration = 0.22
        self.fdm_z_acceleration = 10.5
        self.p_dot = 0.123
        self.q_dot = 0.345
        self.r_dot = 0.678
        self.u_dot = 0.111
        self.v_dot = 0.222
        self.w_dot = 0.333
        self.gravity = 9.9999
        self.u = 1.1
        self.v = 2.2
        self.w = 3.3
        self.p = 11.1
        self.q = 22.2
        self.r = 33.3
        self.true_airspeed = 67.4
        self.calibrated_airspeed = 66.9
        self.climb_rate = 1.9
        self.equivalent_airspeed = 69.9
        self.ground_speed = 87.4

        self.fdm_latitude = 34.67
        self.fdm_longitude = 24.33
        self.fdm_altitude = 123.123
        self.fdm_heading = 55.55

        self.phi = 99.11
        self.theta = 11.99
        self.psi = 19.19

    def create_datagram(self):
        simulator_data = fdm_pb2.SimulatorData()
        
        simulator_data.time = self.simulation_time
        simulator_data.gps.latitude = self.latitude
        simulator_data.gps.longitude = self.longitude
        simulator_data.gps.altitude = self.altitude
        simulator_data.gps.airspeed = self.airspeed
        simulator_data.gps.heading = self.heading
        simulator_data.accelerometer.x = self.x_acceleration
        simulator_data.accelerometer.y = self.y_acceleration
        simulator_data.accelerometer.z = self.z_acceleration
        simulator_data.gyroscope.roll_rate = self.roll_rate
        simulator_data.gyroscope.pitch_rate = self.pitch_rate
        simulator_data.gyroscope.yaw_rate = self.yaw_rate
        simulator_data.thermometer.temperature = self.temperature
        simulator_data.pressure_sensor.pressure = self.static_pressure
        simulator_data.pitot_tube.pressure = self.total_pressure
        simulator_data.ins.roll = self.roll
        simulator_data.ins.pitch = self.pitch
        simulator_data.ins.latitude = self.latitude
        simulator_data.ins.longitude = self.longitude
        simulator_data.ins.altitude = self.altitude
        simulator_data.ins.airspeed = self.airspeed
        simulator_data.ins.heading = self.heading
        simulator_data.engine.thrust = self.thrust
        simulator_data.engine.throttle = self.throttle
        simulator_data.controls.aileron = self.aileron
        simulator_data.controls.elevator = self.elevator
        simulator_data.controls.rudder = self.rudder
        simulator_data.controls.throttle = self.throttle
        simulator_data.accelerations.x = self.fdm_x_acceleration
        simulator_data.accelerations.y = self.fdm_y_acceleration
        simulator_data.accelerations.z = self.fdm_z_acceleration
        simulator_data.accelerations.p_dot = self.p_dot
        simulator_data.accelerations.q_dot = self.q_dot
        simulator_data.accelerations.r_dot = self.r_dot
        simulator_data.accelerations.u_dot = self.u_dot
        simulator_data.accelerations.v_dot = self.v_dot
        simulator_data.accelerations.w_dot = self.w_dot
        simulator_data.accelerations.gravity = self.gravity

        simulator_data.velocities.p = self.p
        simulator_data.velocities.q = self.q
        simulator_data.velocities.r = self.r
        simulator_data.velocities.u = self.u
        simulator_data.velocities.v = self.v
        simulator_data.velocities.w = self.w
        simulator_data.velocities.true_airspeed = self.true_airspeed
        simulator_data.velocities.calibrated_airspeed = self.calibrated_airspeed
        simulator_data.velocities.equivalent_airspeed = self.equivalent_airspeed
        simulator_data.velocities.ground_speed = self.ground_speed
        simulator_data.velocities.climb_rate = self.climb_rate

        simulator_data.position.latitude = self.fdm_latitude
        simulator_data.position.longitude = self.fdm_longitude
        simulator_data.position.altitude = self.fdm_altitude
        simulator_data.position.heading = self.fdm_heading

        simulator_data.orientation.phi = self.phi
        simulator_data.orientation.theta = self.theta
        simulator_data.orientation.psi = self.psi

        return simulator_data.SerializeToString()

class MockSimulatorDataListener(SimulatorDataListener):
    def __init__(self):
        SimulatorDataListener.__init__(self)

    def fdm_data_received(self, fdm_data):
        pass

from huginn.sensors import (GPS, Accelerometer, Gyroscope, 
                            Thermometer, PressureSensor, PitotTube,
                            AttitudeIndicator)

class Aircraft(object):
    def __init__(self, fdmexec):
        self.fdmexec = fdmexec
        self.gps = GPS(fdmexec)
        self.accelerometer = Accelerometer(fdmexec)
        self.gyroscope = Gyroscope(fdmexec)
        self.thermometer = Thermometer(fdmexec)
        self.pressure_sensor = PressureSensor(fdmexec)
        self.pitot_tube = PitotTube(fdmexec)
        self.attitude_indicator = AttitudeIndicator(fdmexec)
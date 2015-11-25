"""
The huginn.simulator module contains classes that are used to run an aircraft
simulation
"""

import logging

from huginn import configuration

class Simulator(object):
    def __init__(self, aircraft):
        self.aircraft = aircraft
        self.fdmexec = aircraft.fdmexec
        self.sensors_port = configuration.SENSORS_PORT
        self.controls_port = configuration.CONTROLS_PORT
        self.fdm_client_address = configuration.FDM_CLIENT_ADDRESS
        self.fdm_client_port = configuration.FDM_CLIENT_PORT
        self.fdm_client_dt = configuration.FDM_CLIENT_DT

        self.paused = True

    @property
    def dt(self):
        return self.fdmexec.GetDeltaT()

    @property
    def simulation_time(self):
        return self.fdmexec.GetSimTime()

    def _update_aircraft(self):
        #running = self.fdm_model.run()
        if not self.paused:
            running = self.aircraft.run()

            if not running:
                logging.error("Failed to update the flight dynamics model")

    def set_initial_conditions(self, latitude, longitude, altitude, airspeed, heading):
        """Set the initial aircraft conditions"""
        ic = self.fdmexec.GetIC()

        #ic.SetVtrueKtsIC(airspeed)
        ic.SetVcalibratedKtsIC(airspeed)
        ic.SetLatitudeDegIC(latitude)
        ic.SetLongitudeDegIC(longitude)
        ic.SetAltitudeASLFtIC(altitude)
        ic.SetPsiDegIC(heading)

        logging.debug("Initial conditions: latitude=%f, longitude=%f, altitude=%f, airspeed=%f, heading=%f",
                      latitude,
                      longitude,
                      altitude,
                      airspeed,
                      heading)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def reset(self):
        return self.aircraft.reset()

    def run(self):
        if not self.paused:
            running = self.aircraft.run()

            return running

        return True
 
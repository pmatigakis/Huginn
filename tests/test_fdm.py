import math
from unittest import TestCase, main

from huginn.fdm import (FDMBuilder, Accelerations, FDM, Velocities, Position,
                        Orientation, Atmosphere, Forces, InitialCondition)

from huginn import configuration
from huginn.unit_conversions import (convert_jsbsim_acceleration,
                                     convert_jsbsim_velocity,
                                     convert_jsbsim_pressure,
                                     convert_jsbsim_temperature,
                                     convert_jsbsim_density,
                                     convert_jsbsim_force,
                                     convert_jsbsim_angular_acceleration,
                                     convert_jsbsim_angular_velocity,
                                     ur)

class TestCreateFDMExec(TestCase):
    def test_create_fdmexec(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()

        self.assertIsNotNone(fdm)

        self.assertEqual(fdm.GetSimTime(), 0.0)
        self.assertEqual(fdm.GetDeltaT(), configuration.DT)
        self.assertAlmostEqual(fdm.GetIC().GetLatitudeDegIC(), configuration.LATITUDE, 3)
        self.assertAlmostEqual(fdm.GetIC().GetLongitudeDegIC(), configuration.LONGITUDE, 3)
        self.assertAlmostEqual(fdm.GetIC().GetPsiDegIC(), configuration.HEADING, 3)

        altitude = configuration.ALTITUDE * ur.meter
        altitude.ito(ur.foot)

        altitude_in_feet = altitude.magnitude

        self.assertAlmostEqual(fdm.GetIC().GetAltitudeASLFtIC(), altitude_in_feet, 3)

        airspeed = configuration.AIRSPEED * ur.meters_per_second
        airspeed.ito(ur.knot)

        airspeed_in_knots = airspeed.magnitude
        
        self.assertAlmostEqual(fdm.GetIC().GetVtrueKtsIC(), airspeed_in_knots, 3)

class AccelerationsTests(TestCase):
    def test_accelerations(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        accelerations = Accelerations(fdmexec)

        x_acceleration = fdmexec.GetAuxiliary().GetPilotAccel(1)
        expected_x_acceleration = convert_jsbsim_acceleration(x_acceleration)
        self.assertAlmostEqual(accelerations.x, expected_x_acceleration, 3)

        y_acceleration = fdmexec.GetAuxiliary().GetPilotAccel(2)
        expected_y_acceleration = convert_jsbsim_acceleration(y_acceleration)
        self.assertAlmostEqual(accelerations.y, expected_y_acceleration, 3)

        z_acceleration = fdmexec.GetAuxiliary().GetPilotAccel(3)
        expected_z_acceleration = convert_jsbsim_acceleration(z_acceleration)
        self.assertAlmostEqual(accelerations.z, expected_z_acceleration, 3)

        p_dot = fdmexec.GetAccelerations().GetPQRdot(1)
        expected_p_dot = convert_jsbsim_angular_acceleration(p_dot)
        self.assertAlmostEqual(accelerations.p_dot, expected_p_dot, 3)

        q_dot = fdmexec.GetAccelerations().GetPQRdot(2)
        expected_q_dot = convert_jsbsim_angular_acceleration(q_dot)
        self.assertAlmostEqual(accelerations.q_dot, expected_q_dot, 3)

        r_dot = fdmexec.GetAccelerations().GetPQRdot(3)
        expected_r_dot = convert_jsbsim_angular_acceleration(r_dot)
        self.assertAlmostEqual(accelerations.r_dot, expected_r_dot, 3)

        u_dot = fdmexec.GetAccelerations().GetUVWdot(1)
        expected_u_dot = convert_jsbsim_acceleration(u_dot)
        self.assertAlmostEqual(accelerations.u_dot, expected_u_dot, 3)

        v_dot = fdmexec.GetAccelerations().GetUVWdot(2)
        expected_v_dot = convert_jsbsim_acceleration(v_dot)
        self.assertAlmostEqual(accelerations.v_dot, expected_v_dot, 3)

        w_dot = fdmexec.GetAccelerations().GetUVWdot(3)
        expected_w_dot = convert_jsbsim_acceleration(w_dot)
        self.assertAlmostEqual(accelerations.w_dot, expected_w_dot, 3)

        gravity_acceleration = fdmexec.GetAccelerations().GetGravAccelMagnitude()
        expected_gravity_acceleration = convert_jsbsim_acceleration(gravity_acceleration)
        self.assertAlmostEqual(accelerations.gravity, expected_gravity_acceleration, 3)


class VelocitiesTests(TestCase):
    def test_accelerations(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        velocities = Velocities(fdmexec)

        velocity = fdmexec.GetPropagate().GetPQR(1)
        expected_velocity = convert_jsbsim_angular_velocity(velocity)
        self.assertAlmostEqual(velocities.p, expected_velocity, 3)

        velocity = fdmexec.GetPropagate().GetPQR(2)
        expected_velocity = convert_jsbsim_angular_velocity(velocity)
        self.assertAlmostEqual(velocities.q, expected_velocity, 3)

        velocity = fdmexec.GetPropagate().GetPQR(3)
        expected_velocity = convert_jsbsim_angular_velocity(velocity)
        self.assertAlmostEqual(velocities.r, expected_velocity, 3)

        airspeed = fdmexec.GetAuxiliary().GetVtrueFPS()
        expected_airspeed =  convert_jsbsim_velocity(airspeed)
        self.assertAlmostEqual(velocities.true_airspeed, expected_airspeed, 3)

        climb_rate = -fdmexec.GetPropagate().GetVel(3)
        expected_climb_rate = convert_jsbsim_velocity(climb_rate)
        self.assertAlmostEqual(velocities.climb_rate, expected_climb_rate, 3)

        velocity = fdmexec.GetPropagate().GetUVW(1)
        expected_velocity = convert_jsbsim_velocity(velocity)
        self.assertAlmostEqual(velocities.u, expected_velocity, 3)

        velocity = fdmexec.GetPropagate().GetUVW(2)
        expected_velocity = convert_jsbsim_velocity(velocity)
        self.assertAlmostEqual(velocities.v, expected_velocity, 3)

        velocity = fdmexec.GetPropagate().GetUVW(3)
        expected_velocity = convert_jsbsim_velocity(velocity)
        self.assertAlmostEqual(velocities.w, expected_velocity, 3)

        airspeed = fdmexec.GetAuxiliary().GetVcalibratedFPS()
        expected_airspeed = convert_jsbsim_velocity(airspeed)
        self.assertAlmostEqual(velocities.calibrated_airspeed, expected_airspeed, 3)

        airspeed = fdmexec.GetAuxiliary().GetVequivalentFPS()
        expected_airspeed = convert_jsbsim_velocity(airspeed)
        self.assertAlmostEqual(velocities.equivalent_airspeed, expected_airspeed, 3)

class PositionTests(TestCase):
    def test_aircraft_position(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        position = Position(fdmexec)

        self.assertAlmostEqual(position.latitude, fdmexec.GetPropagate().GetLatitudeDeg(), 3)
        self.assertAlmostEqual(position.longitude, fdmexec.GetPropagate().GetLongitudeDeg(), 3)
        self.assertAlmostEqual(position.altitude, fdmexec.GetPropagate().GetAltitudeASLmeters(), 3)
        self.assertAlmostEqual(position.heading, math.degrees(fdmexec.GetPropagate().GetEuler(3)), 3)

class OrientationTests(TestCase):
    def test_aircraft_orientation(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        orientation = Orientation(fdmexec)

        self.assertAlmostEqual(orientation.phi, fdmexec.GetPropagate().GetEulerDeg(1), 3)
        self.assertAlmostEqual(orientation.theta, fdmexec.GetPropagate().GetEulerDeg(2), 3)
        self.assertAlmostEqual(orientation.psi, fdmexec.GetPropagate().GetEulerDeg(3), 3)

class AtmosphereTests(TestCase):
    def test_get_atmospheric_data(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        atmosphere = Atmosphere(fdmexec)

        self.assertAlmostEqual(atmosphere.pressure,
                               convert_jsbsim_pressure(fdmexec.GetAtmosphere().GetPressure()),
                               3)

        self.assertAlmostEqual(atmosphere.sea_level_pressure,
                               convert_jsbsim_pressure(fdmexec.GetAtmosphere().GetPressureSL()),
                               3)

        self.assertAlmostEqual(atmosphere.temperature,
                               convert_jsbsim_temperature(fdmexec.GetAtmosphere().GetTemperature()),
                               3)

        self.assertAlmostEqual(atmosphere.sea_level_temperature,
                               convert_jsbsim_temperature(fdmexec.GetAtmosphere().GetTemperatureSL()),
                               3)

        self.assertAlmostEqual(atmosphere.density,
                               convert_jsbsim_density(fdmexec.GetAtmosphere().GetDensity()),
                               3)

        self.assertAlmostEqual(atmosphere.sea_level_density,
                               convert_jsbsim_density(fdmexec.GetAtmosphere().GetDensitySL()),
                               3)

class ForcesTests(TestCase):
    def test_get_forces(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        forces = Forces(fdmexec)

        self.assertAlmostEqual(forces.x_body,
                               convert_jsbsim_force(fdmexec.GetAerodynamics().GetForces(1)),
                               3)

        self.assertAlmostEqual(forces.y_body,
                               convert_jsbsim_force(fdmexec.GetAerodynamics().GetForces(2)),
                               3)

        self.assertAlmostEqual(forces.z_body,
                               convert_jsbsim_force(fdmexec.GetAerodynamics().GetForces(3)),
                               3)

        self.assertAlmostEqual(forces.x_wind,
                               convert_jsbsim_force(fdmexec.GetAerodynamics().GetvFw(1)),
                               3)

        self.assertAlmostEqual(forces.y_wind,
                               convert_jsbsim_force(fdmexec.GetAerodynamics().GetvFw(2)),
                               3)

        self.assertAlmostEqual(forces.z_wind,
                               convert_jsbsim_force(fdmexec.GetAerodynamics().GetvFw(3)),
                               3)

        self.assertAlmostEqual(forces.x_total,
                               convert_jsbsim_force(fdmexec.GetAccelerations().GetForces(1)),
                               3)

        self.assertAlmostEqual(forces.y_total,
                               convert_jsbsim_force(fdmexec.GetAccelerations().GetForces(2)),
                               3)

        self.assertAlmostEqual(forces.z_total,
                               convert_jsbsim_force(fdmexec.GetAccelerations().GetForces(3)),
                               3)

class InitialConditionTests(TestCase):
    def test_get_initial_condition(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        ic = InitialCondition(fdmexec)

        self.assertAlmostEqual(ic.latitude, configuration.LATITUDE, 3)
        self.assertAlmostEqual(ic.longitude, configuration.LONGITUDE, 3)
        self.assertAlmostEqual(ic.altitude, configuration.ALTITUDE, 3)
        self.assertAlmostEqual(ic.airspeed, configuration.AIRSPEED, 3)
        self.assertAlmostEqual(ic.heading, configuration.HEADING, 3)

    def test_set_initial_condition(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        ic = InitialCondition(fdmexec)

        ic.latitude = 10.0
        ic.longitude = 20.0
        ic.airspeed = 150.0
        ic.heading = 90.0
        ic.altitude = 500.0

        self.assertAlmostEqual(ic.latitude, 10.0, 3)
        self.assertAlmostEqual(ic.longitude, 20.0, 3)
        self.assertAlmostEqual(ic.altitude, 500.0, 3)
        self.assertAlmostEqual(ic.airspeed, 150.0, 3)
        self.assertAlmostEqual(ic.heading, 90.0, 3)

if __name__ == "__main__":
    main()

import math
from unittest import TestCase

from huginn.fdm import (FDMBuilder, Accelerations, FDM, Velocities, Position,
                        Orientation, Atmosphere, Forces, InitialCondition)

from huginn import configuration
from huginn.unit_conversions import (convert_jsbsim_acceleration,
                                     convert_jsbsim_velocity,
                                     convert_jsbsim_pressure,
                                     convert_jsbsim_temperature,
                                     convert_jsbsim_density,
                                     convert_jsbsim_force)

#here are defined the accelerations when the JSBSim model is at the initial
#conditions
ic_x_acceleration = -2.1684955116282985
ic_y_acceleration = 0.13504071310147797
ic_z_acceleration = -19.273096239317525

ic_p = 0.0 #math.degrees(0.020975)
ic_q = 0.0 #math.degrees(-0.056170)
ic_r = 0.0 #math.degrees(0.019293)
ic_u = 30.0 #convert_jsbsim_acceleration(90.448965)
ic_v = 0.0 #convert_jsbsim_acceleration(-0.391714)
ic_w = 0.0 #convert_jsbsim_acceleration(-2.337495)
ic_calibrated_airspeed = convert_jsbsim_velocity(97.016659)
ic_equivalent_airspeed = convert_jsbsim_velocity(97.013340)

ic_vtrue = 30.0 #convert_jsbsim_velocity(90.478887)
ic_climb_rate = 0.0 #convert_jsbsim_velocity(-1.871979)

ic_p_dot = 0.0007954234992649408
ic_q_dot = -58.697486202139515
ic_r_dot = 22.765392500429837

ic_u_dot = -2.461306940365588
ic_v_dot = 0.025224422806454053
ic_w_dot = -10.218232433766243

ic_gravity_acceleration = convert_jsbsim_acceleration(32.136667)

class TestCreateFDMExec(TestCase):
    def test_create_fdmexec(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm = fdm_builder.create_fdm()

        self.assertIsNotNone(fdm)

class AccelerationsTests(TestCase):
    def test_accelerations(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        accelerations = Accelerations(fdmexec)

        self.assertAlmostEqual(accelerations.x, ic_x_acceleration, 3)
        self.assertAlmostEqual(accelerations.y, ic_y_acceleration, 3)
        self.assertAlmostEqual(accelerations.z, ic_z_acceleration, 3)
        self.assertAlmostEqual(accelerations.p_dot, ic_p_dot, 3)
        self.assertAlmostEqual(accelerations.q_dot, ic_q_dot, 3)
        self.assertAlmostEqual(accelerations.r_dot, ic_r_dot, 3)
        self.assertAlmostEqual(accelerations.u_dot, ic_u_dot, 3)
        self.assertAlmostEqual(accelerations.v_dot, ic_v_dot, 3)
        self.assertAlmostEqual(accelerations.w_dot, ic_w_dot, 3)
        self.assertAlmostEqual(accelerations.gravity, ic_gravity_acceleration, 3)

class FDMTests(TestCase):
    def setUp(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        self.fdmexec = fdm_builder.create_fdm()
    
    def test_fdm_accelerations(self):
        fdm = FDM(self.fdmexec)

        self.assertAlmostEqual(fdm.accelerations.x, ic_x_acceleration, 3)
        self.assertAlmostEqual(fdm.accelerations.y, ic_y_acceleration, 3)
        self.assertAlmostEqual(fdm.accelerations.z, ic_z_acceleration, 3)

    def test_velocities(self):
        fdm = FDM(self.fdmexec)

        self.assertAlmostEqual(fdm.velocities.p, ic_p, 3)
        self.assertAlmostEqual(fdm.velocities.q, ic_q, 3)
        self.assertAlmostEqual(fdm.velocities.r, ic_r, 3)
        self.assertAlmostEqual(fdm.velocities.u, ic_u, 3)
        self.assertAlmostEqual(fdm.velocities.v, ic_v, 3)
        self.assertAlmostEqual(fdm.velocities.w, ic_w, 3)
        self.assertAlmostEqual(fdm.velocities.climb_rate, ic_climb_rate, 3)
        self.assertAlmostEqual(fdm.velocities.true_airspeed, ic_vtrue, 3)
        self.assertAlmostEqual(fdm.velocities.calibrated_airspeed, ic_calibrated_airspeed, 3)
        self.assertAlmostEqual(fdm.velocities.equivalent_airspeed, ic_equivalent_airspeed, 3)

class VelocitiesTests(TestCase):
    def test_accelerations(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        velocities = Velocities(fdmexec)

        self.assertAlmostEqual(velocities.p, ic_p, 3)
        self.assertAlmostEqual(velocities.q, ic_q, 3)
        self.assertAlmostEqual(velocities.r, ic_r, 3)
        self.assertAlmostEqual(velocities.true_airspeed, ic_vtrue, 3)
        self.assertAlmostEqual(velocities.climb_rate, ic_climb_rate, 3)
        self.assertAlmostEqual(velocities.u, ic_u, 3)
        self.assertAlmostEqual(velocities.v, ic_v, 3)
        self.assertAlmostEqual(velocities.w, ic_w, 3)
        self.assertAlmostEqual(velocities.calibrated_airspeed, ic_calibrated_airspeed, 3)
        self.assertAlmostEqual(velocities.equivalent_airspeed, ic_equivalent_airspeed, 3)

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

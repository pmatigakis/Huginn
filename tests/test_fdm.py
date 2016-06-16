import math
from unittest import TestCase

from huginn.fdm import (FDMBuilder, Accelerations, FDM, Velocities, Position,
                        Orientation, Atmosphere, Forces)

from huginn import configuration
from huginn.unit_conversions import (convert_feet_to_meters,
                                     convert_psf_to_pascal,
                                     convert_rankine_to_kelvin,
                                     convert_slug_sqr_feet_to_kg_sqr_meters,
                                     convert_pounds_to_newtons)

#here are defined the accelerations when the JSBSim model is at the initial
#conditions
ic_x_acceleration = convert_feet_to_meters(-7.829086)
ic_y_acceleration = convert_feet_to_meters(0.985110)
ic_z_acceleration = convert_feet_to_meters(-26.564349)

ic_p = math.degrees(0.020975) 
ic_q = math.degrees(-0.056170)
ic_r = math.degrees(0.019293)
ic_u = convert_feet_to_meters(90.448965)
ic_v = convert_feet_to_meters(-0.391714)
ic_w = convert_feet_to_meters(-2.337495)
ic_calibrated_airspeed = convert_feet_to_meters(89.153633)
ic_equivalent_airspeed = convert_feet_to_meters(89.181657)

ic_vtrue = convert_feet_to_meters(90.478887)
ic_climb_rate = convert_feet_to_meters(-1.871979)

ic_p_dot = math.degrees(0.008016)
ic_q_dot = math.degrees(-0.021258)
ic_r_dot = math.degrees(-0.003549)

ic_u_dot = convert_feet_to_meters(-6.540986)
ic_v_dot = convert_feet_to_meters(-0.114221)
ic_w_dot = convert_feet_to_meters(0.359305)

ic_gravity_acceleration = convert_feet_to_meters(32.136667)

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
                               convert_psf_to_pascal(fdmexec.GetAtmosphere().GetPressure()),
                               3)

        self.assertAlmostEqual(atmosphere.sea_level_pressure,
                               convert_psf_to_pascal(fdmexec.GetAtmosphere().GetPressureSL()),
                               3)

        self.assertAlmostEqual(atmosphere.temperature,
                               convert_rankine_to_kelvin(fdmexec.GetAtmosphere().GetTemperature()),
                               3)

        self.assertAlmostEqual(atmosphere.sea_level_temperature,
                               convert_rankine_to_kelvin(fdmexec.GetAtmosphere().GetTemperatureSL()),
                               3)

        self.assertAlmostEqual(atmosphere.density,
                               convert_slug_sqr_feet_to_kg_sqr_meters(fdmexec.GetAtmosphere().GetDensity()),
                               3)

        self.assertAlmostEqual(atmosphere.sea_level_density,
                               convert_slug_sqr_feet_to_kg_sqr_meters(fdmexec.GetAtmosphere().GetDensitySL()),
                               3)

class ForcesTests(TestCase):
    def test_get_forces(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdmexec = fdm_builder.create_fdm()

        forces = Forces(fdmexec)

        self.assertAlmostEqual(forces.x_body,
                               convert_pounds_to_newtons(fdmexec.GetAerodynamics().GetForces(1)),
                               3)

        self.assertAlmostEqual(forces.y_body,
                               convert_pounds_to_newtons(fdmexec.GetAerodynamics().GetForces(2)),
                               3)

        self.assertAlmostEqual(forces.z_body,
                               convert_pounds_to_newtons(fdmexec.GetAerodynamics().GetForces(3)),
                               3)

        self.assertAlmostEqual(forces.x_wind,
                               convert_pounds_to_newtons(fdmexec.GetAerodynamics().GetvFw(1)),
                               3)

        self.assertAlmostEqual(forces.y_wind,
                               convert_pounds_to_newtons(fdmexec.GetAerodynamics().GetvFw(2)),
                               3)

        self.assertAlmostEqual(forces.z_wind,
                               convert_pounds_to_newtons(fdmexec.GetAerodynamics().GetvFw(3)),
                               3)

        self.assertAlmostEqual(forces.x_total,
                               convert_pounds_to_newtons(fdmexec.GetAccelerations().GetForces(1)),
                               3)

        self.assertAlmostEqual(forces.y_total,
                               convert_pounds_to_newtons(fdmexec.GetAccelerations().GetForces(2)),
                               3)

        self.assertAlmostEqual(forces.z_total,
                               convert_pounds_to_newtons(fdmexec.GetAccelerations().GetForces(3)),
                               3)


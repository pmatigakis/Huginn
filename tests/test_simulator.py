from unittest import TestCase

from huginn.simulator import Simulator, SimulationBuilder
from huginn.fdm import FDMBuilder
from huginn import configuration

class SimulatorBuilderTests(TestCase):
    def test_create_simulation(self):
        huginn_data_path = configuration.get_data_path()

        simulation_builder = SimulationBuilder(huginn_data_path)
        simulation_builder.aircraft = "Rascal"

        simulator = simulation_builder.create_simulator()

        self.assertIsNotNone(simulator)
        self.assertGreaterEqual(simulator.simulation_time, 0.5)

class TestSimulator(TestCase):
    def test_run_with_real_fdmexec(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()

        self.assertIsNotNone(fdmexec)

        simulator = Simulator(fdmexec)

        start_time = simulator.simulation_time

        simulator.resume()
        
        #run_result = aircraft.run()
        simulator.run()

        self.assertAlmostEqual(simulator.simulation_time,
                               start_time + configuration.DT,
                               6)

    def test_run(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
    
        simulator = Simulator(fdmexec)
        
        result = simulator.run()
        
        self.assertTrue(result)

    def test_reset(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        simulator = Simulator(fdmexec)
        simulator.run()
        
        simulator.set_aircraft_controls(0.1, 0.2, 0.3, 0.4)
        self.assertAlmostEqual(simulator.aircraft.controls.aileron, 0.1, 3)
        self.assertAlmostEqual(simulator.aircraft.controls.elevator, 0.2, 3)
        self.assertAlmostEqual(simulator.aircraft.controls.rudder, 0.3, 3)
        self.assertAlmostEqual(simulator.aircraft.controls.throttle, 0.4, 3)

        result = simulator.reset()
        
        self.assertTrue(result)
        self.assertAlmostEqual(simulator.aircraft.controls.aileron, 0.0, 3)
        self.assertAlmostEqual(simulator.aircraft.controls.rudder, 0.0, 3)
        self.assertAlmostEqual(simulator.aircraft.controls.throttle, 0.0, 3)
        self.assertAlmostEqual(simulator.aircraft.controls.elevator, 0.0, 3)

    def test_step(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        simulator = Simulator(fdmexec)
        
        result = simulator.step()

        self.assertTrue(result)

    def test_run_for(self):
        huginn_data_path = configuration.get_data_path()

        fdm_builder = FDMBuilder(huginn_data_path)
        fdm_builder.aircraft = "Rascal"
        fdmexec = fdm_builder.create_fdm()
        
        simulator = Simulator(fdmexec)
        
        time_to_run = 1.0
        
        start_time = simulator.simulation_time
        expected_end_time = start_time + time_to_run
        
        result = simulator.run_for(time_to_run)

        self.assertTrue(result)
        self.assertAlmostEqual(expected_end_time, simulator.simulation_time, 3)

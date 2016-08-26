from unittest import TestCase

from mock import MagicMock

from huginn.control import SimulatorControlClient

class TestSimulatorControlClient(TestCase):
    def test_reset(self):
        simulator_control_client = SimulatorControlClient("127.0.0.1", 12345)

        simulator_control_client._send_command = MagicMock(return_value={"result": "ok"})

        result = simulator_control_client.reset()

        self.assertTrue(result)

        simulator_control_client._send_command.assert_called_once_with("reset")

    def test_pause(self):
        simulator_control_client = SimulatorControlClient("127.0.0.1", 12345)

        simulator_control_client._send_command = MagicMock(return_value={"result": "ok"})

        result = simulator_control_client.pause()

        self.assertTrue(result)

        simulator_control_client._send_command.assert_called_once_with("pause")

    def test_resume(self):
        simulator_control_client = SimulatorControlClient("127.0.0.1", 12345)

        simulator_control_client._send_command = MagicMock(return_value={"result": "ok"})

        result = simulator_control_client.resume()

        self.assertTrue(result)

        simulator_control_client._send_command.assert_called_once_with("resume")

    def test_start_paused(self):
        simulator_control_client = SimulatorControlClient("127.0.0.1", 12345)

        simulator_control_client._send_command = MagicMock(
            return_value={"result": "ok"})

        result = simulator_control_client.start_paused(True)

        self.assertTrue(result)

        simulator_control_client._send_command.assert_called_once_with("start_paused")

    def test_start_running(self):
        simulator_control_client = SimulatorControlClient("127.0.0.1", 12345)

        simulator_control_client._send_command = MagicMock(
            return_value={"result": "ok"})

        result = simulator_control_client.start_paused(False)

        self.assertTrue(result)

        simulator_control_client._send_command.assert_called_once_with("start_running")
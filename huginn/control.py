"""
The huginn.control module contains classes an objects that can be used to
control the state of the simulator (pause, resume etc)
"""


import json

import requests


class SimulatorControlClient(object):
    """The SimulatorControlClient is used to remotely pause, resume and
    reset the simulator."""
    def __init__(self, huginn_host, simulator_control_port):
        self.huginn_host = huginn_host
        self.simulator_controls_port = simulator_control_port

    def _send_command(self, command, data=None):
        """Send an http command to the simulator"""
        command_data = {"command": command}

        if data:
            command_data.update(data)

        headers = {"content-type": "application/json"}

        response = requests.post(
            "http://%s:%d/simulator" % (self.huginn_host,
                                        self.simulator_controls_port),
            data=json.dumps(command_data),
            headers=headers
        )

        response_data = json.loads(response.text)

        return response_data

    def reset(self):
        """Reset the simulator"""
        response_data = self._send_command("reset")

        if response_data["result"] != "ok":
            return False

        return True

    def pause(self):
        """Pause the simulator"""
        response_data = self._send_command("pause")

        if response_data["result"] != "ok":
            return False

        return True

    def resume(self):
        """Resume the simulation"""
        response_data = self._send_command("resume")

        if response_data["result"] != "ok":
            return False

        return True

    def step(self):
        """Run one simulation step"""
        response_data = self._send_command("step")

        if response_data["result"] != "ok":
            return False

        return True

    def run_for(self, time_to_run):
        """Run the simulation for the given time in seconds"""
        response_data = self._send_command("run_for",
                                           data={"time_to_run": time_to_run})

        if response_data["result"] != "ok":
            return False

        return True

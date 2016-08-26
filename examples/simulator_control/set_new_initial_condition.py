from huginn.control import SimulatorControlClient

client = SimulatorControlClient("localhost", 8090)

latitude = 37.9232547
longitude = 23.921773
altitude = 300.0
airspeed = 30.0
heading = 45.0
paused = True

client.set_initial_condition(latitude, longitude, altitude, heading, airspeed)
client.start_paused(paused)

client.reset()

client.resume()

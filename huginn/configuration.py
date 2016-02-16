"""
The huginn.configuration module contains the default configuration values
"""
import pkg_resources

#interface settings
SIMULATOR_CONTROL_PORT = 10500
WEB_SERVER_PORT = 8090
SENSORS_PORT = 10300
CONTROLS_PORT = 10301
FDM_CLIENT_ADDRESS = "127.0.0.1"
FDM_CLIENT_PORT = 10302
FDM_CLIENT_DT = 0.1
TELEMETRY_PORT = 10400
TELEMETRY_DT = 1.0
AIRCRAFT = "Rascal"

#simulation settings
DT = 1.0/160.0

#initial condition
LATITUDE = 37.9232547
LONGITUDE = 23.921773
ALTITUDE = 300.0
AIRSPEED = 30.0
HEADING = 45.0

AVAILABLE_AIRCRAFT = ["Rascal", "easystar"]
DEFAULT_AICRAFT = "Rascal"

LOG_FILE = "huginn.log"

def get_data_path():
    return pkg_resources.resource_filename("huginn", "data")  # @UndefinedVariable

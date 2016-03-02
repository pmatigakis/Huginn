"""
The huginn.serialport module contains classes that are used to transmit fdm
data on the serial port.
"""

import struct

from twisted.internet.protocol import Protocol

from huginn.protocols import FDMDataListener

def calculate_checksum(data):
    """Calculate the 8bit checksum for the given data"""
    checksum = 0

    for i in range(len(data)):
        checksum += ord(data[i])
        checksum += (checksum >> 8)
        checksum = checksum & 0xff

    return checksum

class FrameDataEncoder(object):
    """The FrameDataEncoder is used to convert the given data into a frame
    that can be transmitted over the serial port"""
    def __init__(self):
        self.start_flag = 0x7d
        self.escape_flag = 0x7e
        self.end_flag = 0x7f

    def _escape_data(self, data):
        for i in reversed(range(len(data))):
            if (data[i] == chr(self.start_flag)
                or data[i] == chr(self.escape_flag)
                or data[i] == chr(self.end_flag)):
                data[i] = chr(ord(data[i]) ^ self.escape_flag)
                data.insert(i, chr(self.escape_flag))

    def encode_data(self, data):
        """Create a frame using the given data"""
        data_items = list(data)

        checksum = calculate_checksum(data)
        data_items.append(chr(checksum))

        self._escape_data(data_items)

        encoded_data = ''.join(data_items)

        return chr(self.start_flag) + encoded_data + chr(self.end_flag)

class FrameDataDecoder(object):
    """The FrameDataDecoder is used to extract the data from a frame"""
    def __init__(self):
        self.escape_flag = 0x7e

    def _unescape_data(self, data):
        for i in reversed(range(len(data))):
            if data[i] == chr(self.escape_flag):
                data[i+1] = chr(ord(data[i+1]) ^ self.escape_flag)
                del data[i]

    def decode_frame(self, frame):
        """Extract the data from a frame and calculate the expected checksum
        for those data"""
        frame_items = list(frame)
        frame_items = frame_items[1:-1]

        self._unescape_data(frame_items)

        data = ''.join(frame_items)

        return data[:-1], data[-1]

class FramedDataProtocol(Protocol):
    """The FramedDataProtocol is used to create the data frame that is used
    to communicate with a device listening on the serial port"""
    def __init__(self):
        self._state = self._handle_ready_state
        self._buffer = []
        self._max_buffer_size = 1000
        self._start_flag = 0x7d
        self._escape_flag = 0x7e
        self._end_flag = 0x7f
        self.frame_data = None

        self._decoder = FrameDataDecoder()
        self._decoder.start_flag = self._start_flag
        self._decoder.escape_flag = self._escape_flag
        self._decoder.end_flag = self._end_flag

        self._encoder = FrameDataEncoder()
        self._encoder.start_flag = self._start_flag
        self._encoder.escape_flag = self._escape_flag
        self._encoder.end_flag = self._end_flag

    def dataReceived(self, data):
        for i in range(len(data)):
            self._state(data[i])

    def _handle_ready_state(self, received_byte):
        if received_byte == chr(self._start_flag):
            self._buffer = [received_byte]
            self.frame_data = None
            self._state = self._handle_receiving_state

    def _handle_receiving_state(self, received_byte):
        if received_byte == chr(self._escape_flag):
            self._buffer.append(received_byte)
            self._state = self._handle_receiving_escaped_state
        elif received_byte == chr(self._start_flag):
            self._state = self._handle_ready_state
        elif received_byte == chr(self._end_flag):
            self._buffer.append(received_byte)
            self._validate_frame()
        else:
            self._buffer.append(received_byte)

    def _handle_receiving_escaped_state(self, received_byte):
        if received_byte == chr(self._escape_flag) or received_byte == chr(self._start_flag) or received_byte == chr(self._end_flag):
            self._state = self._handle_ready_state
        else:
            self._buffer.append(received_byte)
            self._state = self._handle_receiving_state

    def _validate_frame(self):
        if len(self._buffer) < 3:
            self.frame_data = None
            self._state = self._handle_ready_state
            return

        received_frame_data = ''.join(self._buffer)

        decoded_frame_data, checksum = self._decoder.decode_frame(received_frame_data)
        if not decoded_frame_data:
            return

        self.frame_data = decoded_frame_data

        expected_checksum = calculate_checksum(self.frame_data)

        if ord(checksum) != expected_checksum:
            self.invalid_frame_received(self.frame_data)
            self.frame_data = None
            return

        self.frame_received(self.frame_data)
        self._state = self._handle_ready_state

    def write_data(self, data):
        encoded_data = self._encoder.encode_data(data)

        self.transport.write(encoded_data)

    def frame_received(self, frame_data):
        pass

    def invalid_frame_received(self, frame_data):
        print("invalid frame: %s" % frame_data)

class AircraftControlsListener(object):
    """The AircraftControlsListener interface must be implemented by any
    object that needs to be notified when the aircraft control data
    have been received"""
    def controls_received(self, aileron, elevator, rudder, throttle):
        pass

class FDMDataFrameProtocol(FramedDataProtocol):
    """The FDMDataFrameProtocol creates the fdm data frame that is used when
    communicating with a device using the serial port"""
    def __init__(self):
        FramedDataProtocol.__init__(self)
        self.controls_listeners = []

    def add_controls_listener(self, listener):
        self.controls_listeners.append(listener)

    def remove_controls_listener(self, listener):
        self.controls_listeners.remove(listener)

    def frame_received(self, frame_data):
        if len(frame_data) != 16:
            return

        control_values = struct.unpack("!ffff", frame_data)

        for listener in self.controls_listeners:
            listener.controls_received(control_values[0], control_values[1], control_values[2], control_values[3])

    def send_fdm_data(self, fdm_data):
        encoded_data = struct.pack("!" + ("f" * len(fdm_data)), *fdm_data)

        self.write_data(encoded_data)

class AutopilotBoardAdapter(FDMDataFrameProtocol, FDMDataListener, AircraftControlsListener):
    """The AutopilotBoardAdapter is used to connect to an autopilot using the
    serial port"""
    def __init__(self, controls_client):
        FDMDataFrameProtocol.__init__(self)

        self.controls_client = controls_client
        self.add_controls_listener(self)

        self.fdm_data = []

    def fdm_data_received(self, fdm_data):
        gps = fdm_data.gps
        accelerometer = fdm_data.accelerometer
        gyroscope = fdm_data.gyroscope
        ins = fdm_data.ins
        controls = fdm_data.controls
        self.fdm_data = [fdm_data.time,
                         gps.latitude,
                         gps.longitude,
                         gps.altitude,
                         gps.airspeed,
                         gps.heading,
                         accelerometer.x_acceleration,
                         accelerometer.y_acceleration,
                         accelerometer.z_acceleration,
                         gyroscope.roll_rate,
                         gyroscope.pitch_rate,
                         gyroscope.yaw_rate,
                         fdm_data.thermometer.temperature,
                         fdm_data.pressure_sensor.pressure,
                         fdm_data.pitot_tube.pressure,
                         ins.roll,
                         ins.pitch,
                         fdm_data.engine.thrust,
                         controls.aileron,
                         controls.elevator,
                         controls.rudder,
                         controls.throttle]
        self.send_fdm_data(self.fdm_data)

    def controls_received(self, aileron, elevator, rudder, throttle):
        self.controls_client.transmit_controls(aileron, elevator, rudder, throttle)

from unittest import TestCase
import struct

from huginn.serialport import FramedDataProtocol, calculate_checksum,\
                              FrameDataEncoder, FrameDataDecoder,\
                              FDMDataFrameProtocol, AircraftControlsListener

from test_common import isclose

from mock.mock import MagicMock

class TestFramedDataProtocol(TestCase):
    def test_data_received(self):
        protocol = FramedDataProtocol()

        checksum = chr(0xaa)
        data = struct.pack("ccccccc", chr(0x7d), chr(0x11), chr(0x22), chr(0x33), chr(0x44), checksum, chr(0x7f))

        protocol.dataReceived(data)

        self.assertEqual(len(protocol.frame_data), 4)

        self.assertEqual(ord(protocol.frame_data[0]), 0x11)
        self.assertEqual(ord(protocol.frame_data[1]), 0x22)
        self.assertEqual(ord(protocol.frame_data[2]), 0x33)
        self.assertEqual(ord(protocol.frame_data[3]), 0x44)

        checksum = chr(0xbb)
        data = struct.pack("ccccc", chr(0x7d), chr(0x55), chr(0x66), checksum, chr(0x7f))

        protocol.dataReceived(data)

        self.assertEqual(len(protocol.frame_data), 2)

        self.assertEqual(ord(protocol.frame_data[0]), 0x55)
        self.assertEqual(ord(protocol.frame_data[1]), 0x66)

class TestChecksumCalculation(TestCase):
    def test_calculate_checksum(self):
        data = struct.pack("cccccc", chr(0x11), chr(0x22), chr(0x33), chr(0x44), chr(0x55), chr(0x66))

        checksum = calculate_checksum(data)

        expected_checksum = 0x66

        self.assertEqual(checksum, expected_checksum)

class TestFrameDataEncoder(TestCase):
    def test_encode_data(self):
        encoder = FrameDataEncoder()
        
        data = [chr(0), chr(1), chr(2), chr(3)]

        encoded_data = encoder.encode_data(data)

        self.assertEqual(len(encoded_data), 7) #this assumes there are no escape flags in the data
        self.assertTrue(ord(encoded_data[0]) == encoder.start_flag)
        self.assertTrue(ord(encoded_data[-1]) == encoder.end_flag)
        
        self.assertEqual(ord(encoded_data[-2]), 6)

    def test_escape_data(self):
        encoder = FrameDataEncoder()

        data = [chr(0x11), chr(0x22), chr(encoder.start_flag)]

        encoder._escape_data(data)

        self.assertEqual(len(data), 4)
        self.assertEqual(data[0], chr(0x11))
        self.assertEqual(data[1], chr(0x22))
        self.assertEqual(data[2], chr(encoder.escape_flag))
        self.assertEqual(data[3], chr(encoder.escape_flag ^ encoder.start_flag))

class TestFrameDataDecoder(TestCase):
    def test_decode_float_data(self):
        decoder = FrameDataDecoder()

        frame = struct.pack("ccccc", chr(0x7d), chr(0x11), chr(0x22), chr(0x33), chr(0x7f))

        data, checksum = decoder.decode_frame(frame)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], chr(0x11))
        self.assertEqual(data[1], chr(0x22))
        
        self.assertEqual(checksum, chr(0x33))

    def test_unescape_data(self):
        decoder = FrameDataDecoder()
        
        data = [chr(0x11), chr(0x22), chr(decoder.escape_flag), chr(decoder.escape_flag ^ decoder.escape_flag)]
        
        decoder._unescape_data(data)
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], chr(0x11))
        self.assertEqual(data[1], chr(0x22))
        self.assertEqual(data[2], chr(decoder.escape_flag))

class TestFrameEncodingAndDecoding(TestCase):
    def test_encode_and_decode_frame(self):
        data = struct.pack("cc", chr(0x11), chr(0x22))

        encoder = FrameDataEncoder()

        frame = encoder.encode_data(data)

        decoder = FrameDataDecoder()
        
        decoded_data, checksum = decoder.decode_frame(frame)

        self.assertEqual(len(decoded_data), 2)
        self.assertEqual(decoded_data[0], chr(0x11))
        self.assertEqual(decoded_data[1], chr(0x22))
        
        self.assertEqual(checksum, chr(0x33))

class ControlValueMatcher(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, value):
        if not isclose(self.value, value, 0.01): return False

        return True

    def __repr__(self):
        return "<ControlValueMatcher value=%f>" % self.value

class TestFDMDataFrameProtocol(TestCase):
    def test_frame_received(self):
        control_data = struct.pack("!ffff", 1.1, 2.2, 3.3, 4.4)

        protocol = FDMDataFrameProtocol()
        
        listener = AircraftControlsListener()
        
        protocol.add_controls_listener(listener)
        
        listener.controls_received = MagicMock()
        
        protocol.frame_received(control_data)
        
        listener.controls_received.assert_called_once_with(ControlValueMatcher(1.1),
                                                           ControlValueMatcher(2.2),
                                                           ControlValueMatcher(3.3),
                                                           ControlValueMatcher(4.4))

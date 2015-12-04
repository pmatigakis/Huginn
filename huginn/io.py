"""
The huginn.io module contains classes and functions that are used by the
simulator in order to perform io operations
"""

from huginn.protocols import TelemetryDataListener

import csv

class CSVTelemetryWriter(TelemetryDataListener):
    """The CSVTelemetryWriter is used to save telemetry data to a file
    in csv format"""
    def __init__(self, output_file):
        TelemetryDataListener.__init__(self)

        self.output_file = output_file
        self.csv_writer = csv.writer(self.output_file, delimiter=",")

    def received_telemetry_header(self, data):
        self.csv_writer.writerow(data)

    def received_telemetry_data(self, data):
        self.csv_writer.writerow(data)

class TelemetryPrinter(TelemetryDataListener):
    """The TelemetryPrinter prints to the console the telemetry data that have
    been received"""
    def __init__(self, variables=None):
        self.variables = variables
        self.data = {}
        self.variable_indexes = {}
        self.inverted_variable_indexes = {}

    def received_telemetry_header(self, data):
        for index, header_variable in enumerate(data):
            self.data[header_variable] = 0.0
            self.variable_indexes[header_variable] = index
            self.inverted_variable_indexes[index] = header_variable

    def print_selected_variables(self, data):
        for variable in self.variables:
            variable_index = self.variable_indexes.get(variable, None)
            if variable_index is not None:
                print("%s: %s" % (variable, data[variable_index]))
            else:
                print("Invalid variable name %s" % variable)

    def print_all_variables(self, data):
        for index, value in enumerate(data):
            variable_name = self.inverted_variable_indexes.get(index, None)
            if variable_name:
                print("%s: %s" % (variable_name, value))

    def received_telemetry_data(self, data):
        if self.variables:
            self.print_selected_variables(data)
        else:
            self.print_all_variables(data)

        print("")

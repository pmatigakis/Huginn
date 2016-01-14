"""
The huginn.io module contains classes and functions that are used by the
simulator in order to perform io operations
"""

import csv

class CSVFDMDataWriter(object):
    """The CSVFDMDataWriter is used to save fdm data to a file
    in csv format"""

    def __init__(self, variables, output_file):
        self.variables = variables
        self.output_file = output_file
        self.csv_writer = csv.writer(self.output_file, delimiter=",")

    def write_header(self):
        """Write the variable names in the csv file"""
        self.csv_writer.writerow(self.variables)

    def write_fdm_data(self, data):
        """Write fdm data to the output file"""
        data_to_write = [data[item] for item in self.variables]

        self.csv_writer.writerow(data_to_write)

class FDMDataPrinter(object):
    """The FDMDataPrinter prints to the console the fdm data that have
    been received"""

    def __init__(self, variables=None):
        self.variables = variables

    def print_fdm_data(self, data):
        """Print the fdm data values to the console"""
        for item in self.variables:
            print("%s: %f" % (item, data[item]))
        print("")

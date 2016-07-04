from huginn.fdm import FDMBuilder
from huginn import configuration

def main():
    huginn_data_path = configuration.get_data_path()

    fdm_builder = FDMBuilder(huginn_data_path)
    fdm_builder.aircraft = "Rascal"
    fdmexec = fdm_builder.create_fdm()

    with open("fdm_properties.txt", "r") as f, open("fdm_property_values.txt", "w") as o:
        for line in f:
            property_name = line.strip()
            property_value = fdmexec.GetPropertyValue(property_name)
            print("%s\t%f" % (property_name, property_value))
            o.write("%s\t%f\n" % (property_name, property_value))

if __name__ == "__main__":
    main()
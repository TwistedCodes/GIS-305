import requests
import yaml
import arcpy
from SpatialETL import SpatialETL


def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    return config_dict


class GSheetsEtl(SpatialETL):
    def __init__(self, remote, local_dir, data_format, destination):
        super().__init__(remote, local_dir, data_format, destination)

    def extract(self):
        print("Extracting addresses from google form spread sheet")

        r = requests.get(
            "https://docs.google.com/spreadsheets/d/1edDbGl8MwKlh101Xl4-_0vEON8YuPnSqRA4_GVn8IAs/edit?usp=sharing")
        r.encoding = "utf-8"
        data = r.text
        with open("C:\Users\Owner\Documents\305 Python\Lab2\Contact Information (Responses) - Form Responses 1.csv",
                  "w") as output_file:
            output_file.write(data)

    def process(self):
        self.extract()
        super().transform()
        super().load()

    def transform(self):
        print(f"Transforming data from GSheet")
        r = requests.get(
            "https://docs.google.com/spreadsheets/d/1edDbGl8MwKlh101Xl4-_0vEON8YuPnSqRA4_GVn8IAs/edit?usp=sharing")
        r.encoding = "utf-8"
        data = r.text
        with open("C:\Users\Owner\Documents\305 Python\Lab2\Contact Information (Responses) - Form Responses 1.csv",
                  "w") as output_file:
            output_file.write(data)

    def process(self):
        self.extract()
        super().transform()
        super().load()

    def load(self):
        print(f"Loading data into arcGIS")
        # Description: Creates a point feature class from inpit table

        # Set enviroment settings
        arcpy.env.workspece = r"C:\Users\Owner\Documents\305 Python\Lab 1A\WestNileOutbreak\WestNileOutbreak.gdb\\"
        arcpy.env.overwriteOutput = True

        # Set local variables
        in_table = r"C:\Users\Owner\Documents\305 Python\Lab2\Contact Information (Responses) - Form Responses 1.csv"
        out_feature_class = "avoid points"
        x_coords = "X"
        y_coords = "Y"

        # Make the XY event layer...
        arcpy.management.XYTableToPoints(in_table, out_feature_class, x_coords, y_coords)

        # print the total rows
        print(arcpy.GetCount_management(out_feature_class))

    def process(self):
        self.extract()
        super().transform()
        super().load()


def etl():
    print("etling....")
    etl_instance = GSheetsEtl(
        "https://docs.google.com/spreadsheets/d/1edDbGl8MwKlh101Xl4-_0vEON8YuPnSqRA4_GVn8IAs/edit?usp=sharing",
        "C:/Users", "GSheets", "C:\Users\Owner\Documents\305 Python\Lab 1A\WestNileOutbreak\WestNileOutbreak.gdb")
    etl.instance.process()


def setup():
    arcpy.env.workspace = r"C:\Users\Owner\Documents\305 Python\Lab 1A\WestNileOutbreak\WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True


def buffer(layer_name, buf_dist):
    # Buffer the incoming layer by the buffer distance
    output_buffer_layer_name = f"{layer_name}_buf"

    print(f'My Buffering {layer_name} to generate a new {output_buffer_layer_name}')

    arcpy.analysis.Buffer(layer_name, output_buffer_layer_name, buf_dist, "FULL", "ROUND", "ALL")


def intersect(layer_name, int_lyrs):
    # Use a breakpoint in the code line below to debug your script.
    print(f'My intersect Method')

    output_intersect_name = "Intersect"
    arcpy.analysis.Intersect(int_lyrs, output_intersect_name)


def spatial_join():
    # Use a breakpoint in the code line below to debug your script.
    print(f'My spatial join Method')
    arcpy.analysis.SpatialJoin("BoulderAddresses", "Intersect", "Areas_of_concern")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup()
    # mosquito larval sites
    # wetlands
    # lakes and reservoirs
    # open space (OSMP)
    buffer_layer_list = ["Mosquito_Larval_Sitess", "LakesandRes_Boulder", "OSMP_properties", "Wetlands_Boulder"]
    for layer in buffer_layer_list:
        print("Looping")
        buffer(layer, "0.1 mile")
    int_lyrs = ["LakesandRes_Boulder_buf", "Mosquito_Larval_Sitess_buf", "OSMP_properties_buf", "Wetlands_Boulder_buf"]
    intersect("Intersect", int_lyrs)

    spatial_join()

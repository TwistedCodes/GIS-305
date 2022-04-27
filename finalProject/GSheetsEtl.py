import csv
import requests
import arcpy
from SpatialEtl import SpatialEtl


class GSheetsEtl(SpatialEtl):
    """
    GSheetsEtl performs and extract, transform and
    load process using a URL to a Google spreadsheet.
    The spread sheet must contain an address and zipcode
    column.
    
    Parameters:
    config_dict (dictionary): A dictionary containg a remote_url key to the Google
    spreadsheet and web geocoding service
    
    """  
    # A dictionary of configuration keys and values
    config_dict = None

    def __init__(self, config_dict):
        super().__init__(config_dict)

    def extract(self):
        """
        Extracting data from a Google spreadsheet
        """
        print("Extracting addresses from google form spreadsheet")
        # file = urllib.request.urlopen(
        # "https://docs.google.com/spreadsheets/d/e/2PACX-1vRt1Ywa2tOQAmbzF8S8DeI7hGz2rHkiygmZl-FugiqRtN_umlvWNmeHYkCxD_y7erOYumgvgJsWUpje/pub?output=csv")

        r = requests.get(
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vRt1Ywa2tOQAmbzF8S8DeI7hGz2rHkiygmZl"
            "-FugiqRtN_umlvWNmeHYkCxD_y7erOYumgvgJsWUpje/pub?output=csv")
        r.encoding = "utf-8"
        data = r.text
        with open(r"C:\Users\Owner\Downloads\addresses.csv", "w") as output_file:
            output_file.write(data)

    def transform(self):
        print("Add City, State")

        transformed_file = open(r"C:\Users\Owner\Downloads\new_addresses.csv", "w")
        transformed_file.write("X,Y,Type\n")
        with open(r"C:\Users\Owner\Downloads\addresses.csv", "r") as partial_file:
            csv_dict = csv.DictReader(partial_file, delimiter=',')
            for row in csv_dict:
                address = row["Street Address"] + " Boulder CO"
                print(address)
                geocode_url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=" + address + "&benchmark=2020&format=json"
                print(geocode_url)
                r = requests.get(geocode_url)

                resp_dict = r.json()
                x = resp_dict['result']['addressMatches'][0]['coordinates']['x']
                y = resp_dict['result']['addressMatches'][0]['coordinates']['y']
                transformed_file.write(f"{x},{y},Residential\n")

        transformed_file.close()

    def load(self):
        # Description: Creates a point feature class from input table

        # Set environment settings
        arcpy.env.workspace = r"C:\Users\Owner\Documents\305 Python\Lab 1A\WestNileOutbreak\WestNileOutbreak.gdb\\"
        arcpy.env.overwriteOutput = True

        # Set the local variables
        in_table = r"C:\Users\Owner\Downloads\new_addresses.csv"
        out_feature_class = "avoid_points"
        x_coords = "X"
        y_coords = "Y"

        # Make the XY event layer...
        arcpy.management.XYTableToPoint(in_table, out_feature_class, x_coords, y_coords)

        # Print the total rows
        print(arcpy.GetCount_management(out_feature_class))

    def process(self):
        self.extract()
        self.transform()
        self.load()

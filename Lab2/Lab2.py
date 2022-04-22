import yaml
import arcpy
from GSheetsEtl import GSheetsEtl


def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)

    arcpy.env.workspace = f"{config_dict['proj_dir']}WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    return config_dict


def etl():
    print("etling....")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()


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


def erase():
    arcpy.analysis.Erase("Intersect", "Avoid_Area", "final_analysis")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()

    # # mosquito larval sites
    # # wetlands
    # # lakes and reservoirs
    # # open space (OSMP)
    # Avoid_Points
    buffer_layer_list = ["Mosquito_Larval_Sitess", "LakesandRes_Boulder", "OSMP_properties", "Wetlands_Boulder"]
    for layer in buffer_layer_list:
        print("Looping")
        buffer(layer, "0.15 mile")
        int_lyrs = ["LakesandRes_Boulder_buf", "Mosquito_Larval_Sitess_buf", "OSMP_properties_buf",
                    "Wetlands_Boulder_buf"]
    intersect("Intersect", int_lyrs)

    spatial_join()

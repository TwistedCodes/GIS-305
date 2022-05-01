import yaml
import arcpy
from GSheetsEtl import GSheetsEtl
import logging

logging.info('Starting West Nile Virus Script')


# srs = arcpy.listSpatialRefernces("*UTM*13N")
#
# for sr_string in srs:
# 	sr_object = arcpy.SpatialReference(sr_string)
# 	print("{0.centralMeridian} {0.name} {0.PCSCode}".format(sr_object))
# aprx = arcpy.mp.ArcGISProject("CURRENT")
# utm_zone_13 = acrpy.SpatialReference(3743)
# map_doc.spatialReference = utm_zone_13

def setup():
    """
    Setting up the workspace and dictionaries from which data will be pulled
    as well as external resources
    :return:
    """
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)

    arcpy.env.workspace = f"{config_dict['proj_dir']}WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    return config_dict




def set_spatial_reference(aprx):
    """
    Set the spatial refernce of the map document
    :param aprx:
    :return:
    """
    try:
        # Set spatial refernce
        map_doc = aprx.listMaps()[0]
        # https://www.spatialreerence.org/ref/esri/3743/ UTM13
        state_plane_noco = arcpy.SpatialReference(3743)
        map_doc.SpatialReference = state_plane_noco
    except Exception as e:
        print(f"Error in set_spatial_reference {e}")

def etl():
    """
    performs and extract, transform and
    load process set up in previous code blocks
    :return:
    """
    try:
        print("etling....")
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()
    except Exception as e:
    print(f"etl failure {e}")

def buffer(layer_name, buf_dist):
    """
    Buffers layers found in West Nile Outbreak Geodata base
    :param layer_name: Mosquito_Larval_Sitess", "LakesandRes_Boulder", "OSMP_properties", "Wetlands_Boulder
    :param buf_dist: 0.15 miles
    :return:
    """
    # Buffer the incoming layer by the buffer distance
    try:
        logging.debug("Starting Buffering")
    output_buffer_layer_name = f"{layer_name}_buf"

    logging.debug(f'My Buffering {layer_name} to generate a new {output_buffer_layer_name}')

    arcpy.analysis.Buffer(layer_name, output_buffer_layer_name, buf_dist, "FULL", "ROUND", "ALL")
    except Exception as B:
    print(f"Buffer not run {B}")

def intersect(layer_name, int_lyrs):
   """
   creates an intersect layer
   :param layer_name:
   :param int_lyrs:
   :return:
   """
# Use a breakpoint in the code line below to debug your script.
try:
    logging.debug("Starting Intersect")

output_intersect_name = "Intersect"
arcpy.analysis.Intersect(int_lyrs, output_intersect_name)
logging.debug("End Intersect Fuction")
except Exception as I:
print(f"Intersect not run {I}")

def spatial_join():
    """
    Joins data from Boulder Addresses, Intersect layer and areas of highest concern
    :return:
    """
    try:
        logging.debug("Starting spatial join")
    # Use a breakpoint in the code line below to debug your script.
    arcpy.analysis.SpatialJoin("BoulderAddresses", "Intersect", "Areas_of_concern")
    logging.debug("My spatial join Method")
    except Exception as S:
    print(f"Spatial join not run {S}")

def erase():
    """
    Creates an area around addresses that opted out of spraying of up to
    0.15 miles. Areas within this  zone do not get sprayed
    :return:
    """
    try:
        logging.debug("Begin erase")
    arcpy.analysis.Erase("Intersect", "Avoid_Area", "final_analysis")
    logging.debug("Erase Complete")
    except Exception as E:
    print(f"Erase not run {E}")


def exportMap():
    """
    Exports the map to a PDF
    :return:
    """
    try:
        aprx = arcpy.mp.ArcGISProject = f({config_dict.get('proj_dir')}, 'WestNileOutbreak.aprx'),
    lyt = aprx.listLayouts()[0]
    for el in lyt.listElements():
        print(el.name)
    if "Title" in el.name:
        el.text = el.text + "Map Export Complete"
    except Exception as M:
    print(f"Map not exported {M}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()
    logging.basicConfig(filename=f"{config_dict('proj_dir')}wnv.log,",
                        filemode="w",
                        level=logging.DEBUG)
    # # mosquito larval sites
    # # wetlands
    # # lakes and reservoirs
    # # open space (OSMP)
    # Avoid_Points
    buffer_layer_list = ["Mosquito_Larval_Sitess", "LakesandRes_Boulder", "OSMP_properties", "Wetlands_Boulder"]
    for layer in buffer_layer_list:
        logging.debug("Looping")
        buffer(layer, "0.15 mile")
        int_lyrs = ["LakesandRes_Boulder_buf", "Mosquito_Larval_Sitess_buf", "OSMP_properties_buf",
                    "Wetlands_Boulder_buf"]
    intersect("Intersect", int_lyrs)

    spatial_join()

    # spatial_join between 'Boulder Addressess' and 'final_analysis'

    # Rendering
    # aprx =arcpy.mp.ArcGISProject("CURRENT")
    # lyr = map_doc.listLayers("LakesandRes_Boulder_buf", "Mosquito_Larval_Sitess_buf", "OSMP_properties_buf",
    #                     "Wetlands_Boulder_buf")[0]
    # Get the existing symbol
    # sym.lry.symbology
    # sym.renderer.symbol.color = {'RGB': [255, 0, 0, 100]}
    # sym.renderer.symbol.outlineColor = {'RGB' :[0, 0, 0, 100]}
    # lyr.symbology = sym
    # lyr.transparency = 50

    # Definition Query
    # lyr = map_doc.listLayers ("LakesandRes_Boulder_buf", "Mosquito_Larval_Sitess_buf", "OSMP_properties_buf",
    #                     "Wetlands_Boulder_buf")[0]
    # lyr.definitionQuery = ""City" = 'Boulder'"

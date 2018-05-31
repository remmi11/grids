# db cruedentials
# database="jcfcqrso"
# user="postgres"
# password="gdipass2018!"
# host="13.82.41.95"
# port="5432"

# pg_dump -h 192.168.1.10 -U postgres -t form bandocat > form.sql

password = "43HmqDx1"
host = "crusty-pisang-mas.db.elephantsql.com"
database = "localyfe"
user = "guest"
port = "5432"

import psycopg2
import os
import time
import arcpy
from arcpy import env

# env.workspace = "/folders"

conn = psycopg2.connect(database=database,
                        user=user,
                        password=password,
                        host=host,
                        port=port)
if conn:
    print "Opened database successfully"
    cur = conn.cursor()

else:
    print "[ ERROR ] Could not connect to database"


def main():
    # check line distance
    #
    print 'check line distance between subs'
    cur.execute("""

                SELECT san_mateo_places.name 

                FROM san_mateo_county, 

                san_mateo_places

                WHERE ST_Intersects(san_mateo_places.geom, san_mateo_county.geom)
                
                LIMIT 4;
                
                """)
    count = 1
    for row in cur.fetchall():

        city = row[0]
        print city
        # create folders for output
        os.makedirs(os.path.join('folders', city))
        # save shp for each city to disk
        # pgsql2shp -f "/path/to/jpnei" -h myserver -u apguser -P apgpassword mygisdb
        # "SELECT neigh_name, the_geom FROM neighborhoods WHERE neigh_name = 'Jamaica Plain'"
        #cmd = """pgsql2shp -f /folders/%s/%s.shp -h %s -u %s -P %s %s "SELECT gid AS id, name, geom FROM places WHERE name = '%s'\"""" % ( city, city, host, user, password, database, city )
        cmd1 = """ogr2ogr -f "ESRI Shapefile" "folders/%s/%s.shp" PG:"host=localhost user=postgres dbname=postgres password=pass" -sql "SELECT gid AS id, name, geom FROM places WHERE name = '%s'\"""" % (
            city, city, city)
        os.system(cmd1)

        # clip san_mateo_lines with each city and store clip results to folder
        #print "Clipping %s Lines" % (city)
        cur.execute("""
        drop table if exists lines_clip_%(int)s;        
        SELECT san_mateo_lines.gid AS id,san_mateo_lines.src, san_mateo_lines.geom 
        INTO lines_clip_%(int)s
        FROM san_mateo_lines, san_mateo_places 
        WHERE ST_Intersects(san_mateo_places.geom, san_mateo_lines.geom) 
        AND san_mateo_places.name = %(str)s;
                
        """, {'int': count, 'str': city})
        conn.commit()

        # fetch the lines and dump shp for each
        cmd2 = """ogr2ogr -f "ESRI Shapefile" "folders/%s/%s_lines.shp" PG:"host=localhost user=postgres dbname=postgres password=pass" -sql "SELECT * FROM lines_clip_%s\"""" % (
            city, city, count)
        #print cmd2
        os.system(cmd2)
        # clipClean(city)
        # chkCRS(city)
        # fishnet(city)

        count += 1


# clip using arcpy store as *_clip_clean
def clipClean():
    env.workspace = "C:/Users/Noah/Desktop/grids/San Mateo County/shapefiles"
    places = 'san_mateo_places.shp'
    lines = 'san_mateo_lines.shp'

    # Make a layer from the feature class
    arcpy.MakeFeatureLayer_management(places, "lyr") 

    fields = ['name', 'SHAPE@XY']

    names = [row[0] for row in arcpy.da.SearchCursor(places, fields)]
    uniqueValues = set(names)

    for name in names:
        print name
        query = """ "name" = '%s'"""%name      
        # Within selected features, further select only those cities which have a population > 10,000   
        arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", query)
        # result = arcpy.GetCount_management("lyr")
        # print result

        clip_features = "lyr"
        in_features = lines
        out_feature_class = "{0}_lines_clip.shp".format(name)
        xy_tolerance = ""
        # Execute Clip
        arcpy.Clip_analysis(in_features, clip_features,
                        out_feature_class, xy_tolerance)





# Resuts: {city}_{file}_utm.shp


def chkCRS(a):

    env.workspace = "C:/Users/Noah/Desktop/grids/scripts/folders/{0}".format(a)
    # Get a list of the feature classes in the input folder
    feature_classes = arcpy.ListFeatureClasses()

    # Loop through the list
    for fc in feature_classes:

        # Determine if the input has a defined coordinate system, can't project it if it does not
        dsc = arcpy.Describe(fc).spatialReference

        # Determine the new output feature class path and name
        outfc = fc[:-4] + "_utm.shp"

        # Set output coordinate system
        #outCS = arcpy.SpatialReference(4283)
        outCS = arcpy.SpatialReference(26910)

        # run project tool
        arcpy.Project_management(fc, outfc, outCS)

        # check messages
        print(arcpy.GetMessages())


# Resuts: {city}_fishnet.shp
def fishnet(a):

    # run fishnet 804.67m (1/2 mi) grids, bounds defined by places polygon
    # project the layers to utm

    env.workspace = "C:/Users/Noah/Desktop/grids/scripts/folders/{0}".format(a)
    # # Get a list of the feature classes in the input folder
    # feature_classes = arcpy.ListFeatureClasses('')
    inFC = '{0}_utm.shp'.format(a)
    desc = arcpy.Describe(inFC)
    outFC = '{0}_fishnet.shp'.format(a)
    arcpy.CreateFishnet_management(outFC, str(desc.extent.lowerLeft), str(desc.extent.XMin) + " " + str(
        desc.extent.YMax + 10), "804.67", "804.67", "", "", str(desc.extent.upperRight), "NO_LABELS", "#", "POLYGON")
    sr = arcpy.SpatialReference("NAD 1983 UTM Zone 10N")
    arcpy.DefineProjection_management(outFC, sr)


def clipFishnet():

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: "fishnet_index", "san_mateo_places"

    arcpy.Clip_analysis(in_features="fishnet_index", clip_features="san_mateo_places",
                        out_feature_class="C:/Users/Noah/Desktop/grids/sample/fishnet_index_clip.shp", cluster_tolerance="")


def createIndex():
    pass


#main()
clipClean()

# deleteFC = "{0}_clip_clean.shp".format(a)
# arcpy.Delete_management(deleteFC)
# deleteFC = "{0}_lines.shp".format(a)
# arcpy.Delete_management(deleteFC)
conn.close()

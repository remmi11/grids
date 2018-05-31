import psycopg2
import os
import time
import arcpy
from arcpy import env

countyname = 'Contra Costa'

myws = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles"
env.workspace = myws
places = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/in_features/" + countyname + "_places.shp"
lines = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/in_features/" + countyname + "_lines.shp"

# Make a layer from the feature class
arcpy.MakeFeatureLayer_management(places, "lyr")
fields = ['name', 'SHAPE@XY']
names = [row[0] for row in arcpy.da.SearchCursor(places, fields)]
uniqueValues = set(names)

# clip using arcpy store as *_clip_clean


def clipClean(name, cln_name, new_directory):

    query = """ "name" = '%s'""" % name
    arcpy.SelectLayerByAttribute_management("lyr", "NEW_SELECTION", query)
    # result = arcpy.GetCount_management("lyr")
    # print result

    clip_features = "lyr"
    inFC = lines
    outFC = "{1}_lines_clip.shp".format(new_directory, cln_name)
    out_filename = os.path.join(new_directory, outFC)
    print out_filename
    xy_tolerance = ""
    # Execute Clip
    arcpy.Clip_analysis(inFC, clip_features, out_filename, xy_tolerance)

    # Write the selected features to a new featureclass
    # Determine the new output feature class path and name
    outname = "{0}.shp" .format(cln_name)
    outfc = os.path.join(new_directory, outname)
    arcpy.CopyFeatures_management("lyr", outfc)
    # Resuts: {city}_{file}_26910.shp


def chkCRS(cln_name, crs):

    env.workspace = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/{0}" .format(
        cln_name)
    # Get a list of the feature classes in the input folder
    feature_classes = arcpy.ListFeatureClasses()

    # Loop through the list
    for fc in feature_classes:

        # Determine if the input has a defined coordinate system, can't project it if it does not
        dsc = arcpy.Describe(fc).spatialReference

        if crs == 4326:
            # Determine the new output feature class path and name
            outfc = fc[:-10] + "_{0}.shp" .format(str(crs))
        else:
            outfc = fc[:-4] + "_{0}.shp" .format(str(crs))

        # Set output coordinate system
        #outCS = arcpy.SpatialReference(4283)
        outCS = arcpy.SpatialReference(crs)

        # run project tool
        arcpy.Project_management(fc, outfc, outCS)

        # check messages
        print(arcpy.GetMessages())


# Resuts: {city}_fishnet.shp
def fishnet(cln_name):

    # run fishnet 804.67m (1/2 mi) grids, bounds defined by places polygon
    # project the layers to utm

    env.workspace = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/{0}" .format(
        cln_name)
    # # Get a list of the feature cln_name in the input folder
    # feature_classes = arcpy.ListFeatureClasses('')
    inFC = '{0}_26910.shp'.format(cln_name)
    desc = arcpy.Describe(inFC)
    outFC = '{0}_fishnet_26910.shp'.format(cln_name)
    arcpy.CreateFishnet_management(outFC, str(desc.extent.lowerLeft), str(desc.extent.XMin) + " " + str(
        desc.extent.YMax + 10), "804.67", "804.67", "", "", str(desc.extent.upperRight), "NO_LABELS", "#", "POLYGON")
    sr = arcpy.SpatialReference("NAD 1983 UTM Zone 10N")
    arcpy.DefineProjection_management(outFC, sr)


def clipFishnet(cln_name):

    env.workspace = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/{0}" .format(
        cln_name)
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: "fishnet_index", "santa_clara_places"

    inFC = "{0}_fishnet_26910_grid.shp".format(cln_name)
    outFC = '{0}_fishnet_clip_26910.shp'.format(cln_name)
    clip_features = '{0}_26910.shp'.format(cln_name)
    xy_tolerance = ""

    arcpy.Clip_analysis(inFC, clip_features, outFC, xy_tolerance)
    # arcpy.Clip_analysis(in_features="fishnet_index", clip_features="santa_clara_places",
    #                     out_feature_class="C:/Users/Noah/Desktop/grids/sample/fishnet_index_clip.shp", cluster_tolerance="")


def gridIndex(cln_name):

    env.workspace = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/{0}" .format(cln_name)
    feature_classes = arcpy.ListFeatureClasses()

    # Set local variables
    outfc = "{0}_fishnet_26910_grid.shp".format(cln_name)
    infc = "{0}_fishnet_26910.shp".format(cln_name)

    desc = arcpy.Describe(infc)
    originCoord = str(desc.extent.lowerLeft)

    intersect_feature = "INTERSECTFEATURE"
    usePageUnit = "NO_USEPAGEUNIT"
    scale = ""
    polygonWidth = "804.67 Meters"
    polygonHeight= "804.67 Meters"
    numberRows = ""
    numberColumns = ""
    startingPageNum = "1"
    labeling = "LABELFROMORIGIN"

    # Execute GridIndexFeatures
    arcpy.GridIndexFeatures_cartography(outfc, infc, intersect_feature, usePageUnit,
                                        scale, polygonWidth, polygonHeight,
                                        originCoord, numberRows, numberColumns,
                                        startingPageNum, labeling)
    
    del outfc
    del infc


def delFeatures(a):
    env.workspace = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/{0}" .format(a)
    feature_classes = arcpy.ListFeatureClasses()

    removeLayer1 = '{0}_lines_clip_26910.shp' .format(a)
    feature_classes.remove(removeLayer1);
    removeLayer2 = '{0}_fishnet_clip_26910.shp' .format(a)
    feature_classes.remove(removeLayer2);

    for feature_class in feature_classes:
        arcpy.Delete_management(feature_class)


def deletefields():
    arcpy.DeleteField_management(fl,"index_no")
    arcpy.DeleteField_management(fl,"index")
    arcpy.DeleteField_management(fl,"city")


def addfields(fl):

    # Execute AddField twice for three new fields
    arcpy.AddField_management(fl, "index_no", "SHORT")
    arcpy.AddField_management(fl, "index", "TEXT", 50)
    arcpy.AddField_management(fl, "city", "TEXT", 50)

  
#loop through and find all instances of 'pagename'
def unique_values(table , field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})


def customIndex(a):
    
    env.workspace = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/{0}" .format(a)
    infc = '{0}_fishnet_clip_26910.shp'.format(a)
    #fl = arcpy.MakeFeatureLayer_management(infc,'flyr')
    #arcpy.MakeFeatureLayer_management(places, "lyr")
    addfields(infc)

    rec = 0
    
    arcpy.CalculateField_management(infc, "city", "'" + a + "'", "PYTHON")
   
    myValues = unique_values(infc, 'pagename')

    #calculate index_no
    for value in myValues:
        query = """"PageName" = '{0}'""" .format(value)
        with arcpy.da.UpdateCursor(infc, 'index_no', query) as cursor:
            for row in cursor:
                rec += 1
                row[0] = str(rec)
                cursor.updateRow(row)
            rec = 0
        del cursor

        with arcpy.da.UpdateCursor(infc, ['index', 'city', 'PageName', 'index_no']) as newcursor:
            for row in newcursor:
                row[0] = 'CA-' + row[1] + '-' + row[2] + '.' + str(row[3])
                newcursor.updateRow(row)
        del newcursor
    

    arcpy.DeleteField_management(infc,"index_no")
    del infc


def covnertKMZ(a):
    
    env.workspace = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/{0}" .format(a)
    
    infc = '{0}_fishnet_clip_4326.shp'.format(a)
    outfc = '{0}_fishnet.kmz'.format(a)
    fl = arcpy.MakeFeatureLayer_management(infc, "fishnet_lyr")
    arcpy.LayerToKML_conversion(fl, outfc)
    del infc
    del outfc
    arcpy.Delete_management(fl)


def deleteUTM(a):
    
    env.workspace = "C:/Users/Noah/Desktop/grids/" + countyname + " County/shapefiles/{0}" .format(a)
    
    del1 = '{0}_fishnet_clip_26910.shp'.format(a)
    del2 = '{0}_lines_clip_26910.shp'.format(a)
    arcpy.Delete_management(del1)
    arcpy.Delete_management(del2)



def main():
    limit = 100
    for _, name in zip(range(limit), names):
        print name
        cln_name = name.replace("-", "_")

        # # RUN THIS FIRST ##
        # new_directory = os.path.join(myws, cln_name)
        # os.mkdir(new_directory)
        # clipClean(name, cln_name, new_directory)
        # chkCRS(cln_name, 26910)
        # fishnet(cln_name)
        # # ADD INDEX BEFORE CLIP
        # gridIndex(cln_name)
        # clipFishnet(cln_name)
        # delFeatures(cln_name)
        try:

            # THEN MANUALLY SPLIT AND EXPLODE BEFORE RUNNING customIndex() FUNCTION ##
            customIndex(cln_name)

            #convert to wgs84
            chkCRS(cln_name,4326)

            #create kmz files
            covnertKMZ(cln_name)

            #delete utm files
            deleteUTM(cln_name)
        except:
            print " "
            print " "
            print " "
            print " "
            print cln_name + " Could Not Be processed!!!"
            print " "
            print " "
            print " "
            print " "

if __name__ == "__main__":
    main()




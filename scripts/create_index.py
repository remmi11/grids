import arcpy

# clip lines by places in sql
# ogr2ogr dump places
# OGR2OGR dump clippped lines
# clip lines in arc
# run fishnet 804.67m (1/2 mi) grids, bounds defined by places polygon

# create grid index

# clip with places poly

# LAYER MUST BE EXPLODED PRIOR RUNNING SCRIPT
fc = '{0}_fishnet_clip_utm.shp'.format(cln_name)
fl = arcpy.MakeFeatureLayer_management(fc,'fl')


def deletefields():
    arcpy.DeleteField_management(fl,"index_no")
    arcpy.DeleteField_management(fl,"index")
    arcpy.DeleteField_management(fl,"city")


def addfields():

    # Execute AddField twice for three new fields
    arcpy.AddField_management(fl, "index_no", "SHORT")
    arcpy.AddField_management(fl, "index", "TEXT", 50)
    arcpy.AddField_management(fl, "city", "TEXT", 50)

  
#loop through and find all instances of 'pagename'
def unique_values(table , field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})


def main():
    rec = 0
    
    arcpy.CalculateField_management(fl, "city", "'" + city + "'", "PYTHON")
   
    myValues = unique_values(fl, 'pagename')

    #calculate index_no
    for value in myValues:
        query = """"PageName" = '{0}'""" .format(value)
        with arcpy.da.UpdateCursor(fl, 'index_no', query) as cursor:
            for row in cursor:
                rec += 1
                row[0] = str(rec)
                cursor.updateRow(row)
            rec = 0
        del cursor

        with arcpy.da.UpdateCursor(fl, ['index', 'city', 'PageName', 'index_no']) as newcursor:
            for row in newcursor:
                row[0] = 'CA-' + row[1] + '-' + row[2] + '.' + str(row[3])
                newcursor.updateRow(row)
        del newcursor

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: "fishnet_index_clip"
    arcpy.DeleteField_management(fc,"index_no")


    # reproject to wgs84 and save to deliverables folder

    # convert to kml

# try:
#     deletefields()
#     addfields()
# except:
#     addfields()

deletefields()
addfields()
main()
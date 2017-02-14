# ---------------------------------------------------------------------------
# ImageCopy.py
# Created on: 2016-12-22 23:38:05
# Created By: Arun Doss
# Usage: For Copying Images falls in an AOI
# Description: Copy Images of a particular AOI from source(like server) to another location using Mosaic Dataset created from the source Images.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
import os
import shutil

# Script arguments
Iteration_Test = arcpy.GetParameterAsText(0)
if Iteration_Test == '#' or not Iteration_Test:
    Iteration_Test = "Iteration Test" # provide a default value if unspecified

Mosaic = arcpy.GetParameterAsText(1)
if Mosaic == '#' or not Mosaic:
    Mosaic = "Mosaic" # provide a default value if unspecified

SrcDir = arcpy.GetParameterAsText(2)

Destination = arcpy.GetParameterAsText(3)

# Local variables:

ScratchGDBName = "Scratch_Workspace"
ScratchGDB = Destination+"\\"+ScratchGDBName+".gdb"
MosaicFootprintName = ScratchGDB + "\\" + "MosaicFootprint"

# Delete existing Scratch

if arcpy.Exists(ScratchGDB):
    arcpy.Delete_management(ScratchGDB)
    
# Process: Create Scratch GDB

arcpy.CreateFileGDB_management(Destination,ScratchGDBName,"CURRENT")

IntersectOutputFeatureClass = Destination+"\\"+ScratchGDBName+".gdb"+"\\ScratchIntersect"

# Create Footprints GDB

arcpy.ExportMosaicDatasetGeometry_management(Mosaic, MosaicFootprintName, "", "FOOTPRINT")

# Process: Intersect
arcpy.Intersect_analysis([MosaicFootprintName,Iteration_Test], IntersectOutputFeatureClass, "ALL","","INPUT")

# Iterate Intersection Result

#def Iterate_Values(Feature, Field):
#    with arcpy.da.SearchCursor(Feature,[Field]) as cursor:
#        return sorted({row[0] for row in cursor})/*

FieldValue = arcpy.SearchCursor(IntersectOutputFeatureClass, fields = "Name")

NameList = []
for value in FieldValue:
    NameList.append(value.getValue("Name"))
    

# Saving Intersection Name

#NameList = Iterate_Values(IntersectOutputFeatureClass, "Name")

print NameList

### Defining Input & Output

FileName = []
for line in NameList:
    FileName.append(line+".tif")
    FileName.append(line+".tif.ovr")
    FileName.append(line+".tif.aux.xml")
    FileName.append(line+".tfw")


FileNameDir = []
for FN in FileName:
    FileNameDir.append(SrcDir+'//'+FN)

for FND in FileNameDir:

    try:
        shutil.copy(FND, Destination)
        print FND
        print "Succeed"
    except:
        print FND
        print "Failed"

# Delete existing Scratch

if arcpy.Exists(ScratchGDB):
    arcpy.Delete_management(ScratchGDB)


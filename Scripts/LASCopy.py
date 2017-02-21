# ---------------------------------------------------------------------------
# LidarCopy.py
# Created on: 2017-02-14 11:21:15
# Created By: Arun Doss
# Usage: For Copying Lidar files which falls in an AOI
# Description: Copy .las files of a particular AOI from source(like server) to another location using Lidar Boundary Polygons created using LasToPolygongs tool
# ---------------------------------------------------------------------------

# Import necessary modules
import arcpy
import os
import shutil

# Scripr Arguments
AOI = arcpy.GetParameterAsText(0)
LidarBoundary = arcpy.GetParameterAsText(1)
SrcDir = arcpy.GetParameterAsText(2)
Destination = arcpy.GetParameterAsText(3)

# Local Variables
ScratchGDBName = "Scratch_Workspace"
ScratchGDB = Destination+"\\"+ScratchGDBName+".gdb"
IntersectOutputFeatureClass = Destination+"\\"+ScratchGDBName+".gdb"+"\\ScratchIntersect"

# Delete existing Sxratch
if arcpy.Exists(ScratchGDB):
    arcpy.Delete_management(ScratchGDB)

# Create Scratch GDB
arcpy.CreateFileGDB_management(Destination,ScratchGDBName,"CURRENT")


#Debug#
# Intersect the AOI and Lidar Boundary
#arcpy.Intersect_analysis([AOI,LidarBoundary], IntersectOutputFeatureClass, "ALL","","INPUT")

#Create spatial Join
arcpy.SpatialJoin_analysis(LidarBoundary,AOI,IntersectOutputFeatureClass,"JOIN_ONE_TO_ONE","KEEP_ALL","","INTERSECT","","")


# Iterate Intersection Result
FieldValue = arcpy.SearchCursor(IntersectOutputFeatureClass, fields = "LasName")

# Save Iteration Name
NameList = []
for value in FieldValue:
    NameList.append(value.getValue("LasName"))
arcpy.AddMessage(NameList)

# Defining Input & Output

FileName = []
for line in NameList:
    FileName.append(line+".las")

FileNameDir = []
for FN in FileName:
    FileNameDir.append(SrcDir+'//'+FN)

for FND in FileNameDir:

    try:
        shutil.copy(FND, Destination)
        arcpy.AddMessage(FND)
        arcpy.AddMessage("Succeed")
    except:
        arcpy.AddMessage(FND)
        arcpy.AddMessage("Failed")

        
#if arcpy.Exists(ScratchGDB):
#    arcpy.Delete_management(ScratchGDB)




# LasToPolygon.py
# To create Boundary Shape file from the .las files
# Using lasboundary.exe at the background
# Compiled by Arun Doss

import sys, os, subprocess, arcpy, shutil

def check_output(command,console):
    if console == True:
        process = subprocess.Popen(command)
    else:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output,error = process.communicate()
    returncode = process.poll()
    return returncode,output

### Including Arguments
Source = arcpy.GetParameterAsText(0)
Destination = arcpy.GetParameterAsText(1)
FileName = arcpy.GetParameterAsText(2)

### Add Starting Message
arcpy.AddMessage("Starting Las To Polygon")

### Getting Path to Las Tools
lastools_path = os.path.dirname(__file__)

### making sure the path does not contain spaces
if lastools_path.count(" ") > 0:
    arcpy.AddMessage("Error. Path to .\\lastools contains spaces.")
    sys.exit(1)

### complete the path to where the LAStools executables are
lastools_path = lastools_path + "\\bin"

### checking if path exists
if os.path.exists(lastools_path) == False:
    arcpy.AddMessage("Cannot find .\\lastools\\bin at " + lastools_path)
    sys.exit(1)
else:
    arcpy.AddMessage("Found " + lastools_path + " ...")

### creating full path to the lasboundary executable
lasboundary_path = lastools_path+"\\lasboundary.exe"

### checking if executable exists
if os.path.exists(lastools_path) == False:
    arcpy.AddMessage("Cannot find lasboundary.exe at " + lasboundary_path)
    sys.exit(1)
else:
    arcpy.AddMessage("Found " + lasboundary_path + " ...")

### Creating List of Las Files in Input Directory
LasList = []

for las in os.listdir(Source):
    if las.endswith(".las"):
        LasList.append(las)
arcpy.AddMessage(LasList)
### Displaying the count of Las Files
LasFileCount = len(LasList)
arcpy.AddMessage(str(LasFileCount) + " .las files found in Source Folder")

### Starting the Process Iteration
arcpy.AddMessage("Creating Single Polygons. The Process may take a while, depends upon the number of files")

### Creating Temp Folder
Output_Temp = os.path.join(Destination, "temp")
if os.path.exists(Output_Temp):
    shutil.rmtree(Output_Temp)
os.makedirs(Output_Temp)
for las in LasList:
    LasFilePath = os.path.join(Source,las)
    ### create the command string for lasboundary.exe
    try:
        command = ['"' + lasboundary_path + '"']

    ### Add Input LiDAR
        command.append("-i")
        command.append('"' + LasFilePath + '"')

    ### Add Output Folder
        command.append("-odir")
        command.append('"' + Output_Temp + '"')

    ### report command string
        arcpy.AddMessage("LAStools command line:")
        command_length = len(command)
        command_string = str(command[0])
        command[0] = command[0].strip('"')
        for i in range(1, command_length):
            command_string = command_string + " " + str(command[i])
            command[i] = command[i].strip('"')
        arcpy.AddMessage(command_string)

    ### running command
        returncode, output = check_output(command, False)

    ### report output of lasboundary
        arcpy.AddMessage(str(output))

    ### check return code
        if returncode != 0:
            arcpy.AddMessage("Error. las to polygon failed for " + las)
            sys.exit(1)

    ### report happy end
        arcpy.AddMessage("Success. las to polygon created for " + las)
    except:
        arcpy.AddMessage("Failure. las to polygon created for " + las)

### Creating Output Polygon Starts here

### Creating ShapeFileList
ShapeList = []

for shp in os.listdir(Output_Temp):
    if shp.endswith(".shp"):
        ShapeList.append(shp)
arcpy.AddMessage(ShapeList)

### Creating Final GDB
arcpy.CreateFileGDB_management(Destination,FileName,"CURRENT")

### Creating Final Feature Class
OutputGDB = os.path.join(Destination,FileName+".gdb")
arcpy.CreateFeatureclass_management(OutputGDB, FileName, 'POLYGON', '#', 'DISABLED', 'DISABLED', "PROJCS['NAD_1983_StatePlane_Florida_East_FIPS_0901_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',656166.6666666665],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-81.0],PARAMETER['Scale_Factor',0.9999411764705882],PARAMETER['Latitude_Of_Origin',24.33333333333333],UNIT['Foot_US',0.3048006096012192]];-17791299.9990048 -41645399.9999997 3906.24999636202;-100000 10000;-100000 10000;2.04800000190735E-03;0.001;0.001;IsHighPrecision", '#', '0', '0', '0')
OutputFC = os.path.join(OutputGDB,FileName)
arcpy.AddField_management(OutputFC, "Name", "TEXT", "", "", 50, "Las Name", "NULLABLE", "NON_REQUIRED", "")
### Adding Name to Field
for shp in ShapeList:
    ShapePath = os.path.join(Output_Temp,shp)
    arcpy.AddField_management(ShapePath, "Name", "TEXT", "", "", 50, "Las Name", "NULLABLE", "NON_REQUIRED", "")
    shpname = shp[:-4]
    arcpy.AddMessage(shpname)
    arcpy.CalculateField_management(ShapePath, "Name", shpname, "PYTHON", "")
    arcpy.Append_management(ShapePath,OutputFC,"","","")



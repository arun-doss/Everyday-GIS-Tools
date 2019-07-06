"""
GeoDevs,
Developed For: Rajeev Saini
------------------------------------------------------------
Creation Date : 16/June/2019
Creator Name : Arun Prasad R
Version No. : 1.0
Major changes
=============
Date Name Change description

"""

import arcpy
import os
import sys

""" folderPath = raw_input("Enter the Folder Path: ").strip()
outputMdbDir = raw_input("Enter the Output .mdb Path: ").strip()
outputMdbName = raw_input("Enter the Required Mdb Name with extension: ").strip() """

folderPath = arcpy.GetParameterAsText(0)
outputMdbDir = arcpy.GetParameterAsText(1)
outputMdbName = arcpy.GetParameterAsText(2)



isDirExists = os.path.isdir(folderPath)
isOutputDirExists = os.path.isdir(outputMdbDir)

def isCharPresent(actual, charString):
    isPresent = False
    for char in charString:
        if(actual.find(char) != -1):
            isPresent = True
    return isPresent

def isMdbPresent(dirName, mdbName):
    isPresent = False
    try:
        outputFolderMdbList = arcpy.ListFiles("*.mdb")
    except:
        # print "Failed.Can't able to reach output mdb folder."
        arcpy.AddError("Failed.Can't able to reach output mdb folder.")
    for outMdb in outputFolderMdbList:
        if(outMdb == outputMdbName):
           isPresent = True
    return isPresent 


if(isDirExists):
    if(isOutputDirExists):

        gdbUnallowedChars = r'\//*?:\'"<>|' # \/*?:'"<>|
        
        if (isCharPresent(outputMdbName, gdbUnallowedChars) == False):

            try:
                arcpy.env.workspace = folderPath
            except:
                # print "Creating Enviroinment Workspace Failed."
                arcpy.AddError("Creating Enviroinment Workspace Failed.")
                sys.exit(1)

            isOutputFileExists =isMdbPresent(outputMdbDir, outputMdbName)
            
            if(isOutputFileExists == False):
                
                try:
                    mdbList = arcpy.ListFiles("*.mdb")
                except:
                    # print "Getting List of .mdb failed."
                    arcpy.AddError("Getting List of .mdb failed.")
                    sys.exit(2)
                if(len(mdbList) > 0):
                    ouputMdbPath = os.path.join(outputMdbDir, outputMdbName)
                    mdbNameShort = os.path.splitext(outputMdbName)[0]
                    try:
                        arcpy.CreatePersonalGDB_management(outputMdbDir, mdbNameShort)
                    except:
                        print "Failed. Can't able to Create Output .mdb"
                        arcpy.AddError("Failed. Can't able to Create Output .mdb")
                        sys.exit(4)
                    try:
                        arcpy.CreateFileGDB_management(outputMdbDir, mdbNameShort + "_Scratch")
                    except:
                        print "Failed.Can't able to Create Scrath .gdb for " + inputMdb
                        arcpy.AddError("Failed.Can't able to Create Scrath .gdb for " + inputMdb)
                        sys.exit(3)
                    
                    for inputMdb in mdbList:
                        outputMdbScratch = os.path.join(outputMdbDir, mdbNameShort + "_Scratch.gdb")
                        fullMdbPath = os.path.join(folderPath, inputMdb)
                        inputMdbShort = os.path.splitext(inputMdb)[0]
                        
                        # Moving the Datasets to the Output Mdb
                        try:
                            arcpy.env.workspace = fullMdbPath
                            try:
                                dataSetsList = arcpy.ListDatasets()
                                for dataSet in dataSetsList:
                                    fullDataSetPath = os.path.join(fullMdbPath, dataSet)
                                    
                                    fullDataSetOutPath = os.path.join(ouputMdbPath, dataSet + "_" + inputMdbShort)
                                    fullDataSetOutPathScratch = os.path.join(outputMdbScratch, dataSet + "_" + inputMdbShort)
                                    try:
                                        arcpy.Copy_management(fullDataSetPath, fullDataSetOutPathScratch)
                                        try:
                                            arcpy.env.workspace = fullDataSetOutPathScratch
                                            try:
                                                scratchFCList = arcpy.ListFeatureClasses()
                                                isAllFCRenamed = True
                                                for scrachFc in scratchFCList:
                                                    fullScratchFCPath = os.path.join(fullDataSetOutPathScratch, scrachFc)
                                                    try:
                                                        arcpy.Rename_management(fullScratchFCPath, fullScratchFCPath + "_" + inputMdbShort)
                                                    except:
                                                        isAllFCRenamed = False
                                                        # print "Warning. Renaming Feature Class " + scrachFc + " in " + dataSet + " of " + inputMdb + " failed."
                                                        arcpy.AddWarning("Warning. Renaming Feature Class " + scrachFc + " in " + dataSet + " of " + inputMdb + " failed.")
                                                if(isAllFCRenamed):
                                                    try:
                                                        arcpy.Copy_management(fullDataSetOutPathScratch, fullDataSetOutPath)
                                                    except:
                                                        # print "Warning. Copying " + dataSet + " of " + inputMdb + " failed."
                                                        arcpy.AddWarning("Warning. Copying " + dataSet + " of " + inputMdb + " failed.")
                                                else:
                                                    # print "Warning. Copying " + dataSet + " of " + inputMdb + " failed."
                                                    arcpy.AddWarning("Warning. Copying " + dataSet + " of " + inputMdb + " failed.")
                                            except:
                                                print "Warning. Getting List of Feature Classes in " + dataSet + " of " + inputMdb + " failed."
                                                arcpy.AddWarning("Warning. Getting List of Feature Classes in " + dataSet + " of " + inputMdb + " failed.")
                                        except:
                                            print "Warning. Changing Workspace to the Scratch dataset location failed for " + dataSet + " of " + inputMdb
                                            arcpy.AddWarning("Warning. Changing Workspace to the Scratch dataset location failed for " + dataSet + " of " + inputMdb)
                                    except:
                                        print "Warning. Copying Feature Dataset to the Scrath GDB for " + inputMdb
                                        arcpy.AddWarning("Warning. Copying Feature Dataset to the Scrath GDB for " + inputMdb)
                                    
                            except:
                                # print "Warning. Listing datasets in " + inputMdb
                                arcpy.AddWarning("Warning. Listing datasets in " + inputMdb)

                            
                        except:
                            # print "Warning. Copying Datsets in " + inputMdb + " Failed"
                            arcpy.AddWarning("Warning. Copying Datsets in " + inputMdb + " Failed")
                        # Moving Feature Classes in root of gdb
                        try:
                            arcpy.env.workspace = fullMdbPath
                            try:
                                fcList = arcpy.ListFeatureClasses()
                                mdbNameShort = os.path.splitext(outputMdbName)[0]
                                for fc in fcList:
                                    fcPath = os.path.join(fullMdbPath, fc)
                                    fcOutPath = os.path.join(ouputMdbPath, fc + "_" + inputMdbShort)
                                    try:
                                        arcpy.Copy_management(fcPath, fcOutPath)
                                    except:
                                        # print "Warning. Copying Feature Class " + fc + " of " + inputMdb + " failed."
                                        arcpy.AddWarning("Warning. Copying Feature Class " + fc + " of " + inputMdb + " failed.")
                            except:
                                # print "Warning. Getting List of Feature Classes in "+ inputMdb + " failed."
                                arcpy.AddWarning("Warning. Getting List of Feature Classes in "+ inputMdb + " failed.")
                            
                        except:
                            # print "Warning. Copying Feature Clasess in " + inputMdb + " Failed"
                            arcpy.AddWarning("Warning. Copying Feature Clasess in " + inputMdb + " Failed")
                        
                else:
                    # print "Failed. No .mdb files found on the given Folder."
                    arcpy.AddError("Failed. No .mdb files found on the given Folder.")
                try:
                    arcpy.Delete_management(outputMdbScratch)
                except:
                    # print "Warning. Deleting Scratch GDB of " + inputMdb + " Failed"
                    arcpy.AddError("Warning. Deleting Scratch GDB of " + inputMdb + " Failed")
            else:
                # print "The given .mdb file already exists."  
                arcpy.AddError("The given .mdb file already exists.")
            
            
        else:
            # print('Failed. Following Characters are not allowed in GDB Name: ' + gdbUnallowedChars )
            arcpy.AddError('Failed. Following Characters are not allowed in GDB Name: ' + gdbUnallowedChars )
        
    else:
        print "Failed. Given Output MDB Folder Doesn't Exist!!"
        arcpy.AddError("Failed. Given Output MDB Folder Doesn't Exist!!")
    
else:
    print "Failed. Given Input Folder Doesn't Exist!!"
    arcpy.AddError("Failed. Given Input Folder Doesn't Exist!!")
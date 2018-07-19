# 
# Created by towshif ali (tali) on 7/18/2018
#
# directory = r"H:\temp\Ebeam_RunLog"

# open database connections


# directory = r"H:\temp\Ebeam_RunLog"

import re
import os
import traceback
import sys
from pprint import pprint
import datetime
from dateutil.parser import parse

# open database connections
from pymongo import mongo_client
from pprint import pprint

client = mongo_client.MongoClient('mongodb://tali-e7440z:27017/')
db = client['result_database']  # or db = client.test_database
collection = db['results-ubuntu']  # or collection = db.posts

import pickle
# from os import walk
from scandir import walk  # use scan dir - its faster (5-10x faster on win64; 3x on Linux, MacOS)


def listFilesWithPattern(directory, extension):  # working version for one type of extension
    files_set = set()
    for (dirpath, dirnames, filenames) in walk(directory):
        for file in filenames:
            if file.endswith(extension):
                full_path = os.path.abspath(os.path.join(dirpath, file))
                files_set.add(full_path)
    return files_set


def listFilesWithPattern2(directory, extension):  # working version for one type of extension
    files_set = set()


def stringify(filename):
    for ch in [':', '\\', '/', '%']:
        if ch in filename:
            filename = filename.replace(ch, '')
    return filename


def getNewState(dir, extension):
    file_set = listFilesWithPattern(dir, extension)
    # print ("set[live]: ", file_set)
    return (file_set)


def getOldState(dir, extension):
    syncfilename = stringify(dir) + '.dat'
    with open(os.path.join(".", "data", syncfilename), 'rb') as f:
        file_set = pickle.load(f)
    # print ("set[_old]: ", file_set)
    return (file_set)


def setOldState(dir, extension):
    files_set2 = listFilesWithPattern(dir, extension)
    syncfilename = stringify(dir) + '.dat'
    with open(os.path.join(".", "data", syncfilename), 'wb') as f:
        pickle.dump(files_set2, f)
    return (files_set2)


def compare_states(state1, state2):
    print ("state[1]: ", state1)  # save the set of objects file and directory names.
    print ("state[2]: ", state2)
    return (state1 - state2, state2 - state1)


def checkSyncState(dir, fileext):
    # compare states from old file and new directory state
    print('Checking Sync Stats @', dir)
    try:
        in_dir1 = getNewState(dir, fileext) - getOldState(dir, fileext)
    except:
        in_dir1 = setOldState(dir, fileext)
        pass
    print ('----------------New Files-----------------')
    # print in_dir1

    if in_dir1:  # if not in_dir2 :  ####(to check if set is empty
        setOldState(dir, fileext)
        print "New Files Found in Sync. Parser will proceed", dir
        print in_dir1
    else:
        print "No File Changes. No Sync required...", dir
    print ('-----------------ENDING-----------------')
    return in_dir1


def searchAndPostRunLogs(dir, extension):
    # Add the Sync and compare module
    fileList = checkSyncState(dir, extension)
    # remainder of the list (New files get to next round)

    # for file in listFilesWithPattern(dir, extension):
    for file in fileList:
        print '----------------------------------'
        print "File Path:", file
        # from Run.log or ADRRun.log <text>
        recipe = ""
        recipeModifiedTimestamp = ""
        recipeCreatedTimestamp = ""
        result = ""
        resultTimestamp = ""
        waferID = 0  # slot
        pwaferID = 0
        portID = 0
        testID = []
        testCount = 0
        repeats = [1]  # default: 1 repeat per scan
        repeatsCount = 0
        timePerInspection = []
        toolID = ""
        toolAlias = ""
        resultsSWVersion = ""

        # Sample File post
        post = {"rawPath": file,
                # "isDir": os.path.isdir(p),
                # "type": os.path.splitext(p)[1],
                "ancestors": os.path.abspath(file).split(os.path.sep)[:-1],  # remove last element
                # "dateModified":os.path.getmtime(p),
                # "dateCreated":os.path.getctime(p),
                "path": os.path.abspath(file).replace('\\', '/').replace('/', ','),
                "inProcessed": False,
                "recipe": recipe,
                "recipeModifiedTimestamp": resultTimestamp,
                "recipeCreatedTimestamp": recipeCreatedTimestamp,
                "result": result,
                "resultTimestamp": resultTimestamp,
                "waferID": waferID,
                "portID": portID,
                "testID": testID,
                "testCount": testCount,
                "repeats": repeats,
                "repeatsCount": repeatsCount,
                "timePerInspection": timePerInspection,
                "toolID": toolID,
                "toolAlias": toolAlias,
                "toolModel": toolModel,
                "resultsSWVersion": resultsSWVersion,
                "logtext": logtext}
        pprint(post)
        post_id = collection.insert_one(post).inserted_id
        print (post_id)


# searchAndPostRunLogs(directory, "Run.log")


import glob

# open a log file for logging
errorlogfile = "RunLogParser" + datetime.datetime.now().isoformat() + ".log"
errorlogfile = os.path.join(".", "logs", stringify(errorlogfile))
logf = open(errorlogfile, "w")

# define /root dir for the document tree
path = r'/home/towshif/mounted'  # Ubuntu
resultFolders = glob.glob(path + r"\DATA*\*\Usr\Results*")
# resultFolders = glob.glob(path + r"/DATA*/*/Usr/Results*")  # Ubuntu

# for EBeam
# resultFolders = glob.glob(path + r"\*\Usr\Results*")
print resultFolders
for folder in resultFolders:
    print folder
    try:
        searchAndPostRunLogs(folder, "Run.log")
        print 'Search and Post Run Logs '
    except Exception as e:  # most generic exception you can catch
        logf.write("Failed to download {0}: {1}\n".format(str(errorlogfile), str(e)))
    # optional: delete local version of failed download
    finally:
        # optional clean up code
        pass

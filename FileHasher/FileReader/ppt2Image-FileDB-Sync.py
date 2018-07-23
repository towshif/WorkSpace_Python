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
collection = db['fileStor']  # or collection = db.posts

import pickle
# from os import walk
from scandir import \
    walk  # use scandir.walk instead of os.walk  - its faster (5-10x faster on win64; 3x on Linux, MacOS)

deepscanflag = True


# DEEP SCAN: All dir and subdirs needed for user folders K Drive etc.
def listFilesWithPattern2(directory, extension):  # working version for one type of extension
    files_set = set()
    for (dirpath, dirnames, filenames) in walk(directory):
        for file in filenames:
            for ext in extension:
                # print ("checking for *" + ext)
                if file.endswith(ext):
                    full_path = os.path.abspath(os.path.join(dirpath, file))
                    files_set.add(full_path)
                    # pprint(full_path)
    return files_set


# FAST (SURFACE) SCAN:  2 level scan /Lotname/*Run.log & /Lotname/Stepname/*RunLog
def listFilesWithPattern(directory, extension):  # working version for one type of extension
    files_set = set()
    resultFolders = glob.glob(directory + r"\*\*" + extension)
    resultFolders2 = glob.glob(directory + r"\*\*\*" + extension)
    resultFolders.append(resultFolders2)
    print(directory + r"\*\*" + extension)
    # print resultFolders
    print(directory + r"\*\*\*" + extension)
    # print resultFolders2

    return resultFolders


def stringify(filename):
    for ch in [':', '\\', '/', '%']:
        if ch in filename:
            filename = filename.replace(ch, '')
    return filename


def getNewState(dir, extension):
    if deepscanflag:
        print("Deep Scan Flag is ON. Running Deep Scan...this may take 5-30 mins...")
        file_set = listFilesWithPattern2(dir, extension)
    else:
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
    if deepscanflag:
        print("Deep Scan Flag is ON. Running Deep Scan...this may take 5-30 mins...")
        files_set2 = listFilesWithPattern2(dir, extension)
    else:
        files_set2 = listFilesWithPattern(dir, extension)

    syncfilename = stringify(dir) + '.dat'
    with open(os.path.join(".", "data", syncfilename), 'wb') as f:
        pickle.dump(files_set2, f)
    return (files_set2)


def setOldStatefromSet(dir, files_set2):
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
    newDir = set()
    oldDir = set()
    try:
        newDir = getNewState(dir, fileext)
        oldDir = getOldState(dir, fileext)
        in_dir1 = newDir - oldDir
    except:
        # in_dir1 = setOldState(dir, fileext)
        in_dir1 = newDir
        pass
    print ('----------------New Files-----------------')
    # print "New Dir", newDir
    # print "in_ Dir", in_dir1

    if in_dir1:  # if not in_dir2 :  ####(to check if set is empty
        # setOldState(dir, fileext)
        setOldStatefromSet(dir, newDir)
        print "New Files Found in Sync. Parser will proceed", dir
        print in_dir1
    else:
        print "No File Changes. No Sync required...", dir
    print ('-----------------ENDING-----------------')
    return in_dir1


def searchAndPostRunLogs(dir, extension):
    # Add the Sync and compare module
    fileList = checkSyncState(dir, extension)
    # fileList = listFilesWithPattern2(dir,extension)

    print(fileList)
    # remainder of the list (New files get to next round)

    # for file in listFilesWithPattern(dir, extension):
    for file in fileList:
        print '----------------------------------'
        print "File Path:", file
        # from Run.log or ADRRun.log <text>
        fname, filetype = os.path.splitext(file)
        path, filename = os.path.split(file)
        fileModifiedTimestamp = os.path.getmtime(file)
        fileCreatedTimestamp = os.path.getctime(file)
        size = os.path.getsize(file)

        # tag generate from path and folder tree nodes
        tags = []
        path = path.replace(os.path.abspath(dir), '')  # remove root path from path string
        while 1:
            path, folder = os.path.split(path)
            if folder != "":
                tags.append(folder)
            else:
                if path != "":
                    tags.append(path)
                break
        tags.reverse()

        # remove duplicates and list of literals if present in tags
        rmList = ['\\', '/', '//', ',', '.']
        tags = list(set(tags) - set(rmList))
        print tags

        # Match Logs (for debugging)
        logtext = ""

        # Sample File post
        post = {"rawPath": file,
                # "isDir": os.path.isdir(p),
                # "type": os.path.splitext(p)[1],
                "ancestors": os.path.abspath(file).split(os.path.sep)[:-1],  # remove last element
                # "dateModified":os.path.getmtime(p),
                # "dateCreated":os.path.getctime(p),
                "path": os.path.abspath(file).replace('\\', '/').replace('/', ','),
                "relPath": file.replace(os.path.abspath(dir), ''),
                "inProcessed": False,
                "filename": filename,
                "filetype": filetype,
                "size": size,
                "modified": fileModifiedTimestamp,
                "created": fileCreatedTimestamp,
                "tags": tags,
                "logtext": logtext}

        pprint(file)
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
# path = r'/home/towshif/mounted'  # Ubuntu

# path = r'/home/towshif/mounted'  # Ubuntu

root = "G:\OneDrive - KLA-Tencor Corporation\Data\ExecReview"

extensions = {".ppt", ".pptx", ".doc", ".docx", ".pdf"}
# extensions = {".ppt"}

try:
    searchAndPostRunLogs(root, extensions)
    # listFilesWithPattern2 (root, extensions)
    print 'Search and Post Run Logs '
except Exception as e:  # most generic exception you can catch
    logf.write("Failed to download {0}: {1}\n".format(str(errorlogfile), str(e)))
# optional: delete local version of failed download
finally:
    # optional clean up code
    pass

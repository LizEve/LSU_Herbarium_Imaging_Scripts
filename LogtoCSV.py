import os
import datetime as dt


# script - will need to run for both workstations. 
# constants:
# log folder (on workstation storage drives) get as input when calling in rsync file 
logFolder = '/mnt/LSUCollectionsWS1/Logs/' # get from bash script
# csv out folder (on workstation storage drives) - get from bash script 
csvFolder='/mnt/LSUCollections/UnmappedCSV/'
# base folder for collection (/data/LSUCollections/)
baseFolder = 'http://cyberfloralouisiana.com/images' 

todaysFilesList=[]

# Get list of all log files edited on todays date. in log folder
now = dt.datetime.now()
ago = now-dt.timedelta(days=1)

# Walk through, get date time, and add that file to list
for root, dirs,files in os.walk(logFolder):  
    for fname in files:
        path = os.path.join(root, fname)
        st = os.stat(path)    
        mtime = dt.datetime.fromtimestamp(st.st_mtime)
        if mtime > ago:
            todaysFilesList.append(path)

for logFile in todaysFilesList:
    logF = open(logFile,"r")
    for line in logF

# for each log file edited today
# do 
# get date from name of log folder 
# for each line in log file (VascFake/LSU/00/004/LSU00004314.JPG)
# do 
# get portal (first folder in path)
# get name of csv file image path would be filed in - portal + date 
# get line to add to csv file 
#     - grab barcode
#     - get path 
#     - make path to each file - append base folder to path 
#     - make csv string for this file 
# if csv file exists
# - append csv string to file 
# elif csv file does not exists
# - create file and add header
# - append csv string to file 
# - done 




oPath = 'VascFake/LSU/00/004/LSU00004314_1.JPG'

path = os.path.split(oPath)[0]



fileName=os.path.basename(oPath).split(".")[0]
# Get barcode 
barCode=fileName.split("_")[0]
# Create web ready and thumbnail paths 
wrPath=os.path.join(path,fileName+'_WR.JPG')
tnPath=os.path.join(path,fileName+'_TN.JPG')
lgPath=os.path.join(path,fileName+'_L.JPG')


fileName
barCode
wrPath
tnPath
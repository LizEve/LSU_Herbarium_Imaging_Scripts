import os
import glob
import datetime as dt
import pandas as pd

def makeLog(logFolders,csvFolder,webPath,header):

    # Get list of all log files edited on todays date. in log both folders
    todaysFilesList=[]

    # Set times for the last day
    now = dt.datetime.now()
    ago = now-dt.timedelta(days=10000)

    # Make list of files from all log folders 
    for logFolder in logFolders:

        # Get all files in Log Folder
        logFolderList = []
        for file in os.listdir(logFolder):
            if file.endswith(".txt"):
                path = os.path.join(logFolder, file)
                logFolderList.append(path)

        # Get all files that were modified today 
        for p in logFolderList:
            #print(path)
            st = os.stat(p)    
            mtime = dt.datetime.fromtimestamp(st.st_mtime)
            if mtime > ago:
                todaysFilesList.append(p)
    print(todaysFilesList)

    # Iterate through log files from today 
    for logFile in todaysFilesList:
        # Get the date from the log name 
        logDate = os.path.basename(logFile).split("_")[0]
        #print(logDate)

        # Open the file 
        logF = open(logFile,"r")
        #print(logFile)

        # Loop through lines in log file 
        for oPath in logF:

            # Get portal name 
            portal=oPath.split("/")[0]

            # Get path to csv file line will be written to.
            #print(csvFolder,logDate,portal)
            csvPath = os.path.join(csvFolder,logDate+"_"+portal+".csv")
            #print(csvPath)

            # Get path to original image
            path = os.path.split(oPath)[0]

            # Get file name without extension
            fileName=os.path.basename(oPath).split(".")[0]

            # Get barcode 
            barCode=fileName.split("_")[0]

            # Create web ready and thumbnail paths to web address 
            wr=os.path.join(webPath,path,fileName+'_WR.JPG')
            tn=os.path.join(webPath,path,fileName+'_TN.JPG')
            lg=os.path.join(webPath,path,fileName+'_L.JPG')

            # Creat csv file line
            info=[barCode,lg,tn,wr]
            csvLine=','.join(info)

            # If csv file does not exist, create with header 
            if not os.path.exists(csvPath):
                #print(header)
                with open(csvPath,"w") as csvFile:
                    csvFile.write("%s\n" % header)
                    csvFile.close()
                     
            # If csv file exists, add new line 
            elif os.path.exists(csvPath):
                #print(csvLine)
                with open(csvPath,"a") as csvFile:
                    csvFile.write("%s\n" % csvLine)
                    csvFile.close()
            else:
                print("This should never happen")

def main():
    # script - will need to run for both workstations. 
    # constants:
    # log folders where log files are
    logFolder1 = '/mnt/LSUCollectionsWS1/Logs/'
    logFolder2 = '/mnt/LSUCollections/Logs/'
    #logFolder1 = '/Users/ChatNoir/Projects/HerbariumRA/test/'
    #logFolder2 = '/Users/ChatNoir/Projects/HerbariumRA/test/test1/'

    logFolders = [logFolder1,logFolder2]
    
    # csv out folder - put all csv files on one computer for Jennie 
    csvFolder='/mnt/LSUCollections/CSVLogs/'
    #csvFolder='/Users/ChatNoir/Projects/HerbariumRA/test/csv/'
    # Web address for link
    webPath = 'http://cyberfloralouisiana.com/images' 
    # Header for csv file
    csvHeader = ['catalogNumber','large JPG','thumbnail','webview']
    header = ",".join(csvHeader)
    # Call function
    makeLog(logFolders,csvFolder,webPath,header)

if __name__ == "__main__":
    main()

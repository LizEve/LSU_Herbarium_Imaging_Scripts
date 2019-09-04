import os
import pickle 
from csv import DictReader

def portalDict(occurrencesFile,portalName,colName,outPkl,outFolder):
    '''
    Get dictionary of all barcodes and respective portal names
    Input - csv file, header for col of barcodes, header for col of portal names
    Output - Dictionary of barcodes: portal name 
    '''
    # Open csv file and grab both columns. then close file
    csv_file = open(occurrencesFile, "r")
    catNumList = [row[colName] for row in DictReader(csv_file)]
    csv_file = open(occurrencesFile, "r")
    portalNameList = [row[portalName] for row in DictReader(csv_file)]
    csv_file.close()
    # Start dictionary
    portalDictionary={}
    # Create dictionary from two csv lists
    l=len(catNumList)
    for n in range(0,l):
        portalDictionary[catNumList[n]]=portalNameList[n]
    # Turn barcodes into caps 
    dictCaps = dict((k.upper(), v) for k, v in portalDictionary.items())
    # Create output file. Write a python readable dictionary to file
    outD = open(os.path.join(outFolder,outPkl+".pkl"),'wb')
    pickle.dump(dictCaps,outD)
    outD.close()
    return portalDictionary

def main():
    #occurrencesFile="/Users/ChatNoir/Projects/HerbariumRA/MasterPortalList/masterDF_july24.csv"
    #portalName="portalName"
    #colName="catalogNumber"
    #outFolder = "/Users/ChatNoir/Projects/HerbariumRA/MasterPortalList/"
    #outPkl = 'masterDF_july24'
    #portalDictionary=portalDict(occurrencesFile,portalName,colName,outPkl,outFolder)

    occurrencesFile="/Users/ChatNoir/Google Drive/Herbiarum_Notes/ImageSpreadSheets/ULM_RepatriationSet3_forNEW_ImageServer.csv"
    portalName="portalName"
    colName="catalogueNumber"
    outFolder = "/Users/ChatNoir/Google Drive/Herbiarum_Notes/ImageSpreadSheets/"
    outPkl = 'ULM_RepatriationSet3_sept04'
    portalDictionary=portalDict(occurrencesFile,portalName,colName,outPkl,outFolder)



if __name__ == "__main__":
    main()

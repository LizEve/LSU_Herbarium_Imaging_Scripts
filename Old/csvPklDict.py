import os
import csv
import pickle 
from csv import DictReader

def portalDict(occurrencesFile,portalName,colName,outPkl):
    '''
    Get dictionary of all barcodes and respective portal names
    Input - occurrences.csv, name of portal, and name of column with barcodes
    Output - Dictionary of barcodes and portal name for each barcode
    '''
    csv_file = open(occurrencesFile, "rU")
    catNumList = [row[colName] for row in DictReader(csv_file)]
    csv_file = open(occurrencesFile, "rU")
    portalNameList = [row[portalName] for row in DictReader(csv_file)]
    csv_file.close()
    portalDictionary={}
    l=len(catNumList)
    for n in range(0,l):
        portalDictionary[catNumList[n]]=portalNameList[n]
    # return an all caps dicts
    dictCaps = dict((k.upper(), v) for k, v in portalDictionary.items())
    outD = open(os.path.join(outFolder,outPkl+"D.pkl"),'wb')
    outL = open(os.path.join(outFolder,outPkl+"L.pkl"),'wb')
    pickle.dump(dictCaps,outD)
    pickle.dump(catNumList,outL)
    outD.close()
    outL.close()
    return portalDictionary

def main():
    occurrencesFile="/Users/ChatNoir/Projects/HerbariumRA/play/masterDF_may27.csv"
    portalName="portalName"
    colName="catalogNumber"
    outPkl = 'csv_Jun07'
    portalDictionary=portalDict(occurrencesFile,portalName,colName,outPkl)



if __name__ == "__main__":
    main()

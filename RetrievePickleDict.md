
```python
import pickle 

def pickleOpen(p):
    file=open(p,'rb')
    data = pickle.load(file)
    file.close()
    return data

oldPathDictionary=pickleOpen('oldPathDictionary.pkl')
portalDictionary=pickleOpen('portalDictionary.pkl')
barcodeImageDict=pickleOpen('barcodeImageDict.pkl')
barcodeNoImageDict=pickleOpen('barcodeNoImageDict.pkl')


m29=pickleOpen('oldPathDictionary29.pkl')
m30=pickleOpen('oldPathDictionaryMay30.pkl')

```


```python
import csv 
from csv import DictReader
import os

def portalDict(occurrencesFile,portalName,colName="catalogNumber"):
    '''
    Get dictionary of all barcodes and respective portal names
    Input - occurrences.csv, name of portal, and name of column with barcodes
    Output - Dictionary of barcodes and portal name for each barcode
    '''
    csv_file = open(occurrencesFile, "r")
    catNumList = [row[colName] for row in DictReader(csv_file)]
    csv_file = open(occurrencesFile, "r")
    portalNameList = [row[portalName] for row in DictReader(csv_file)]
    csv_file.close()
    portalDictionary={}
    l=len(catNumList)
    for n in range(0,l):
        portalDictionary[catNumList[n]]=portalNameList[n]
    # return an all caps dicts
    output = open("portalDictionary.pkl",'wb')
    pickle.dump(portalDictionary,output)
    output.close()
    return portalDictionary


occurrencesFile="./masterDF_may27.csv"
portalName="portalName"
colName="catalogNumber"
portalDictionary=portalDict(occurrencesFile,portalName,colName)


csv_file = open(occurrencesFile, "r")
catNumList = [row[colName] for row in DictReader(csv_file)]
csv_file = open(occurrencesFile, "r")
portalNameList = [row[portalName] for row in DictReader(csv_file)]
csv_file.close()

len(portalNameList)
len(catNumList)
len(set(portalNameList))
len(set(catNumList))
```

numbers add up 
365808 unique barcodes in mastercsv file

342267 barcodeImageDict.txt
23541 barcodeNoImageDict.txt


May29 and 30th files not the same not sure why. 

s29=set(m29.keys())
s30=set(m30.keys())
len(s30.intersection(s29))
723611
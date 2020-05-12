import pandas as pd
import pickle
import datetime
import itertools
import pathlib2 as pathlib


def pickleOpen(p):
    file=open(p,'rb')
    data = pickle.load(file)
    file.close()
    return data

# Read in dictionary for all files moved 
inFile = '/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL/temp_newPaths_Aug09.pkl'
inDict = pickleOpen(inFile)
outFile = '/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL/temp_newPaths_Aug11.csv'
#['Barcode_ID','Portal', 'Collection_Code', 'Date','File_Path','Large_Path']
newDict = {}
# Iterate through input dictionary
for key,value in inDict.items():
    # Parse out each part of value list
    b=value[0]
    p=value[1]
    d=value[2]
    np=value[3]
    # Transform epoch time to date time string 
    nd=str(datetime.datetime.fromtimestamp(int(d)))
    # Get theoretical path to "large" smaller image
    lnewPath=str(pathlib.Path(np).with_suffix(""))+str("_L.JPG")
    # Get letters of collection institution from barcode 
    b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]
    # Add all of this to a new dictionary. key is filename. 
    newDict[key]=[b,p,b_letters,nd,d,np,lnewPath]
inPD = pd.DataFrame.from_dict(newDict,orient='index', columns=['Barcode_ID','Portal','Collection_Code','Date','Epoch','File_Path','Large_Path'])
inPD.index.name = 'File_Name'
inPD.to_csv(outFile,sep=',')

'''
# Read in dictionary for all files moved 
inFile = '/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL/temp_newPaths_Aug09.pkl'
inDict = pickleOpen(inFile)
# filename:[barcode, portal, date, current(new) path]
tables = ['Algae',  'Bryophyte',  'Fungi',  'Lichen',  'Vascular', 'NoPortal']
for t in tables:
    outFile = '/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL/temp_'+t+'_Aug09.csv'
    #['Barcode_ID','Portal', 'Collection_Code', 'Date','File_Path','Large_Path']
    newDict = {}
    # Iterate through input dictionary
    for key,value in inDict.items():
        # Parse out each part of value list
        b=value[0]
        p=value[1]
        d=value[2]
        np=value[3]
        # If record from this portal. get more info and eventually save
        if p == t:
            # Transform epoch time to date time string 
            nd=str(datetime.datetime.fromtimestamp(int(d)))
            lnewPath=str(pathlib.Path(newPath).with_suffix(""))+str("_L.JPG")
            b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]
            newDict[key]=[b,p,b_letters,nd,n,np,lnewPath]
    inPD = pd.DataFrame.from_dict(newDict,orient='index', columns=['Barcode_ID','Portal','Collection_Code','Date','Epoch','File_Path','Large_Path'])
    inPD.index.name = 'File_Name'
    inPD.to_csv(outFile,sep=',')
'''
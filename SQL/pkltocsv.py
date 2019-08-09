import pandas as pd
import pickle
import datetime
import itertools

def pickleOpen(p):
    file=open(p,'rb')
    data = pickle.load(file)
    file.close()
    return data

# Read in dictionary for all files moved 
inFile = '/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL/temp_newPaths_Aug09.pkl'
inDict = pickleOpen(inFile)
# filename:[barcode, portal, date, current(new) path]
tables = ['Algae',  'Bryophyte',  'Fungi',  'Lichen',  'Vascular', 'NoPortal']
for t in tables:
    outFile = '/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL/temp_'+t+'_Aug09.csv'
    #['Barcode_ID','Portal', 'Collection_Code', 'Date','File_Path']
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
            print(b)
            b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]
            newDict[key]=[b,p,b_letters,nd,np]
    inPD = pd.DataFrame.from_dict(newDict,orient='index', columns=['Barcode_ID','Portal','Collection_Code', 'Date','File_Path'])
    inPD.index.name = 'File_Name'
    inPD.to_csv(outFile,sep=',')

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
# fileName: [barcode,time,path]
inFile = '/Users/ChatNoir/Google Drive/Herbiarum_Notes/ImageSpreadSheets/lsu_movedFiles_Aug12_filename.pkl'
inDict = pickleOpen(inFile)
outFile = '/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL/temp_masterDB_Aug12.csv'
#['Barcode_ID','Portal', 'Collection_Code', 'Date','File_Path','Large_Path']
newDict = {}
barcodeLen = 11

# Iterate through input dictionary
for key,value in inDict.items():
    # Parse out each part of value list
    b=value[0] # barcode
    d=value[1] # date time
    np=value[2] # new path

    # if barcode is the right lenght, go through a lot of stuff. 
    if len(b) == int(barcodeLen):
        # Split apart letters and numbers from barcode
        try:
            b_letters,b_numbers = ["".join(x) for _, x in itertools.groupby(b, key=str.isdigit)]       
        # For bad barcodes move them to a special folder for Jennie to check. 
        except ValueError:
            pass
        # For all good barcodes that can be split into Letters/Numbers
        else:
                # Transform epoch time to date time string 
                nd=str(datetime.datetime.fromtimestamp(int(d)))
                # Get theoretical path to "large" smaller image
                lnewPath=str(pathlib.Path(np).with_suffix(""))+str("_L.JPG")
                # Get portal from path 
                p=np.split('/')[3]
                # Add all of this to a new dictionary. key is filename. 
                newDict[key]=[b,p,b_letters,nd,d,np,lnewPath]





inPD = pd.DataFrame.from_dict(newDict,orient='index', columns=['Barcode_ID','Portal','Collection_Code','Date','Epoch','File_Path','Large_Path'])
inPD.index.name = 'File_Name'
inPD.to_csv(outFile,sep=',')


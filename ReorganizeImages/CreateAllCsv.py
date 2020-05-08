import os
import pickle
import pandas as pd


def makeCSV(inFilePath,f,r):
    
    # Open pickle file 
    originalPathList = pickle.load(open(inFilePath,'rb'))

    # Initiate dictionary 
    d = {}

    for oPath in originalPathList:
        
        # Get path 
        path = os.path.split(oPath)[0]

        # Get file name without extension
        fileName=os.path.basename(oPath).split(".")[0]

        # Get barcode 
        barCode=fileName.split("_")[0]

        # Create web ready and thumbnail paths 
        wrPath=os.path.join(path,fileName+'_WR.JPG')
        tnPath=os.path.join(path,fileName+'_TN.JPG')
        lgPath=os.path.join(path,fileName+'_L.JPG')

        # Change path to web address
        wr=wrPath.replace(f,r)
        tn=tnPath.replace(f,r)
        lg=lgPath.replace(f,r)

        d[fileName]=[barCode,lg,tn,wr]

    return d


def main():
    col='Algae'
    #col='Bryophyte'
    #col='Fungi'
    #col='Lichen'
    homeFolder='/Users/ChatNoir/Projects/HerbariumRA/test'
    inFilePath=os.path.join(homeFolder,str(col)+'.p')
    outFilePath=os.path.join(homeFolder,str(col)+'.csv')
    # /data/LSUCollections/Algae/LSU/00/169/LSU00169318_1.JPG
    f = '/data'
    r ='http://cyberfloralouisiana.com/images' 
    d1 = makeCSV(inFilePath,f,r)
    print(outFilePath)
    df = pd.DataFrame.from_dict(d1,orient='index',columns=['catalogNumber','large JPG','thumbnail','webview'])
    df.reset_index(drop=True,inplace=True)
    df.to_csv(outFilePath,sep=",",index=False)

if __name__ == "__main__":
    main()


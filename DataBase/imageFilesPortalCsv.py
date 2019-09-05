import os
import itertools
import pickle
import platform
import pandas as pd


def pathDict(root,unwanted,find,replace,portal):
    '''
    Get dictionary of all image files in root folders 
    Input- root directory,  list of file extentions to ignore
    Output- two dictionaries
    dict1 - filename: [barcode, current path]
    '''
    # Set up empty dictionaries
    dict1={}
    dict2={}
    x=0
    # Walk through all folders and files. Not using path or subdirs 
    for path, subdirs, files in os.walk(root):
        # Ignore hidden directories as files, those that start with "."
        files = [f for f in files if not f[0] == '.']
        for name in files:
            # Do not keep any files from unwanted list
            if any(x in name for x in unwanted):
                pass
            else:
                # Combine path and name
                p=os.path.join(path,name)
                p.replace(find,replace)
                # Get barcode from file name 
                b=name.split(".")[0].split("_")[0].split("-")[0]
                # Put into dictionary dict1
                dict1[x]=[b,name,portal,p]
                x =+ 1
    return dict1


def main():
    # List unwanted extensions
    unwanted=["txt","tmp","csv","zip","_s","_m","_l","_S","_M","_L"]
    # Full path to folder for output lists
    outFolder='/home/ggmount/'
    outName='LSU_Fungi_portal'
    # Get dictionaries of files and barcodes 
    find = '/data'
    replace ='http://images.cyberfloralouisiana.com/images' 
    portal = 'Fungi'
    # Full path of current parent folders of images
    root2 = '/data/LSUCollections/Fungi/'
    # filename: [barcode, file name, portal, current path]
    d1=pathDict(root2,unwanted,find,replace,portal)
    # Save dictionaries to csv file 
    # {filename:[barcode,portal,newpath]}
    df = pd.DataFrame.from_dict(d1,orient='index',columns=['CatalogNumber','ImageFileName','Portal','originalurl'])
    df.to_csv(os.path.join(outFolder,(outName+".csv")),sep=",")

    root3 = '/data/LSUCollections/Bryophyte/'
    root4 = '/data/LSUCollections/Algae/'
    root5 = '/data/LSUCollections/Lichen/'
    root6 = '/data/LSUCollections/Vascular/'



if __name__ == "__main__":
    main()

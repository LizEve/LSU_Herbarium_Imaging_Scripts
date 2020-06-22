import os
import itertools
import shutil 
import pickle 


def reSize(root,tempTrash,unwanted,originalFileList,outFilePath,remove):
    # Walk through all folders and files. Not using path or subdirs 
    for path, subdirs, files in os.walk(root):

        # Ignore hidden directories as files, those that start with "."
        files = [f for f in files if not f[0] == '.']
        for name in files:

            # Do not keep any files from unwanted list, only original files
            if any(x in name for x in unwanted):
                pass

            # For all original size files
            else:
                # Combine path and original file name
                originalPath=os.path.join(path,name)

                # Add original path to list, using this list for things later 
                originalFileList.append(originalPath)

                # Get file name without extension
                fileName=name.split(".")[0]

                # Get paths for files we want to make and move
                wrPath=os.path.join(path,fileName+'_WR.JPG')
                tnPath=os.path.join(path,fileName+'_TN.JPG')
                lgPath=os.path.join(path,fileName+'_L.JPG')

                # Check for web ready version, if not there, make it from original
                if os.path.exists(wrPath) and os.path.getsize(wrPath) > 0:
                    print(str(originalPath)+" - wr")
                else:
                    os.system("convert %s -units pixelsperinch -density 80x80 -resize 1400x1400^ -quality 80 %s"%(originalPath,wrPath))
                    print(str(originalPath)+" - wr")

                # Check for thumb nail version, if not there, make it from original
                if os.path.exists(tnPath) and os.path.getsize(tnPath) > 0:
                    print(str(originalPath)+" - tn")
                else:
                    os.system("convert %s -units pixelsperinch -density 80x80 -resize 200x200^ -quality 80 %s"%(originalPath,tnPath))
                    print(str(originalPath)+" - tn")

                # Write over any old large files 
                os.system("convert %s -quality 95 %s"%(originalPath,lgPath))
                print(str(originalPath)+" - lg")

                # Check for Large version, if not there, make it from original
                #if os.path.exists(lgPath) and os.path.getsize(lgPath) > 0:
                #    print(str(originalPath)+" - lg")
                #else:
                #    os.system("convert %s -quality 95 %s"%(originalPath,lgPath))
                #    print(str(originalPath)+" - lg")

                # Move unwanted files 
                for u in remove:
                    rPath=os.path.join(path,fileName+u)
                    try:
                        shutil.move(rPath,tempTrash)
                    except:
                        pass 

    # Save list into a pickle file for later use. 
    outFile = open(outFilePath,'wb')
    pickle.dump(originalFileList,outFile)
    outFile.close()



def main():
    #col='Algae'
    #col='Bryophyte'
    #col='Fungi'
    #col='Lichen'
    #col='lsus'
    col='thib'
    unwanted=["thumb","txt","tmp","csv","zip","_s","_m","_l","_S","_M","_L","WR","TN","CR2","cr2"]
    remove=["_s.jpg","_m.jpg","_l.jpg","_thumb.jpg"]
    tempTrash='/data/lost+found/'
    #root=os.path.join('/data/LSUCollections/',col)
    root=os.path.join('/data/nfsshare/',col)
    originalFileList=[]
    outFilePath=os.path.join('/home/ggmount/',str(col)+'.p')

    reSize(root,tempTrash,unwanted,originalFileList,outFilePath,remove)

if __name__ == "__main__":
    main()

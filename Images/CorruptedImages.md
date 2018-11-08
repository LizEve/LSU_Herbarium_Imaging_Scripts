
# Notes

It looks like there are many types of corruption, and the methods for IDing corruption is dependant on what is the source of the corruption. 

# Sources

Corruption of Graphics Files <http://www.fileformat.info/mirror/egff/ch08_04.htm>

How do I programmatically check whether an image (PNG, JPEG, or GIF) is corrupted? <https://stackoverflow.com/questions/1401527/how-do-i-programmatically-check-whether-an-image-png-jpeg-or-gif-is-corrupte>

```python
from PIL import Image

v_image = Image.open(file)
v_image.verify()
```
'If you really want to cover everything, you can try show() or even better: load(). These will raise an exception if it fails, mostly OSError. '

Prewritten python program <https://bitbucket.org/denilsonsa/small_scripts/src/f609067ed37392007fa686748bb2ce7f12717ef8/jpeg_corrupt.py?at=default&fileviewer=file-view-default>

# Tests

## Download files

```bash
cp /data_storage/nfsshare/nlu/0/5/83/16/* /home/gmount1/corruptedImages
cp /data_storage/nfsshare/nlu/0/4/34/54/* /home/gmount1/corruptedImages
cp /data_storage/nfsshare/nlu/0/3/55/17/* /home/gmount1/corruptedImages

cp /data_storage/nfsshare/nlu/0/5/83/22/* /home/gmount1/corruptedImages
cp /data_storage/nfsshare/nlu/0/4/34/22/* /home/gmount1/corruptedImages
cp /data_storage/nfsshare/nlu/0/3/55/22/* /home/gmount1/corruptedImages


rsync -avzure ssh --stats --progress gmount1@cyberflora.lsu.edu:/home/gmount1/corruptedImages/* /Users/ChatNoir/Projects/HerbariumRA/corruptedImages
```

## Check image

This works on the NLU images but not on my personal images. 

```python
from PIL import Image
import os
import ntpath

fileList=[]  
root="/Users/ChatNoir/Projects/HerbariumRA/corruptedImages"
for path, subdirs, files in os.walk(root):
    for name in files:
        oldPath=os.path.join(path,name)
        fileList.append(oldPath)


for f in fileList:
    if f.endswith(".jpg"):
        try:
                v_image = Image.open(f)
                print(ntpath.basename(f))
                try:
                        x=v_image.load()
                except Exception as e:
                        print(str(e))
        except IOError as f:
                print(str(f))
```

```python
oldPathList=[]
root="/Users/ChatNoir/Projects/HerbariumRA/corruptedImages"
for path, subdirs, files in os.walk(root):
    for name in files:
        oldPath=os.path.join(path,name)
        oldPathList.append(oldPath)
```


IMG_3523.jpg     NLU0035517.jpg   NLU0043454.jpg   NLU0058316.jpg
IMG_3525.jpg     NLU0035517.txt   NLU0043454.txt   NLU0058316.txt
IMG_3528.jpg     NLU0035517_l.jpg NLU0043454_l.jpg NLU0058316_l.jpg
IMG_3578.jpg     NLU0035517_m.jpg NLU0043454_m.jpg NLU0058316_m.jpg
IMG_3877.jpg     NLU0035517_s.jpg NLU0043454_s.jpg NLU0058316_s.jpg


## Iterate

```python
import os

files=[]   
for filename in os.listdir('.'):
  if filename.endswith('.jpg'):
    files.append(filename)
```

## Attempted, failed

### image magik

same as python with NLU and my image files. 

`identify -verbose -regard-warnings NLU0043454.jpg >/dev/null && echo File is OK. || echo File is corrupted.`


import imghdr
for f in files:
    print(ntpath.basename(f))
    imghdr.what(f)
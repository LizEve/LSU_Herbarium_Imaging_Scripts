<http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/index.html>
<http://staff.washington.edu/rowen/TkinterSummary.html#BasicTkApplication>
<https://wiki.wxpython.org/wxPython%20by%20Example>
google - wx python program examples
# To Do:
- find gui window that continually lists files in two folders
- start with first, check for files function


# Buttons needed

- press okay to continue script
- choose a or b
- alert when more than 1 file in unlabeled/
- press okay to continue with more than 1 in 

# Screens wanted

- do something to open python script window? start running script
- show screen with files in "unlabeled/" 
- screen with files in "/session"

# Output 

- sessions by day, one file or mult? by month? 


# Gui pseudo code V1:

```python
Open window
continually display and update contents of unlabeled and session 

```


# Pseudo Code V2:

```python

Do something to open python script window? start running script
def checkforphotos()"
while photos in "/unlabeled" == 0:
    raise message window "no files in incoming folder"
if photos in "/unlabeled" == 1:
    no message window
    return nphotos = 1
elif photos in "/unlabeled" > 1:
    raise alert "multiple photos in /unlabeled, these will be automatically numbered, if you dont want this, please manually delete duplicate photos"
    multphotos = T/F:
    if multphotos == T:
        return nphotos = nphotos
    elif multphotos == F:
        display "waiting for photos to be deleted"
        when photos in "/unlabeled" ==1: OR user input click button "just kidding keep all photos"
            return nphotos = nphotos
        
def scanbarcode(): 
# Make sure barcode is only scanned once. not barcodebarcode. check length? 
if barcode exists and unlabeled == 0 photos:
   raise alert "please take photo"
    exit function. return to checkforphots
barcode = scanned and checked barcode
return barcode

def renameFiles():
if photos in "/unlabeled/*IMG" == 1:
    number with barcode
elif barcode exists and photos in "/unlabeled/*IMG" > 1:
    number with  barcode_1 etc. 

# we are still in /unlabeled folder (im not sure if i want to move these once they are barcoded, to help with workflow)

# check last scanned barcode against mySQL database
def mysqlcheck():
if barcode in mySQL:
    raise alert "this has been barcoded before. overwrite old file?"
    overwrite = yes or no
    # require user input "overwrite OR delete new version"
    if overwrite == yes:
        continue with process, ie do nothing 
        return TRUE
    elif overwrite == no:
        delete all files unlabeled/barcode*.CR2
        if unlabeled/ == 0:
            return TRUE
        else:
            print "error file not deleted"
else: # barcode not in mysql
    return TRUE

def sessionfiles():
# store in session folder
if mySQLcheck == TRUE:
    put all files == barcode into "/session"
    erase barcode from memory
```

# Cron Jobs:
- daily download/update of mysql database locally. 
- daily push/upload of all images from the day  
- barcodes per day by taxon group
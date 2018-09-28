EOS - camera software. 
- can change where photos go to. Monitor folder. Destination folder 

DPP v.4

Take photo

alt Rename

- CAN rename with barcode, but much more tedious 

silver biology
- mult images, keep tabs on unlabeled incoming folder. alert if more than one photo in incoming folder at once. raise error 

alert for mult images
- when you scan barcode or when you take photo? 


barcode double checker - ie have you already barcoded this? check everything in LaCie drives. 
- use MySQL downloaded locally on a regular basis to check. 
- give option to overwrite or not
- pop up screen when you barcode

jpeg that gets uploaded is what gets edited. 


barcoding moves it automatically to session 

in session folder - do batch processing things. save as jpeg in DPP. stays in session folder. have jpg and CR2 in session folder. 

Silver biology - Finalize session. press button "file images"
log prints out how many images are "filed" , Jennie compares this to the number of photos in DPP to make sure they are the same. 
- I think this step means its moved to LaCie. 

uploading is automated.

Silverbiology has "History" tab that says filed or transfered. transfered means it has been pushed to server.

change scripts to 11pm upload and store. 

keep log of all images/barcodes taken per day. number uploaded to server. number logged. 



Pseudo Code:

Take photo
# photo goes into "/unlabeled" as specified by DPP and EOS
Potentially take more photos
    if photos in "/unlabeled" > 1:
        raise alert "multiple photos in /unlabeled, these will be automatically numbered, if you dont want this, please manually delete duplicate photos"

# only target IMG photos
# Need to add in some premade thing to get scanned barcode
# wait for user input
scan barcode 
# Make sure barcode is only scanned once. not barcodebarcode. check length? 
barcode = scanned and checked barcode
# Label based on number of *IMG files (unbarcoded files) in unlabled folder
if photos in "/unlabeled/*IMG" > 1:
    number with  barcode_1 etc. 
elif photos in "/unlabeled/*IMG" == 1:
    number with barcode
else:
    raise alert "no photos or unlabled photos in unlabeled folder, please take a photo or revert name"

# we are still in /unlabeled folder (im not sure if i want to move these once they are barcoded, to help with workflow)

# check last scanned barcode against mySQL database

if barcode in mySQL:
    raise alert "this has been barcoded before"
    require user input "overwrite OR delete new version"
    if overwrite:
        continue with process, ie do nothing 
        return TRUE
    elif delete new version:
        remove all files unlabeled/barcode*.CR2
        return TRUE
else:
    return TRUE

# store in session folder
if mySQL check == TRUE:
    put all files == barcode into "/session"




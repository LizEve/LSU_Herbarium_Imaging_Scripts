
# Terms

## Darwin Core Archive (DwC-A)

Darwin Core Archive (DwC-A) is a biodiversity informatics data standard that makes use of the Darwin Core terms to produce a single, self contained dataset for sharing species-level (taxonomic), species-occurrence data, and sampling-event data. An archive is a set of text files, in standard comma- or tab-delimited format, with a simple descriptor file (called meta.xml) to inform others how your files are organised. The format is defined in the Darwin Core Text Guidelines. It is the preferred format for publishing data in the GBIF network.
A DwC-A may consist of a single data file or multiple files, depending on the scope of the published data. The entire collection of files (core data, extensions, metafile, and resource metadata) can be compressed into a single archive file.
GUID(globally unique identifiers) is the "core ID"

<https://github.com/gbif/ipt/wiki/DwCAHowToGuide>

# Imaging Programs

## The Integrated Publishing Toolkit: IPT

A free open source software tool used to publish and share biodiversity datasets through the GBIF network.

<https://www.gbif.org/ipt>

## LBCC Imaging workflow application

The imaging workflow is a Java v7 application for accumulating label images and their associated metadata for submission to the central FTP site in Florida for processing.

<http://lbcc1.acis.ufl.edu/?q=workflow_application>
<http://lbcc1.acis.ufl.edu/project_resources>

## CPNH Consortium of Pacific Northwest Herbaria

Full documentation describing their digitization efforts and progress made to date, including server configuratons and processing scripts

<http://www.pnwherbaria.org/documentation/specimenimaging.php>


## iDigBio Media Appliance

The iDigBio Media Appliance is a cross-platform local web app that is used to upload media files from a local computer environment into iDigBio storage where they become available on the public Internet.
<http://symbiota.org/docs/idigbio-media-ingestion-application/>
<http://symbiota.org/docs/image-submission-2/>


# Symbiota Related

## Batch upload images
Remote Image Storage – Images can also be processed and stored on a remote server and mapped to the specimen image through the full image URL. Standalone image processing scripts will be needed to process images and map image URLs to the portal database. Scripts can configured to write the image URL directly to the database or image metadata can be written to a log file, which is loaded into the database afterwards. Remote images must be mapped in the database using the full image URL with the domain name. Standalone script can be found in the following Symbiota directory: /trunk/collections/specprocessor/standalone_scripts/ 
<http://symbiota.org/docs/batch-loading-specimen-images-2/>


# Meeting notes

To Do:
Data pushing
- iDigBio - best way to keep updated?, what is the script we were using? 
- Sernec - currently mapping? or static? 
  
List of barcodes per portal
- Re-organize 

Camera and computer software and updates

Incoming folder - NOT on home?

figure out hosting of images locally. 
set up pull, if time make a merge of all database and images. 


list of images to keep
resort nested folders 1000


# Projects:

## Other

Raw files to server, for backup 
Backup back down to local raid. 
Stamp copyright on JPGs?


## Imaging 

### Imagining and file naming

- need: barcoding softwear 
- lable image files based on software
- edit name of image file if barcode swiped twice. (check notes)
- uppercase LSU lowercase jpg
- do we need separate folders for each step? No
- check if barcodes have been scanned before. (mySQL db?)
- check for corruption? 

### Local storage and uploading

- record of all files imaged per day/week 
- stage for uploading. 
- store locally after(or before) uploading? 
- can we upload directly based on shared file structure of local and server? 

## Organize incoming images on server

- flexible to also pull CR files? CR is proprietary, turn into DNG or TIFF
- record of files pushed uploaded
- auto download to backup
- auto upload to portals
- check for corruption? 
- Incoming folder - NOT on home?

## Re-organize images on server

- need: list of barcodes for each portal
- need: bad image identifier
- Script to re- sort
- 1000 per folder
- folder by portal. 
- folder by lsu, no, nlu (flexibility in adding new folders)
- rename files to uppercase LSU, lowercase jpg. 


## mySQL database on server 

- keep database of image location, ID, portal
- date modified column? 
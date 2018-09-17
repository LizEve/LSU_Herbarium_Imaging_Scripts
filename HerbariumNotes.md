
# Open Refine

Catalogue number, LSU, 
other catalogue, LSU, other univ to match image. 

```python
# For locality, location ID, and LouisianaProtectedArea
# Edit cells > transform  > GREL
if(isBlank(value)," ",value)
# Open any column
# Edit column > Add column based on column > jython/python
import re

def col_to_list(column):
    # Split up the words in the cell into a list of words.
    colList = column.split()
    # Create a list with words only, no extra characters
    stripped=[re.sub('[,.();:]', '', x) for x in colList]
    # Make all things lowercase for simplier comparison
    stri=[x.lower() for x in stripped]
    return stri

# Assign each column/cell to a variable
# Also stripping off spaces and semicolons, so it is cleaner when we concatenate columns
column1 = cells['locationID']['value'].strip().strip(";").strip()
column2 = cells['locality']['value'].strip().strip(";").strip()
column3 = cells['LouisianaProtectedArea']['value'].strip().strip(";").strip()

# Use function to turn each cell into a string of lowercase words to compare
str1=col_to_list(column1)
str2=col_to_list(column2)
str3=col_to_list(column3)

# Replace unspecified columns with blanks. Use the string of the first item in the list to compare to the word 'unspecified'
if str(str1[0]) == 'unspecified':
    column1 = ' '
    str1 = [' ']

if str(str2[0]) == 'unspecified':
    column2 = ' '
    str2 = [' ']

# If all columns are blank. New column entry will be "unspecified"
if str(str1[0]) == str(str2[0]) == ' ':
    if str(str3[0]) == ' ':
        newCol = 'unspecified'
    # If column 3 has information. Use this information.
    elif str(str3[0]) != ' ':
        newCol = column3
# Now proceed with comparing columns
else:
    # Check if column1 is found in column2(preserving the order of words)
    is_1_in_2 = any(str1 == str2[i:i+len(str1)] for i in range(len(str2)))
    # If col1 *is* found in col2, use col2 going forward (naming it col1+2)
    if is_1_in_2:
        str12 = str2
        column12 = column2
    # If col1 is *not* in col2, concatenate col1 and col2 into col1+2
    else:
        str12 = str1 + str2
        column12 = column1 + "; " + column2
    # Now check the col1+2 for matches to col3
    is_3_in_12 = any(str3 == str12[i:i+len(str3)] for i in range(len(str12)))
    # If col3 is found in col1+2, use col1+2 going forward, ignoring col3
    if is_3_in_12:
        newCol = column12
    # If col3 is *not* in col1+2, add it.
    else:
        newCol = column12 + "; " + column3

# remove leading and trailing whitespace and semicolons a few times
newcolumn = newCol.strip().strip(";").strip()
return newcolumn
```

    # Try #1

```python
# edit cells > transform on locality and location ID - GREL
if(isBlank(value)," ",value)
# make a TF column. add column > edit column based on locality column
value.contains(cells["locationID"].value) 
# Create new locality col based on TF list col. 
if(value==false,cells["locality"].value + ", " + cells["locationID"].value,cells["locality"].value)
```

Issues:
- if locationID says unspecified, it tags that on the end of locality
- if locationID has a part that matches locality, but not all of it, still gets added on
- if there is spelling differences between locationID and locality, it adds it. 

    # Try #2
<https://groups.google.com/forum/#!topic/openrefine/qCnQTOfdHAA>

This does the same thing as try 1. 
```python
column1 = cells['locationID']['value']
column2 = cells['locality']['value']

if column1 in column2:
    return column2
else:
    return column2+", "+column1
```

    # Try #3 this works
<https://groups.google.com/forum/#!topic/openrefine/qCnQTOfdHAA>
<https://stackoverflow.com/questions/3900054/python-strip-multiple-characters>
Trying to modify try 2 to avoid pitfalls of try 1
https://stackoverflow.com/questions/8625351/check-if-two-items-are-in-a-list-in-a-particular-order
```python
import re

    def col_to_list(column):
    # Split up the words in the cell into a list of words.
    colList = column.split()
    # Create a list with words only, no extra characters
    stripped=[re.sub('[,.();:]', '', x) for x in colList]
    # Make all things lowercase for simplier comparison
    stri=[x.lower() for x in stripped]
    return stri

# Assign each column/cell to a variable
# Also stripping off spaces and semicolons, so it is cleaner when we concatenate columns
column1 = cells['locationID']['value'].strip().strip(";").strip()
column2 = cells['locality']['value'].strip().strip(";").strip()
column3 = cells['LouisianaProtectedArea']['value'].strip().strip(";").strip()

# Use function to turn each cell into a string of lowercase words to compare
str1=col_to_list(column1)
str2=col_to_list(column2)
str3=col_to_list(column3)

# Replace unspecified columns with blanks. Use the string of the first item in the list to compare to the word 'unspecified'
if str(str1[0]) == 'unspecified':
    column1 = ' '
    str1 = [' ']

if str(str2[0]) == 'unspecified':
    column2 = ' '
    str2 = [' ']

# If all columns are blank. New column entry will be "unspecified"
if str(str1[0]) == str(str2[0]) == ' ':
    if str(str3[0]) == ' ':
        newCol = 'unspecified'
    # If column 3 has information. Use this information.
    elif str(str3[0]) != ' ':
        newCol = column3
# Now proceed with comparing columns
else:
    # Check if column1 is found in column2(preserving the order of words)
    is_1_in_2 = any(str1 == str2[i:i+len(str1)] for i in range(len(str2)))
    # If col1 *is* found in col2, use col2 going forward (naming it col1+2)
    if is_1_in_2:
        str12 = str2
        column12 = column2
    # If col1 is *not* in col2, concatenate col1 and col2 into col1+2
    else:
        str12 = str1 + str2
        column12 = column1 + "; " + column2
    # Now check the col1+2 for matches to col3
    is_3_in_12 = any(str3 == str12[i:i+len(str3)] for i in range(len(str12)))
    # If col3 is found in col1+2, use col1+2 going forward, ignoring col3
    if is_3_in_12:
        newCol = column12
    # If col3 is *not* in col1+2, add it.
    else:
        newCol = column12 + "; " + column3

# remove leading and trailing whitespace and semicolons a few times
newcolumn = newCol.strip().strip(";").strip()
return newcolumn
```


```python
# Check if column1 is found in column2 in the order of column1
result = any(str1 == str2[i:i+len(str1)] for i in xrange(len(str2) - 1))

if result:
   return column2
else:
   return column1+'; '+column2


replace(value, 'unspecified', ' ')
if semicolon, trim

# Assign each column/cell to a variable
column1 = cells['locationID']['value']
column2 = cells['locality']['value']
column3 = cells['LouisianaProtectedArea']['value']
# Split up the words in the cell into a list of words.
colList1 = column1.split()
colList2 = column2.split()

# Create a list with words only, no extra characters
stripped1=[re.sub('[,.();:]', '', x) for x in colList1]
stripped2=[re.sub('[,.();:]', '', x) for x in colList2]

# Make all things lowercase for simplier comparison
str1=[x.lower() for x in stripped1]
str2=[x.lower() for x in stripped2]

# Check if str1 is equal to any number of items of str2 that is equal to str 1
result = any(str1 == str2[i:i+len(str1)] for i in xrange(len(str2) - 1))

if result:
   return column2
else:
   return column1+'; '+column2



x=[item for item in str2 if item in str1]
return x

#Are all elements in str1(named location/locationID) in str2(locality)? 
matching=all(elem in str2 for elem in str1)



if result:
    return column1+"; "+column2
else:
    return column2

# location ID = named place. List first. 
# location ID ; locality; louisiana protected area. 
# still need to account for case differences
# delete all unspecified from location ID. if unspecified and blank in locality, leave as unspecified.s
# probably want to use list not set comparison to preserve order of words
# geolocate

z=0
notInLocality=[]
for x in colList1:
    if x in colList2:
        z+=1
    else:
        notInLocality.append(x)
return notInLocality, colList1, colList2
#return len(colList1),z



if column1 in column2:
    return column2
else:
    return column2+", "+column1
```


#### Did not work

```python
ngramFingerprint(cells.column2.value) == ngramFingerprint(value)


cells["locationID"].value + " " + cells["locality"].value

if(cells["locationID"].value == cells["locality"].value, "Y", "N") 
#  this works, but i want to find if locationID is IN locality



if(isNonBlank(value.match(/your regex/),

if(value.match(/.*(\d{6})/.*,"y","n")) # returns any string of 6 digits
if(value.match(/(.*)(\d{6})/(.*),"y","n")) #returns before, 6 digs, and after.)

if(value.match(/.*(cells["locationID"].value)/.*,"y","n"))



if(
    isNonBlank(
        value.match(
            /.*(cells["locationID"].value)/.*
            )
            )
            ,value,"xx"
            )

(/(.*)(\d{6})(.*)/)
```

open in excel, as tsv, change number columns to text to preserve them. 
save as csv. 
open into openrefine as csv

# Host monster

Login: cyberfloralouisiana.com
PW: LAPlants#2015

data.cbfla click websites, go to files, click file manager. edit publichtml, 
looked through a lot. couldn't figure out where images insert on page is coming from. probably just from current clfa server. LAF is probably on old server. 

# Databases to and from

data.cyberflora 
- Host Monster. hosting website to search database. 
    - would be nice to edit, and eventually delete. 
- where is the physical server for this?
- images not loading, not a huge priority

Check host monster to see what I can do with it. 


Upload images to somewhere else. not the small harddrive. 
Current patch sorts, but doesnt talk to silverimage, on imaging workstation. 

How/what do we edit to change where the image input folder is? Is there one file to edit for this, or multiple?

Server: images.cyberfloralouisiana.com
User: silverimageftp
Password: h@n=dMan
Images Remote Path: incoming

Where was GA images going? - those are now funneled somewhere other than ours. 

/var/www/html
- where apache drops web directories. 
/etc/httpd/conf/httpd.conf <- says where to look on our server when pinged by a www.website.com
all dealt with by apache. 

data.cbfla click websites, go to files, click file manager. edit publichtml, index html. can edit pages to give warnings. 

LAF images on cbfl broken, not on server, but on main page website. might be able to track this down with website html see above. s

cbfla is hosting images

To Do
make list of to do what needs fixing. organize things. 
    - is there somewhere on data that talks to the incoming from images and image station computer? 
    - synology backups 
    - georgia


## Databases

Online Herbarium <http://data.cyberfloralouisiana.com/lsu/>
- Mike Giddens
- specify linked to barcodes
- main interface connecting images and specify
  
Lichen, Bryophyte, Fungi <http://www.herbarium.lsu.edu/>
- consortiums, symbiota based, lots of collections
- can search by collection
- public view and private view, backside, edit data. 
- we have duplicate photos for information that is up here. extra images are on iDigBio servers
- live interface with inputting data

iDigBio, iPlant
- has scripts to upload images. 

Sernec <http://sernecportal.org/portal/>
- southeastern plant herbaria
- Ed gilbert
- database, sybiota
- sending specify data here to keep updated and online. 
- want to be primary database for vascular plants ONLY 
- has backend synonomy help
- has lichen, bryophyte, fungi images, but not metadata
- planning to make this a live portal for entering data for vascular. then specify dies. 
- currently working as spreadsheets to upload. 
- to link images, can do one by one, or find a way to automatically grab from our server
    - not sure if small med large images are on our server or on sernec, think its on iDigBio server
  
CyberFlora
- server where all the images are
- older funded project. were all uploaded to sernec
- had a lot of other herbaria 

Specify
- on a different server

Local LaCie Drives
- locally images are sorted by type 
- server is all by barcode. 

Goals
- scan barcode and know what it is, barcode searcher, own metadatabase. 
- find some way to organize vacular, bryophyte, lichen, fungi. 
- find a way to link sernec symbiota metdata with images on cyberflora server, automatic pull of new images. 
- Archive raw files, currently just archiving jpeg
- Rebarcode everything or use old barcode, NO, NLS, LSU. 3 diff barcode systems. 
    - images already have barcode on it. 
    - currently set up under own folders, NO, NLS. 
    - all other institutions are vascular plants
- restructure server to reflect what specimens we have that used to be elsewhere. and which taxonomic group. 
- set it all up assuming there will be more collections coming in. 
- Do we need to completely restructure how data is being stored - ie mysql or can the upload process on it's own be fixed. 
- get online schematic of folders on server working again. 
- Setup image to saved workflow 

- print path to each filed pic 
- count unique lines in file - want counts of what got sorted
- chron jobs, run at night

- check out python pnw herbaria scripts.
- idig bio workflows for image collection. 
- how does symbiota intake image data and match to current database. 


image - server - up to symbiotia


# Meeting 2018-08-08
Jennie, Laura, Lyndon
chron job. fires up ftp something. ftps go into incoming directory. chron job executes php script, with frey webserver, where one of the final storage locations is, supposed to rename and store images. also links to online searchable database. 
incoming directory works, but won't organize. fills up folder and then can't take any more because its overflowing with unorganized files. 
so chron job of php something. says they are processing but they arent. 
Sernec
Silver image proprietary scripts that tie things together. 
Bug is hidden in java and php script. 
legally can't modify source code. 
node servers - need javascript engineer 
sqlite 

data management plan across institutions. dont leave giant zip files in a temp folder. 

symbiota

Some script on frey or silverimage webserver and isnt pulling images out of incoming folder. php script says its processing, but isnt. 
patch, symlink to bigger drive, but now that isnt working. 
likely a hard coded call to something, OS or some other software updates or changed, and now hard call is broken. - best guess by lyndon. 

open source alternitive to taking pics with data and uploading. silver whatever open source replacement. iDigBio would probably know. Ask Ento guy. 

any new scripts written - write a parameters file that is easy to change if needed. (ask lyndon later.)

cron job - scheduling utility

current setup on fry - nested folders based on ID number. 

sqldatabase with all images that arent used in online sernec
sql reader on desktop GUI - datagrip

plan out structure of database thoroughly. unique identifiers (two unique identifiers). what tables. what keys you want to use to search. location. think about future plans of what you want to add. 

natural history collection database architecture, sqlite. 

symbiota, write to personal database along with writing to symbiota. 

What I want to do:
- write out full pipelines of where things are input, where online searches are. where all the data are saved. 
- what are priorities, where do we want to start? 

What I need to do on my own:
Sqlite - download, learn. python uses. 
Set up some chron jobs locally for fun. can i connect sysco from terminal? 

Picture > silverimage software open, as soon as pic is barcoded, it shuffles photo around. > edit in digital image professional, 
scan barcode and attach to image. silverimage uses this. find open source. 
checks servers for barcodes to avoid duplication.

Jennie - m-f 9-3. 

#  Cron jobs
sudo less  /var/log/cron
Aug 24 12:38:31 cyberflora crond[13479]: (CRON) DEATH (can't open or create /var/run/crond.pid): Permission denied


Aug 19 03:43:03 cyberflora run-parts(/etc/cron.daily)[12098]: finished logrotate
Aug 19 03:43:03 cyberflora run-parts(/etc/cron.daily)[12037]: starting makewhatis.cron
Aug 19 03:43:04 cyberflora run-parts(/etc/cron.daily)[12256]: finished makewhatis.cron
Aug 19 03:43:04 cyberflora run-parts(/etc/cron.daily)[12037]: starting mlocate.cron
Aug 19 03:43:09 cyberflora run-parts(/etc/cron.daily)[12268]: finished mlocate.cron
Aug 19 03:43:09 cyberflora run-parts(/etc/cron.daily)[12037]: starting prelink
Aug 19 03:43:09 cyberflora run-parts(/etc/cron.daily)[12280]: finished prelink
Aug 19 03:43:09 cyberflora run-parts(/etc/cron.daily)[12037]: starting readahead.cron
Aug 19 03:43:09 cyberflora run-parts(/etc/cron.daily)[12292]: finished readahead.cron
Aug 19 03:43:09 cyberflora run-parts(/etc/cron.daily)[12037]: starting tmpwatch
Aug 19 03:43:09 cyberflora run-parts(/etc/cron.daily)[12330]: finished tmpwatch
Aug 19 23:01:01 cyberflora CROND[12617]: (root) CMD (run-parts /etc/cron.hourly)
Aug 19 23:01:01 cyberflora run-parts(/etc/cron.hourly)[12617]: starting 0anacron
Aug 19 23:01:01 cyberflora run-parts(/etc/cron.hourly)[12626]: finished 0anacron
Aug 20 01:01:01 cyberflora run-parts(/etc/cron.hourly)[12694]: finished 0anacron
Aug 20 01:05:01 cyberflora CROND[12697]: (root) CMD 

CMD (/usr/bin/php /var/www/protected/harvester_lsu/harvester.php)
CMD (/bin/sh /var/www/protected/download.sh)
CMD (/usr/bin/php /var/www/protected/harvester_ga/harvester.php)
CMD (/bin/sh /var/www/html/silvercollection/admin/api/update_georgi
a_data.sh)
CMD (/bin/sh /var/www/protected/checkforimages.sh)
CMD (/bin/sh /var/www/protected/processimages.sh)
CMD (/bin/sh /var/www/protected/sync_georgia_images.sh)
CMD (/bin/sh /var/www/protected/link_georgia_images.sh)
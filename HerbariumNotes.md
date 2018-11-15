# To Do:



cbfla
- set up rsync cron job for synology backup and zip of server info
- reorganize script
    - test on server in my home folder
    - test in LaCie
    - output csv for all different files with issues- corrupted, no image.
- script for collecting all leftover files with no portal, make list after all portals have been moved.
- script to make large files for all 

compare / record
- barcodes/files on lacie drives to cbfla 
- all images not moved, not in a portal
- all barcodes in more than one portal

sql database
- input from file reorg
- update with new files regularly (maybe from a list of new uploads?)
- output/update csv for each portal regularly. accesible for jennie

imaging centers
- reorganization lacie
    - run same script used on cbfla  
    - make sure to include CR images
- daily 
    - download sql from cbfla
    - move images from incoming to folders on lacie (make large files?)
    - rsync lacie to cbfla
    - upload CR to box
        - script to scrape all CR images and drop in box.com, by portal/barcode institution/some numbers only. 
- already barcoded checker script
    - open to run whenever imaging
    - keeps eyes on incoming folder, raises alert when any barcode matches barcode in sql db. 

Questions:
- make large images on LaCie or on cbfla? probably not on LaCie. Only on cbfla. 
- backup from LaCie to Cbfla after reorganize?
- LaCie, might not have all files, could have originals somewhere else. Or in duplicate folders on current laCie. 
- reorganizing script 
    - nfsshare/lsu/vascular/lsu/##/###/file.jpg OR nfsshare/vascular/lsu/##/###/file.jpg(this works)
    - Are we ingesting all of the images in no folder? yes, all vascular. also ulm. keep barcodes. 

- what if we need to move a barcode to a different portal after the fact? 
- add closing warning on websites. 
- get keys for herbarium
- box for CR, store directly from LaCie 
- ask eric about cycling drives, do we need more? 
- make notes about everything. records. 


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
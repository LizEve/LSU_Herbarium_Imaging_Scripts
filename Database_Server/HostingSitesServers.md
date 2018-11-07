
Mount synology on cblfa
/mnt/cflabkup/

on cbfla - 
mount //130.39.124.15/cflabkup -o username=cflabkup,password=tiger123 /mnt/cflabkup

/ect/fstab - has a line to re-mount after rebooting of system 

on synology - 
File Station 

google - 





Questions for Eric:
What is the difference between the images.cyberflora.com vs direct link to file? 
- can still use images.cbfla to point people to image paths 
What are the text files in the barcode folders?
- could be some script by m giddens that pulls info from specify database, post image upload. 
- something to do with giddens old scripts. dont need. 
in /var/www/html/, wtf is all this stuff? do we need to save it? does it save with pushes to synology?
- talk to jennie about it
- every once in a while, zip up html and store. once a month. 
is cyberfloralouisiana.com on host monster? Or hosted locally? 
- hostmonster 
- 301 redirect, google w hostmonster
- make sure NSF is mentioned in new pages? question for laura. 
What do we want to save to synology? everything? or only lsu? 
- currently only lsu, nlu, 0, no, LSU_herb.zip 
- ask jennie
How often should I rsync to synology? 
- weekly or daily. 


130.39.19.140 - server for all folders in /var/www/html/
images.cbfla.com/ - cblfa folder specifically. 

# Local image server
Symlink in /var/www/html/
`/var/www/html/images.cyberfloralouisiana.com/images/specimensheets -> /data_storage/nfsshare`
More symlinks
```bash
#ls -al /var/www/html/
bis_cfla -> /var/www/html/bis
bis_ga -> /var/www/html/bis
images.georgiaherbaria.org -> /data_storage/georgiaherbaria
www.georgiaherbaria.org -> /var/www/html/silvercollection
#ls -al /var/www/html/images
cfla -> /data_storage/cfla/
#ls -al /var/www/html/images.cyberfloralouisiana.com/
bis -> /var/www/html/bis
specify_backups -> /var/www/html/specify_backups
```

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

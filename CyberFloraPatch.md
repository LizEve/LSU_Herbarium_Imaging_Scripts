ssh gmount1@cyberflora.lsu.edu
cd /data_storage
/data_storage/nfsshare/lsu/0/
file "$(pwd -L)"
/data_storage/cfla/incoming: symbolic link to `/home/silverimageftp/incoming/'

Goals:
write script to put files into appropriate folders. 
set up chron job to run scripts at regular intervals. 
add step to script to make small, med, lrg jpeg files for each image

Steps:
copy sample of files, folders
+ fake files put into data_storage_fake/cfla/incoming
open an ipy notebook
+ CyberFloraPatch.ipynb
figure out how to parse name and sort into different files. 
+ figure out nesting system. 
- parse name 
- make nested folders based on name
grab files from incoming directory (not sure if sim links will be a problem)
output list of all files that got sorted and file paths for all. 
put into functions and main

Questions:
- do the photos always end with jpg? jpeg? pdf? CR in no folder?
- is no or lsu ever lowercasein the file name? 

Answers:
+ do we put no and lsus images into those folders? - yes
    - for no is it under 0 or under vas_plants? - vas_plants
+ do we want one count per barcode or per photo (_1 and _2)
    - both. number of folders created = number of barcodes. 
    - also good to have number of files total for file count comparisons. 


## Cron jobs:

http://www.adminschoice.com/crontab-quick-reference

Crontab (CRON TABle) is a file which contains the schedule of cron entries to be run and at specified times.
Cron job or cron schedule is a specific set of execution instructions specifing day, time and command to execute. crontab can have multiple execution statments.

crontab -e    Edit crontab file, or create one if it doesn’t already exist.
crontab -l    crontab list of cronjobs , display crontab file contents.
crontab -r    Remove your crontab file.
crontab -v    Display the last time you edited your crontab file. (This option is only available on a few systems.)

Testing on CyberFlora

```bash
export EDITOR=vim
sudo crontab -l

0 1 * * * /bin/sh /var/www/protected/specify_export.sh
40 0 * * * /bin/sh /var/www/protected/specify_update.sh
8 1 * * * /usr/bin/php /var/www/protected/harvester_ga/harvester.php
5 1 * * * /usr/bin/php /var/www/protected/harvester_lsu/harvester.php
5 1 * * * /bin/sh /var/www/protected/download.sh
10 1 * * * /bin/sh /var/www/html/silvercollection/admin/api/update_georgia_data.sh
20 1 * * * /bin/sh /var/www/protected/checkforimages.sh
30 1 * * * /bin/sh /var/www/protected/processimages.sh
40 1 * * * /bin/sh /var/www/protected/sync_georgia_images.sh
55 1 * * * /bin/sh /var/www/protected/link_georgia_images.sh

sudo crontab -e
# opens file to edit above text
less /var/spool/cron/root
# where this crontab file lives
sudo crontab -u root -l
# lists above info 
crontab -l
no crontab for gmount1
crontab -e 
50 * * * * ./test.sh
```

```bash
*     *     *   *    *        command-to-be-executed file-to-execute
-     -     -   -    -
|     |     |   |    |
|     |     |   |    +----- day of week (0 - 6) (Sunday=0)
|     |     |   +------- month (1 - 12)
|     |     +--------- day of        month (1 - 31)
|     +----------- hour (0 - 23)
+------------- min (0 - 59)
```



http://www.unixgeeks.org/security/newbie/unix/cron-1.html

##### Cron to do

test script to only print files TO move, but not moved files. 


rsync -avzure ssh --stats --progress /Users/ChatNoir/Projects/HerbariumRA/CyberFloraPatch.py gmount1@cyberflora.lsu.edu:/home/gmount1/




36 2 * * * /usr/bin/python /home/gmount1/CyberFloraPatch.py &>> /data_storage/cfla/incoming_logs_2018/Errors.log


###### Cyberflora patch testing

Crontab 

```bash
35 11 * * * /usr/bin/python /home/gmount1/CyberFloraPatch.py &>> /home/gmount1/ILOVECATS/testErrors.log
```

Small file list to test on
```bash
sudo cp /home/silverimageftp/incoming/LSU0019684* /data_storage/cfla/incomingTEST
LSU00196965.JPG
```ls

##### To DO

- get working - use test to also print files that already have folders and what is in those folders
    - run chron job to make sure logs are writing, and folders are appropriate. 
    - add in check if file already exists
    - set up def main
    - figure out permissions issue 
- test on small batch
- figure out sym folder issue moving files - should all work fine for now 

- number of files not matching what image station says are uploaded to incoming
- images.cyberfloralouisiana.com
    - silverimageftp
- output locally F:\Liches\output\
- blacked out files. 
localhost:300/index-debug.html?host=http://local&siPort=300&lang=en
- images not loading for lsu herbairum thinger online database. 

## Github account

```bash
cd /Users/ChatNoir/Projects/HerbariumRA
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/LizEve/HerbariumRA.git
git push -u origin master
git add *
git commit -a -m "$message"
git push
```

https://www.quora.com/What-does-git-remote-and-origin-mean
git remote
my computer - origin/master -> copy of remote
            - master -> local branch
            - not different branches, just different committs of same branch
fetch - updates origin/master
merge - merges origin/master with master
pull - fetch + merge

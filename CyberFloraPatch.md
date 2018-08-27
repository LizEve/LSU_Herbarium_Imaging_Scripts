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


Cron jobs:

http://www.adminschoice.com/crontab-quick-reference

Crontab (CRON TABle) is a file which contains the schedule of cron entries to be run and at specified times.
Cron job or cron schedule is a specific set of execution instructions specifing day, time and command to execute. crontab can have multiple execution statments.

crontab -e    Edit crontab file, or create one if it doesn’t already exist.
crontab -l    crontab list of cronjobs , display crontab file contents.
crontab -r    Remove your crontab file.
crontab -v    Display the last time you edited your crontab file. (This option is only available on a few systems.)



Github account

```bash
cd /Users/ChatNoir/Projects/HerbariumRA
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/LizEve/HerbariumRA.git
git push -u origin master
```

https://www.quora.com/What-does-git-remote-and-origin-mean
git remote
my computer - origin/master -> copy of remote
            - master -> local branch
            - not different branches, just different committs of same branch
fetch - updates origin/master
merge - merges origin/master with master
pull - fetch + merge

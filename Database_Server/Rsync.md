

# Updating synology


## Selective backup 
`rm -rf /mnt/cflabkup/nlu`
```bash
sudo zip --symlinks -r /data_storage/nfsshare/varwwwhtml.zip /var/www/html/
sudo rsync -avu /data_storage/nfsshare/incoming_logs_2018 /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/livingimages /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/lsu /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/LSU_herb\ 20110621\ 1439.zip /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/lsus /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/ltu /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/mcn /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/no /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/selu /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/sfrp /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/thib /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/tst /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/uslh /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/varwwwhtml.zip /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/vascular /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/website /mnt/cflabkup/
```

ran out of space. looking at how big folders are and prioritizing backups. 
Eric is looking into using box storage. issue is folder depth, only does 4 deep 
    box x/x/x/x/.jpg
- rack mounted storage?
- get another synology 6 tb drives new 
Jennie said to not backup nlu for now. it is backed up somewhere else 

680G	/data_storage/nfsshare/bad/
    679G	/data_storage/nfsshare/bad/laf - improperly named LAF images 
4.0K	/data_storage/nfsshare/HiJennie.txt
308K	/data_storage/nfsshare/incoming_logs_2018
7.3G	/data_storage/nfsshare/livingimages
1.2T	/data_storage/nfsshare/lsu
19M	    /data_storage/nfsshare/LSU_herb 20110621 1439.zip
84G	    /data_storage/nfsshare/lsus
859G	/data_storage/nfsshare/ltu
12G	    /data_storage/nfsshare/mcn
4.0T	/data_storage/nfsshare/nlu
4.3T	/data_storage/nfsshare/no
146G	/data_storage/nfsshare/selu
54G	    /data_storage/nfsshare/sfrp
224G	/data_storage/nfsshare/thib
1.5M	/data_storage/nfsshare/tst
74G	    /data_storage/nfsshare/uslh
4.7G	/data_storage/nfsshare/varwwwhtml.zip
0	/data_storage/nfsshare/vascular
22M	/data_storage/nfsshare/website

## General Rsync info 

https://www.computerhope.com/unix/rsync.htm
-a, --archive 	archive mode; equals -rlptgoD (no -H,-A,-X)
recurse into directories, copy symlinks as symlinks, preserve permissions, preserve modification times, preserve group, preserve owner, transfer character and block device files to the remote system to recreate these devices- no effect if the receiving rsync is not run as the super-user,transfer special files such as named sockets and fifos.

-n, --dry-run 	perform a trial run with no changes made


## Testing

```bash
sudo rsync -avu /data_storage/nfsshare/0/*  /mnt/cflabkup/0
sudo rsync -avu /data_storage/nfsshare/0  /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/bad  /mnt/cflabkup/
sudo rsync -avu /data_storage/nfsshare/incoming_logs_2018 /mnt/cflabkup/
```





- add to chron job
sudo rsync -avun /data_storage/nfsshare/* /mnt/cflabkup/

sudo zip --symlinks -r /data_storage/nfsshare/varwwwhtml.zip /var/www/html/
- working on it. 

To Do:
imaging computer to LaCie 
From LaCie to cbfla
SqlLite from cbfla to imaging computers
Synology RAID as cbfla backup
    + add as device to my cbfla 
    + test rysync code to update all files on synology
    - add ALL(not georgia) folders to synology
    - run, then set up as chron job

- find synology raid, and backup with rsync
	- 130.39.124.18 - lenovo
	- 130.39.124.15 - synology cflabkup tiger123			
- cbfla cenos 6.9, need cenos 7
- get synology raid working as proper backup 

rsync 
0  lsu  LSU_herb 20110621 1439.zip  nlu  no

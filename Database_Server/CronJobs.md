## Cron jobs:

```bash
20 2 * * * /bin/sh /home/gmount1/backup_to_synology.sh &>> /home/gmount1/backup_to_synology.log
45 23 * * * /bin/sh /home/gmount1/Move_incoming_log.sh &>> /home/gmount1/Move_incoming_log.log
59 23 * * * /usr/bin/python /home/gmount1/CyberFloraPatch.py &>> /data_storage/nfsshare/incoming_logs_2018/Errors.log
0 * * * * /bin/sh /home/gmount1/Move_incoming_files.sh &>> /home/gmount1/Move_incoming_files.log
30 * * * * /bin/sh /home/gmount1/Move_incoming_files.sh &>> /home/gmount1/Move_incoming_files.log
```

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

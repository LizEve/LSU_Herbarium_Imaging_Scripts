


```bash
sudo crontab -e
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
```
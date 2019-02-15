#!/bin/bash

rsync -avu /data_storage/nfsshare/incoming_logs_2018 /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/livingimages /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/lsu /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/LSU_herb\ 20110621\ 1439.zip /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/lsus /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/ltu /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/mcn /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/no /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/selu /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/sfrp /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/thib /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/tst /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/uslh /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/vascular /mnt/cflabkup/
rsync -avu /data_storage/nfsshare/website /mnt/cflabkup/
zip --symlinks -r /data_storage/nfsshare/varwwwhtml.zip /var/www/html/
rsync -avu /data_storage/nfsshare/varwwwhtml.zip /mnt/cflabkup/
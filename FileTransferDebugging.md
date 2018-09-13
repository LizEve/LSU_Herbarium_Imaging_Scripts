


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

#### download.sh
```bash
[gmount1@cyberflora home]$ ls
wget -q -O /var/www/html/images.cyberfloralouisiana.com/archives/dwca-lsu/lsu-mycoportal.zip 'http://mycoportal.org/portal/webservices/dwc/dwcapubhandler.php?collid=15';

wget -q -O /var/www/html/images.cyberfloralouisiana.com/archives/dwca-lsu/lsu-macroalgae.zip 'http://macroalgae.org/portal/webservices/dwc/dwcapubhandler.php?collid=23';

wget -q -O /var/www/html/images.cyberfloralouisiana.com/archives/dwca-lsu/lsu-lichenportal.zip 'http://lichenportal.org/portal/webservices/dwc/dwcapubhandler.php?collid=37';

wget -q -O /var/www/html/images.cyberfloralouisiana.com/archives/dwca-lsu/lsu-bryophyteportal.zip  'http://bryophyteportal.org/portal/webservices/dwc/dwcapubhandler.php?collid=18'
```

#### harvester_lsu/harvester.php

I think this has to do with specify. I didn't see anything that looked related to images

#### checkforimages.sh

```bash
wget -O /dev/null -o /dev/null  'http://bis.georgiaherbaria.org/resources/api/api.php?cmd=imageLoadFromIncoming&storageDeviceId=1';
wget -O /dev/null -o /dev/null  'http://images.cyberfloralouisiana.com/bis/resources/api/api.php?cmd=imageLoadFromIncoming&storageDeviceId=1';
```

Here -O sends the downloaded file to /dev/null and -o logs to /dev/null instead of stderr. That way redirection is not needed at all.
null device, which is a special device which discards the information written to it

https://www.codeofaninja.com/2017/02/create-simple-rest-api-in-php.html


#### processimages.sh

```bash
wget -O /dev/null -o /dev/null http://bis.georgiaherbaria.org/resources/api/api.php?cmd=processQueue
wget -O /dev/null -o /dev/null http://images.cyberfloralouisiana.com/bis/resources/api/api.php?cmd=processQueue
```

#### /home/silverbiology/node_modules/create-torrent
https://github.com/webtorrent/create-torrent/


## On workstation

### C:\SilverBiology\SilverImage

#### server.js

Mention of bis
    - 20 http://bis.silverbiology.com

Export Images function
    - 1144 '/exportImages'

#### silverimagepusher\silverimagepusher.js
looked, not sure if this is what i want

#### \static\resources\scripts\batchout.bat & sendtoserver.bat

C:\xampplite\php\php C:\xampplite\htdocs\silverimage\api\silverimage.php send-remote-images

#### 


To DO:
look into ftp settings
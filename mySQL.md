
# Installation

## Homebrew Install

```bash
brew install mysql
brew unlink mysql-connector-c
brew install mysql
brew services start mysql # I dont know what this did
#brew services start mysql - instruction is equal to :
#$ ln -sfv /usr/local/opt/mysql/*.plist ~/Library/LaunchAgents
#$ launchctl load ~/Library/LaunchAgents/homebrew.mxcl.mysql.plist
mysql_upgrade -u root
mysql_secure_installation
# pw = ilikeplants
# 0 Low security level
# n - remove anonymous useers
# y - no remote root login
# n - remove test db
3 y - reload privelege tables
```

## Install info

```bash
A CA file has been bootstrapped using certificates from the SystemRoots
keychain. To add additional certificates (e.g. the certificates added in
the System keychain), place .pem files in
  /usr/local/etc/openssl/certs

and run
  /usr/local/opt/openssl/bin/c_rehash

openssl is keg-only, which means it was not symlinked into /usr/local,
because Apple has deprecated use of OpenSSL in favor of its own TLS and crypto libraries.

If you need to have openssl first in your PATH run:
  echo 'export PATH="/usr/local/opt/openssl/bin:$PATH"' >> ~/.bash_profile

For compilers to find openssl you may need to set:
  export LDFLAGS="-L/usr/local/opt/openssl/lib"
  export CPPFLAGS="-I/usr/local/opt/openssl/include"

For pkg-config to find openssl you may need to set:
  export PKG_CONFIG_PATH="/usr/local/opt/openssl/lib/pkgconfig"

==> mysql
We've installed your MySQL database without a root password. To secure it run:
    mysql_secure_installation

MySQL is configured to only allow connections from localhost by default

To connect run:
    mysql -uroot

To have launchd start mysql now and restart at login:
  brew services start mysql
Or, if you don't want/need a background service you can just run:
  mysql.server start
```

# Experimenting

## User privileges

```bash
CREATE USER 'gmount'@'localhost' IDENTIFIED BY 'ilikecats';
GRANT ALL PRIVILEGES ON * . * TO 'gmount'@'localhost';
```

# Basics

```bash
mysql -u root -p
show databases;
```

## Playing

```bash
create database plants;
use plants
# or > mysql -u gmount -p plants
select database(); # check which one you using
create table bryophyte (barcode VARCHAR(11), 
museum VARCHAR(20), 
portal VARCHAR(20), 
imagepath VARCHAR(5000));
show tables;
describe bryophyte;
alter table bryophyte add column filename varchar(15) first;
alter table bryophyte add column universalid varchar(20) after portal;
drop table bryophyte;
source /Users/ChatNoir/Downloads/occurrences-csv.sql;
```

# Beginners guides

on page - <https://dev.mysql.com/doc/refman/8.0/en/date-calculations.html>

<https://www.elated.com/articles/mysql-for-absolute-beginners/>
<https://dev.mysql.com/doc/mysql-getting-started/en/>
<https://www.elated.com/articles/mysql-for-absolute-beginners/>

user permissions - <https://www.a2hosting.com/kb/developer-corner/mysql/managing-mysql-databases-and-users-from-the-command-line>
<https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql>


# Isolate data needed

occurances.csv

id, institutionCode,collectionCode,catalogNumber
UUID, LSU, Bryophyte, ID

Openrefine 
Export
SQL Exporter

Exports file. 

# Plans

Can import:
    id, - UUID
    institutionCode, - LSU/museum on ID
    collectionCode, - portal name
    catalogNumber - barcode
Want to add:
    file name (so each barcode will potentially have mult files with _1,2,3 etc)
    image path 

Goals:

Upload (daily) all new image info to symbiota/ all diff portals
Continually (daily) add image info, all info based on location of files (not sure how ill import this info yet)
While imaging, check scanned barcode against current db of barcodes. raise error if already exists. Access via server, or DL database locally, at beginning of day. 

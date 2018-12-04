
test
in list
not in list
lower case file name
corrupted file (?)

# Set up subset of files in file structure to test
LSU00000033
LSU00000044
LSU00000055
LSU00000088
LSU00077777
LSU00022222
NO0110111
NO0022022
NO0033003
NO0044004
NLU0043454
NLU0058322

```bash
mkdir -p /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/33/
cp /data_storage/nfsshare/lsu/0/0/0/33/LSU00000033* /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/33/

mkdir -p /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/44/
cp /data_storage/nfsshare/lsu/0/0/0/44/LSU00000044* /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/44/

mkdir -p /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/55/
cp /data_storage/nfsshare/lsu/0/0/0/55/LSU00000055* /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/55/

mkdir -p /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/88/
cp /data_storage/nfsshare/lsu/0/0/0/88/LSU00000088* /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/88/

mkdir -p /home/gmount1/data_storage_fake/nfsshare/lsu/0/7/77/77/
cp /data_storage/nfsshare/lsu/0/7/77/77/LSU00077777* /home/gmount1/data_storage_fake/nfsshare/lsu/0/7/77/77/

mkdir -p /home/gmount1/data_storage_fake/nfsshare/lsu/0/2/22/22/
cp /data_storage/nfsshare/lsu/0/2/22/22/LSU00022222* /home/gmount1/data_storage_fake/nfsshare/lsu/0/2/22/22/

mkdir -p /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/11/1/11
cp /data_storage/nfsshare/no/vas_plants/0/11/1/11/NO0110111* /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/11/1/11

mkdir -p /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/2/20/22
cp /data_storage/nfsshare/no/vas_plants/0/2/20/22/NO0022022* /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/2/20/22

mkdir -p /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/3/30/3
cp /data_storage/nfsshare/no/vas_plants/0/3/30/3/NO0033003* /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/3/30/3

mkdir -p /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/4/40/4
cp /data_storage/nfsshare/no/vas_plants/0/4/40/4/NO0044004* /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/4/40/4

mkdir -p /home/gmount1/data_storage_fake/nfsshare/nlu/0/4/34/54/
cp /data_storage/nfsshare/nlu/0/4/34/54/NLU0043454* /home/gmount1/data_storage_fake/nfsshare/nlu/0/4/34/54/

mkdir -p /home/gmount1/data_storage_fake/nfsshare/nlu/0/5/83/22/
cp /data_storage/nfsshare/nlu/0/5/83/22/NLU0058322* /home/gmount1/data_storage_fake/nfsshare/nlu/0/5/83/22/

rm /home/gmount1/data_storage_fake/nfsshare/lsu/0/0/0/44/*_l*
rm /home/gmount1/data_storage_fake/nfsshare/lsu/0/7/77/77/*_l*
rm /home/gmount1/data_storage_fake/nfsshare/no/vas_plants/0/3/30/3/*_l*
```

## Occurance file

occurrencesfakecbfla.csv
**Not** in portal list: LSU00000088, LSU00000055, NO0044004
**No** image: LSU00066666, LSU00099999, NO0055055
**No** large: LSU00000044, LSU00077777, all NO images  
**corrupt**: NLU0043454

## Copy files to cbfla

`rsync -avzure ssh --stats --progress /Users/ChatNoir/Projects/HerbariumRA/Scripts/Database_Server gmount1@cyberflora.lsu.edu:/home/gmount1/`

# Import python packages

**ImportError: No module named pathlib2**

```bash
<https://www.tecmint.com/install-pip-in-linux/>
#sudo
yum install epel-release
yum install python-pip
pip install pathlib2
pip install --upgrade setuptools
pip install Pillow
# broken
ImportError: No module named sysconfig
```

Long talk with Eric, ended up installing python2.7 locally in his home dir. I can call it using python2.7. Associated pip with this python. Will specifically call this python for everything. Need to sudo to install python packages via pip. 

```bash
sudo su 
python2.7 -m pip install
su gmount1
```

```bash
python2.7 -m pip install pandas
```

## Fixing Bugs

`python2.7 Database_Server/ReOrganizeFiles.py`

### Files

Should not move
LSU00066666 - no image
LSU00099999 - no image
NO0055055 - no image
NO0044004 - not listed
LSU00000055 - not listed
LSU00000088 - not listed

Should move
NLU0043454 - corrupted
LSU00000044 - no large
LSU00077777 - no large
NO0110111 - no large
NO0022022 - no large
NO0033003 - no large

LSU00022222
LSU00000033
NLU0058322

**Not** in portal list: LSU00000088, LSU00000055, NO0044004
**No** image: LSU00066666, LSU00099999, NO0055055
**No** large: LSU00000044, LSU00077777, all NO images  
**corrupt**: NLU0043454


### Results 1
#### Corrupt
NO0033003.CR2,
NLU0043454.JPG,
NO0022022.CR2,
NO0110111.CR2,
Notes: CR files looks fine 
<http://images.cyberfloralouisiana.com/images/specimensheets/no/vas_plants/0/4/40/4/NO0044004.CR2>

#### No Large
Notes: Same as corrupt output. I think the CR files messed with the barcode dictionary. 

#### No Images
Notes: also same, as other two. may have an output issue

#### Check LSU folder
all the listed files 

### Changes 1
To Do:
+ add CR2 to "no" list of file names w s, m, etc. 
+ check output lists 
- `data_storage_fake/nfsshare/vascular/vascular/` one too many vasculars
- no large files got moved
- add more print statements for each step
  

Reset 
`rm -rf data_storage_fake/nfsshare/vascular/`

`python2.7 Database_Server/ReOrganizeFiles.py`

### Results 2
#### Corrupt
NLU0043454.JPG, +
Yay worked

#### No Large
LSU00000044.JPG, +
LSU00000033.JPG, -
LSU00077777.JPG, +
NLU0043454.JPG, -
LSU00022222.JPG, -
NO0033003.JPG, +
NO0022022.JPG, +
NO0110111.JPG, +
NLU0058322.JPG, -

None of the larges seem to be moving

#### No Images
LSU00099999,vascular +
LSU00066666,vascular +
NO0055055,vascular +
Yay worked

#### Files Moved
|File|barcode|portal|newpath|
|-|-|-|-|
|LSU00000044.JPG|LSU00000044|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/LSU/00/000/LSU00000044.JPG|
|LSU00000033.JPG|LSU00000033|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/LSU/00/000/LSU00000033.JPG|
|LSU00077777.JPG|LSU00077777|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/LSU/00/077/LSU00077777.JPG|
|NLU0043454.JPG|NLU0043454|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/NLU/0/043/NLU0043454.JPG|
|LSU00022222.JPG|LSU00022222|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/LSU/00/022/LSU00022222.JPG|
|NO0033003.JPG|NO0033003|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/NO/0/033/NO0033003.JPG|
|NO0022022.JPG|NO0022022|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/NO/0/022/NO0022022.JPG|
|NO0110111.JPG|NO0110111|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/NO/0/110/NO0110111.JPG|
|NLU0058322.JPG|NLU0058322|vascular|/home/gmount1/data_storage_fake/nfsshare/vascular/NLU/0/058/NLU0058322.JPG|

Should move
NLU0043454 - corrupted
LSU00000044 - no large
LSU00077777 - no large
NO0110111 - no large
NO0022022 - no large
NO0033003 - no large

LSU00022222
LSU00000033
NLU0058322

### Changes 2
- Fix large files moving issue. 

### Results 3 - WORKED 


## Update Output for easy gut check

- updating output
- print # files in occurances, and # files moved, # files no image, # files corrupted, # files no large. 


Reset 
`rm -rf data_storage_fake/nfsshare/vascular/`

`python2.7 Database_Server/ReOrganizeFiles.py`
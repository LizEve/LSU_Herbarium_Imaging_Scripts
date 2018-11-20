
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
NOT in portal list: LSU00000088, LSU00000055, NO0044004
NO image: LSU00066666, LSU00099999, NO0055055
NO large: LSU00000044, LSU00077777, all NO images  
corrupt: NLU0043454

## Copy files to cbfla

`rsync -avzure ssh --stats --progress /Users/ChatNoir/Projects/HerbariumRA/Scripts/Database_Server gmount1@cyberflora.lsu.edu:/home/gmount1/`
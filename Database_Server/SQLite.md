
Needed format for uploading to portals 

|output_order	|Catalog Number	|Image File Name	|Group	|originalurl|originalurl|
|--|--|--|--|--|--|
|1	|LSU00000164	|LSU00000164.jpg	|Vascular	|http://images.cyberfloralouisiana.com/images/specimensheets/lsu/0/0/1/64/LSU00000164.jpg	| http://images.cyberfloralouisiana.com/images/specimensheets/lsu/0/0/1/64/LSU00000164_l.jpg

CSV output for sql ingestion 

|Image File Name | Catalog Number | Group | Path List |
|--|--|--|--|--|

sql 
Table for each portal
if size becomes issue, could use formula for paths. 
write out URL list based on Path info. 
|Image File Name | Catalog Number |Group | Path List | URL List|
|--|--|--|--|--|

# Plans

Goals:

Upload (daily) all new image info to symbiota/ all diff portals
Continually (daily) add image info, all info based on location of files (not sure how ill import this info yet)
While imaging, check scanned barcode against current db of barcodes. raise error if already exists. Access via server, or DL database locally, at beginning of day. 

Ideas:
each portal with own table. 

SqLite
- local 
- need to output csv file 
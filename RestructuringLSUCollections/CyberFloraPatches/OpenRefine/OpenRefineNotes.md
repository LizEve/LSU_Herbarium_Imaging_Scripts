# Open Refine

Catalogue number, LSU, 
other catalogue, LSU, other univ to match image. 

```python
# For locality, location ID, and LouisianaProtectedArea
# Edit cells > transform  > GREL
if(isBlank(value)," ",value)
# Open any column
# Edit column > Add column based on column > jython/python
import re

def col_to_list(column):
    # Split up the words in the cell into a list of words.
    colList = column.split()
    # Create a list with words only, no extra characters
    stripped=[re.sub('[,.();:]', '', x) for x in colList]
    # Make all things lowercase for simplier comparison
    stri=[x.lower() for x in stripped]
    return stri

# Assign each column/cell to a variable
# Also stripping off spaces and semicolons, so it is cleaner when we concatenate columns
column1 = cells['locationID']['value'].strip().strip(";").strip()
column2 = cells['locality']['value'].strip().strip(";").strip()
column3 = cells['LouisianaProtectedArea']['value'].strip().strip(";").strip()

# Use function to turn each cell into a string of lowercase words to compare
str1=col_to_list(column1)
str2=col_to_list(column2)
str3=col_to_list(column3)

# Replace unspecified columns with blanks. Use the string of the first item in the list to compare to the word 'unspecified'
if str(str1[0]) == 'unspecified':
    column1 = ' '
    str1 = [' ']

if str(str2[0]) == 'unspecified':
    column2 = ' '
    str2 = [' ']

# If all columns are blank. New column entry will be "unspecified"
if str(str1[0]) == str(str2[0]) == ' ':
    if str(str3[0]) == ' ':
        newCol = 'unspecified'
    # If column 3 has information. Use this information.
    elif str(str3[0]) != ' ':
        newCol = column3
# Now proceed with comparing columns
else:
    # Check if column1 is found in column2(preserving the order of words)
    is_1_in_2 = any(str1 == str2[i:i+len(str1)] for i in range(len(str2)))
    # If col1 *is* found in col2, use col2 going forward (naming it col1+2)
    if is_1_in_2:
        str12 = str2
        column12 = column2
    # If col1 is *not* in col2, concatenate col1 and col2 into col1+2
    else:
        str12 = str1 + str2
        column12 = column1 + "; " + column2
    # Now check the col1+2 for matches to col3
    is_3_in_12 = any(str3 == str12[i:i+len(str3)] for i in range(len(str12)))
    # If col3 is found in col1+2, use col1+2 going forward, ignoring col3
    if is_3_in_12:
        newCol = column12
    # If col3 is *not* in col1+2, add it.
    else:
        newCol = column12 + "; " + column3

# remove leading and trailing whitespace and semicolons a few times
newcolumn = newCol.strip().strip(";").strip()
return newcolumn
```

    # Try #1

```python
# edit cells > transform on locality and location ID - GREL
if(isBlank(value)," ",value)
# make a TF column. add column > edit column based on locality column
value.contains(cells["locationID"].value) 
# Create new locality col based on TF list col. 
if(value==false,cells["locality"].value + ", " + cells["locationID"].value,cells["locality"].value)
```

Issues:
- if locationID says unspecified, it tags that on the end of locality
- if locationID has a part that matches locality, but not all of it, still gets added on
- if there is spelling differences between locationID and locality, it adds it. 

    # Try #2
<https://groups.google.com/forum/#!topic/openrefine/qCnQTOfdHAA>

This does the same thing as try 1. 
```python
column1 = cells['locationID']['value']
column2 = cells['locality']['value']

if column1 in column2:
    return column2
else:
    return column2+", "+column1
```

    # Try #3 this works
<https://groups.google.com/forum/#!topic/openrefine/qCnQTOfdHAA>
<https://stackoverflow.com/questions/3900054/python-strip-multiple-characters>
Trying to modify try 2 to avoid pitfalls of try 1
https://stackoverflow.com/questions/8625351/check-if-two-items-are-in-a-list-in-a-particular-order
```python
import re

    def col_to_list(column):
    # Split up the words in the cell into a list of words.
    colList = column.split()
    # Create a list with words only, no extra characters
    stripped=[re.sub('[,.();:]', '', x) for x in colList]
    # Make all things lowercase for simplier comparison
    stri=[x.lower() for x in stripped]
    return stri

# Assign each column/cell to a variable
# Also stripping off spaces and semicolons, so it is cleaner when we concatenate columns
column1 = cells['locationID']['value'].strip().strip(";").strip()
column2 = cells['locality']['value'].strip().strip(";").strip()
column3 = cells['LouisianaProtectedArea']['value'].strip().strip(";").strip()

# Use function to turn each cell into a string of lowercase words to compare
str1=col_to_list(column1)
str2=col_to_list(column2)
str3=col_to_list(column3)

# Replace unspecified columns with blanks. Use the string of the first item in the list to compare to the word 'unspecified'
if str(str1[0]) == 'unspecified':
    column1 = ' '
    str1 = [' ']

if str(str2[0]) == 'unspecified':
    column2 = ' '
    str2 = [' ']

# If all columns are blank. New column entry will be "unspecified"
if str(str1[0]) == str(str2[0]) == ' ':
    if str(str3[0]) == ' ':
        newCol = 'unspecified'
    # If column 3 has information. Use this information.
    elif str(str3[0]) != ' ':
        newCol = column3
# Now proceed with comparing columns
else:
    # Check if column1 is found in column2(preserving the order of words)
    is_1_in_2 = any(str1 == str2[i:i+len(str1)] for i in range(len(str2)))
    # If col1 *is* found in col2, use col2 going forward (naming it col1+2)
    if is_1_in_2:
        str12 = str2
        column12 = column2
    # If col1 is *not* in col2, concatenate col1 and col2 into col1+2
    else:
        str12 = str1 + str2
        column12 = column1 + "; " + column2
    # Now check the col1+2 for matches to col3
    is_3_in_12 = any(str3 == str12[i:i+len(str3)] for i in range(len(str12)))
    # If col3 is found in col1+2, use col1+2 going forward, ignoring col3
    if is_3_in_12:
        newCol = column12
    # If col3 is *not* in col1+2, add it.
    else:
        newCol = column12 + "; " + column3

# remove leading and trailing whitespace and semicolons a few times
newcolumn = newCol.strip().strip(";").strip()
return newcolumn
```


```python
# Check if column1 is found in column2 in the order of column1
result = any(str1 == str2[i:i+len(str1)] for i in xrange(len(str2) - 1))

if result:
   return column2
else:
   return column1+'; '+column2


replace(value, 'unspecified', ' ')
if semicolon, trim

# Assign each column/cell to a variable
column1 = cells['locationID']['value']
column2 = cells['locality']['value']
column3 = cells['LouisianaProtectedArea']['value']
# Split up the words in the cell into a list of words.
colList1 = column1.split()
colList2 = column2.split()

# Create a list with words only, no extra characters
stripped1=[re.sub('[,.();:]', '', x) for x in colList1]
stripped2=[re.sub('[,.();:]', '', x) for x in colList2]

# Make all things lowercase for simplier comparison
str1=[x.lower() for x in stripped1]
str2=[x.lower() for x in stripped2]

# Check if str1 is equal to any number of items of str2 that is equal to str 1
result = any(str1 == str2[i:i+len(str1)] for i in xrange(len(str2) - 1))

if result:
   return column2
else:
   return column1+'; '+column2



x=[item for item in str2 if item in str1]
return x

#Are all elements in str1(named location/locationID) in str2(locality)? 
matching=all(elem in str2 for elem in str1)



if result:
    return column1+"; "+column2
else:
    return column2

# location ID = named place. List first. 
# location ID ; locality; louisiana protected area. 
# still need to account for case differences
# delete all unspecified from location ID. if unspecified and blank in locality, leave as unspecified.s
# probably want to use list not set comparison to preserve order of words
# geolocate

z=0
notInLocality=[]
for x in colList1:
    if x in colList2:
        z+=1
    else:
        notInLocality.append(x)
return notInLocality, colList1, colList2
#return len(colList1),z



if column1 in column2:
    return column2
else:
    return column2+", "+column1
```


#### Did not work

```python
ngramFingerprint(cells.column2.value) == ngramFingerprint(value)


cells["locationID"].value + " " + cells["locality"].value

if(cells["locationID"].value == cells["locality"].value, "Y", "N") 
#  this works, but i want to find if locationID is IN locality



if(isNonBlank(value.match(/your regex/),

if(value.match(/.*(\d{6})/.*,"y","n")) # returns any string of 6 digits
if(value.match(/(.*)(\d{6})/(.*),"y","n")) #returns before, 6 digs, and after.)

if(value.match(/.*(cells["locationID"].value)/.*,"y","n"))



if(
    isNonBlank(
        value.match(
            /.*(cells["locationID"].value)/.*
            )
            )
            ,value,"xx"
            )

(/(.*)(\d{6})(.*)/)
```

open in excel, as tsv, change number columns to text to preserve them. 
save as csv. 
open into openrefine as csv
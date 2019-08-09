import sqlite3

conn = sqlite3.connect('TestDB.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved


# The [generated_id] column is used to set an auto-increment ID for each record
# filename:[barcode, portal, date, current(new) path]
# Algae  Bryophyte  Fungi  Lichen  Vascular NoPortal
# Create tables
c.execute('''CREATE TABLE ALGAE
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE BRYOPHYTE
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE FUNGI
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE LICHEN
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE VASCULAR
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE NOPORTAL
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Date] text,[File_Path] text)''')
          
conn.commit()


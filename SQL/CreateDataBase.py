import sqlite3
import pandas as pd
from pandas import DataFrame


conn = sqlite3.connect('TestDB.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor() # The database will be saved in the location where your 'py' file is saved


# The [generated_id] column is used to set an auto-increment ID for each record
# filename, 'Barcode_ID','Portal','Collection_Code', 'Date','File_Path'
# Algae  Bryophyte  Fungi  Lichen  Vascular NoPortal
# Create tables
# c.execute passes commands to sql
c.execute('''CREATE TABLE ALGAE
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Collection_Code] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE BRYOPHYTE
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Collection_Code] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE FUNGI
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Collection_Code] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE LICHEN
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Collection_Code] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE VASCULAR
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Collection_Code] text, [Date] text,[File_Path] text)''')
          
c.execute('''CREATE TABLE NOPORTAL
             ([generated_id] INTEGER PRIMARY KEY,[File_Name] text, [Barcode_ID] text, [Portal] text, [Collection_Code] text, [Date] text,[File_Path] text)''')
            
 # Save (commit) the changes          
conn.commit()

# When reading the csv:
# - Place 'r' before the path string to read any special characters, such as '\'
# - Don't forget to put the file name at the end of the path + '.csv'
# - Before running the code, make sure that the column names in the CSV files match with the column names in the tables created and in the query below
# - If needed make sure that all the columns are in a TEXT format

# Import the CSV files using the read_csv command
read_algae = pd.read_csv (r'/Users/ChatNoir/Projects/HerbariumRA/Scripts/SQL/temp_Algae_Aug09.csv')

# Assign the values imported from the CSV files into the tables using the to_sql command
read_algae.to_sql('ALGAE', conn, if_exists='append', index = False) # Insert the values from the csv file into the table 'CLIENTS' 

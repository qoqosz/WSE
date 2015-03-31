#!/usr/bin/python
import sqlite3, os.path

# Create database file
db_filename = "baza.db"

if os.path.isfile(db_filename):
	print("File {0} already exists.").format(db_filename)
	quit()

conn = sqlite3.connect(db_filename)
curs = conn.cursor()

# Create table structure
# historical - table with historical stock data
curs.execute('''CREATE TABLE historical(
	Id 				INTEGER NOT NULL,
	Date 			TEXT NOT NULL,
	Open 			REAL,
	Close 			REAL,
	Min 			REAL,
	Max 			REAL,
	MaturityPeriod 	INTEGER,
	UNIQUE (Id, Date)
);''')
# curves - connect Id with proper instrument
curs.execute('''CREATE TABLE curve(
	Id 				INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	Identifier 		TEXT NOT NULL,
	Name 			TEXT,
	UNIQUE(Identifier)
);''')
# Save & Close DB
conn.commit()
conn.close()

# Create data/ subfolder
if not os.path.exists("data"): 
	os.makedirs("data")

print "Setup done."
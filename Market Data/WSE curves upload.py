#!/usr/bin/python
import csv, sqlite3

filename = raw_input("File with ticker data: ")

data = list()
with open(filename, 'r') as csvfile:
	rows = csv.reader(csvfile, delimiter = ',')
	for row in rows:
		data.append((row[0], row[1]))

conn = sqlite3.connect("../baza.db")
curs = conn.cursor()
curs.executemany('''INSERT OR IGNORE INTO curve(Identifier, Name)
					VALUES(?, ?)''', data)
conn.commit()
conn.close()

print 'Done'
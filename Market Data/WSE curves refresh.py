#!/usr/bin/python
import csv, sqlite3
from download_data import StockUpdate

filename = raw_input("File with WSE tickers to update: ")

ticker_list = list()
with open(filename, 'r') as csvfile:
	rows = csv.reader(csvfile, delimiter = ',')
	for row in rows:
		ticker_list.append((row[0]))

curve_ids = list()
conn = sqlite3.connect("../baza.db")
curs = conn.cursor()

for ticker in ticker_list:
	curs.execute("SELECT Id FROM curve WHERE Identifier = ?", [ticker])
	curve_ids.append(curs.fetchone()[0])

conn.close()

stocks = StockUpdate("../baza.db", "../data", ticker_list, curve_ids)
stocks.run()

print 'Done'
#!/usr/bin/python
import argparse
import os, sys, csv, sqlite3, datetime, urllib

class StockUpdate:
	def __init__(self, db_name, folder, tkr_list, id_list):
		self.db_name 	= db_name
		self.folder 	= folder + ('' if folder[-1] == '/' else '/')
		self.tkr_list 	= tkr_list
		self.id_list 	= id_list

	def run(self):
		for ticker, cid in zip(self.tkr_list, self.id_list):
			print("Updating " + ticker.rstrip())
			self._update(ticker, cid)

	def _download(self, ticker):
		type = "SHARE"
		if (ticker == "WIG" or ticker == "WIG20"):
			type = "INDEX"
		url = "http://xml.wyborcza.biz/ArchivalProfileExportServlet.servlet?p5=" \
			+ ticker + "&p6=2013-12-01&p7=" \
			+ datetime.datetime.today().strftime("%Y-%m-%d") \
			+ "&p8=1&p3=CSV&type=" + type
		urllib.urlretrieve(url, self.folder + ticker + ".csv")

	def _convertFile(self, ticker):
		filename = ticker + ".csv"
		tmpfilename = "tmp_" + filename

		open(self.folder + tmpfilename, 'a').close()

		i = 0

		with open(self.folder + tmpfilename, "wt") as fout:
			with open(self.folder + filename, "rt") as fin:
				for line in fin:
					if i != 0:
						line = line.replace(',', '.')
						fout.write(line.replace(';', ','))
					i = i + 1

		os.remove(self.folder + filename)
		os.rename(self.folder + tmpfilename, self.folder + filename)

	def _readFile(self, ticker, cid):
		data = list()
		filename = ticker + ".csv"

		with open(self.folder + filename) as csvfile:
			rows = csv.reader(csvfile, delimiter = ',')

			for row in rows:
				data.append((cid, row[6], row[0], row[3], row[2], row[1]))
		return data

	def _updateDB(self, data):
		conn = sqlite3.connect(self.db_name)
		curs = conn.cursor()
		curs.executemany('INSERT OR REPLACE INTO historical' \
						+ ' VALUES (?,?,?,?,?,?,0)', data)
		conn.commit()
		conn.close()

	def _update(self, ticker, cid):
		self._download(ticker)
		self._convertFile(ticker)
		self._updateDB(self._readFile(ticker, cid))

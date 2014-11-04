#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import csv
from config import *

db = MySQLdb.connect( host   = DB_HOST   ,
                      user   = DB_USER   ,
                      passwd = DB_PASSWD ,
                      db     = DB_NAME    )
cur = db.cursor()

csvfile = "test.csv"
inputFile  = open( csvfile, "rb" )
reader = csv.reader(inputFile)

table = "srcSTACK"
if table == "srcSDSS" :
	columns = "`id`,`run`,`col`,`field`,`ra`,`dec`,`u`,`g`,`r`,`i`,`z`"
elif table == "srcSTACK" :
	columns = "`id`,`run`,`col`,`field`,`filter`,`ra`,`dec`,`mag`"

i=0
# file browse
for row in reader :
	if i == 0 :
		i = 1
	else :
		values = ""
		for i in row:
			values += i + ","
		#print( "INSERT INTO " + table + " (" + columns + ") VALUES(" + values[:-1] + ");" )
		cur.execute( "INSERT INTO " + table + " (" + columns + ") VALUES(" + values[:-1] + ");" )

inputFile.close()

# print all the first cell of all the rows
#for row in cur.fetchall() :
#	print row[0]

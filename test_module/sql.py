#!/usr/bin/env pythons
import pymysql

# Open database connection
db = pymysql.connect("localhost","root","","login" )

# prepare a cursor object using cursor() method
cursor = db.cursor()
sql = "INSERT INTO users(username, password, id) VALUES ('Mohan', 'Mohan',  NULL)"
cursor.execute(sql)
print ("Sucess!!")
# disconnect from server
db.close()

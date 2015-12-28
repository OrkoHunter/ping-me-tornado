#!/usr/bin/env python
import os
import datetime
import torndb

options = {
    'mysql_host' : os.environ['OPENSHIFT_MYSQL_DB_HOST'],
    'mysql_database' : 'ping_me',
    'mysql_user' : os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
    'mysql_password' : os.environ['OPENSHIFT_MYSQL_DB_PASSWORD']
}

DB = torndb.Connection(
            host=options['mysql_host'], database=options['mysql_database'],
            user=options['mysql_user'], password=options['mysql_password'])

q = DB.query("SELECT * FROM messages ORDER BY ping_datetime;")

t = datetime.datetime.now()

for i in q:
    if i['ping_datetime'] < t:
        DB.execute("DELETE FROM messages WHERE email = '" + i['email'] + "' AND ping_datetime = '" + i['ping_datetime'].strftime("%Y-%m-%d %H:%M:00") + "';")

DB.close()

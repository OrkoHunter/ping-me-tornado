import MySQLdb as mdb
import os
import sys

con = mdb.connect(os.environ['OPENSHIFT_MYSQL_DB_HOST'],
                  os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
                  os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
                  'ping_me')

def _user_exists(email, phone='0'):
    with con:
        cur = con.cursor()
        no = cur.execute("SELECT * FROM users WHERE email = '" + email + "' OR phone='" + phone + "';")
        if no:
            return True
        else:
            return False

def _authenticate(email, hashed_pass):
    with con:
        cur = con.cursor()
        no = cur.execute("SELECT * FROM users WHERE email = '" + email + "' AND password='" + hashed_pass + "';")
        if no:
            return True
        else:
            return False

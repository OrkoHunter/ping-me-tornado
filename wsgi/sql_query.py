import MySQLdb as mdb
import os
import sys

def _user_exists(email, phone='0'):
    con = mdb.connect(os.environ['OPENSHIFT_MYSQL_DB_HOST'],
                      os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
                      os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
                      'ping_me')

    with con:
        cur = con.cursor()
        no = cur.execute("SELECT * FROM users WHERE email = '" + email + "' OR phone='" + phone + "';")
        if no:
            return True
        else:
            return False

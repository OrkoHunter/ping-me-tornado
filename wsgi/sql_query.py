import MySQLdb as mdb
import sys

def _user_exists(email, phone='0'):
    con = mdb.connect('localhost', 'adminkQ5IJBY', 'KlY1A-hSfgXU', 'ping_me')

    with con:
        cur = con.cursor()
        no = cur.execute("SELECT * FROM users WHERE email = '" + email + "' OR phone='" + phone + "';")
        if no:
            return True
        else:
            return False

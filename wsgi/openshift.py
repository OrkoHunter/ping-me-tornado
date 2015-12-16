#!/usr/bin/env python
import os
import tornado.web
import torndb

import sql_query

options = {
    'mysql_host' : os.environ['OPENSHIFT_MYSQL_DB_HOST'],
    'mysql_database' : 'ping_me',
    'mysql_user' : os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
    'mysql_password' : os.environ['OPENSHIFT_MYSQL_DB_PASSWORD']
}


DB = torndb.Connection(
            host=options['mysql_host'], database=options['mysql_database'],
            user=options['mysql_user'], password=options['mysql_password'])


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class MainHandler(BaseHandler):
     def get(self):
          self.render('index.html')

# Put here yours handlers.

class MessageHandler(BaseHandler):
    def get(self):
        self.write("Hello from the other side")

    def post(self):
        try:
            email = self.get_argument("email")
            if sql_query._user_exists(email=email):
                ping_datetime = self.get_argument("ping_datetime")
                ping_datetime = datetime.datetime.strptime(ping_datetime, "%Y-%m-%d %H:%M:%S")
                message = self.get_argument("message")
                # process
                DB.execute("INSERT INTO messages SET \
                                email = '{}', \
                                ping_datetime = '{:%Y-%m-%d :%H:%M:%S}', \
                                message = '{}';".format(email, ping_datetime,
                                                        message))
                self.write({"success":"True"})
            else:
                self.write({"sucess":"False", "reason":"User doesn't exist"})
        except Exception as e:
            self.write({"success":"False", "reason":"Database Error, please report", "exception":"{}".format(e)})


class ConfigHandler(BaseHandler):
    def get(self):
        self.write("Hello from the other side")

    def post(self):
        try:
            email = self.get_argument("email")
            join_date = self.get_argument("join_date")
            join_date = datetime.datetime.strptime(join_date, "%Y-%m-%d").date()
            os = self.get_argument("os")
            phone = self.get_argument("phone")
            country_code = self.get_argument("country_code")
            password = self.get_argument("password")
            country_name = self.get_argument("country_name")
            phone_os = self.get_argument("phone_os")
            if sql_query._user_exists(email=email, phone=phone):
                self.write({"success":"False", "reason":"User Exists"})
            else:
                ## Do some checks
                DB.execute("INSERT INTO users SET \
                                email = '{}', \
                                password = '{}', \
                                join_date =  '{:%Y-%m-%d}', \
                                os = '{}', \
                                phone = '{}', \
                                country_code = '{}', \
                                country_name = '{}', \
                                phone_os = '{}';".format(email, password,
                                join_date, os, phone, country_code,
                                country_name, phone_os))
                self.write({"success":"True"})
        except Exception as e:
            self.write({"success":"False", "reason":"Database Error, please report"})



handlers = [
    (r'/', MainHandler),
    (r'/config/', ConfigHandler),
    (r'/message/', MessageHandler),
    ]

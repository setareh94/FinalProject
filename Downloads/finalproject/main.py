
import time
import jinja2
import os
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
import random
import datetime

jinja_environment = jinja2.Environment(loader=
jinja2.FileSystemLoader(os.path.dirname(__file__)))

def get_date (tz):
    now = datetime.datetime.now(tz)
    year = str(now.year)
    month = str(now.month)
    weekday = str(now.strftime('%A'))
    day =str(now.day)
    hour = str(now.hour)
    hour_time = get_hour(hour)

    return year,month,weekday,day,hour

def get_hour (n):
    if n >= 5 and n <= 11 :
        return 'Morning'
    if n >= 12 and n <= 15 :
        return 'Afternoon'
    if n >= 16 and n <= 18:
        return 'Evening'
    if n >= 19 and n <=21:
        return 'Night'
    return 'Late-Night'

class EST(datetime.tzinfo ):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-4)

    def dst(self, dt):
        return datetime.timedelta(0)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        localtime = datetime.datetime.now()
        year,month,weekday,day,hour_time = get_date(EST())
        self.response.write(year + '<br>')
        self.response.write(month + '<br>')
        self.response.write(weekday + '<br>')
        self.response.write(day + '<br>')
        self.response.write(hour_time + '<br>')
        self.response.write('')






app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
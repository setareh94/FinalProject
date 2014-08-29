import time
import jinja2
import os
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
import random
import datetime
import json
import logging
jinja_environment = jinja2.Environment(loader=
jinja2.FileSystemLoader(os.path.dirname(__file__)))

Monday_through_Thursday_defaults ={'Morning':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Ride a Bike', 'Call Your Friend', 'Prepare a Trip for the Day', 'Go Hiking', 'Doing Housework', 'Dance to your Favorite Music', 'Sing a Song', 'Work in a Office', 'Drink a cup of Gourmet Coffee or Tea'],'Study':['Read a Book that You Have Always wanted to Read', 'Reread your Favorite Book', 'Study for Your Day Later On', 'Read Your Favorite Magazine', 'Watch the News'],
'Relax':['Pray/Meditate','Buy a must-read book (and read it)', 'Do Yoga', 'Take a shower','Listen to Your Favorite Music']},'Afternoon':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],'Fun':['Meet Up with a Friend','Go Visit a Local Park','Watch a Movie','Work-out','GO Shopping', 'Making Your Favorite Bake Goods'],
'Study':['Study for your class ','Read at a nearby Lake', 'Reread your Favorite Book', 'Study with classical music'], 'Relax':['Listen to Music','Take a Nap', 'Watch a Comedy Movie', 'DO Yoga', 'Surf the Web','Watch TV']},'Evening':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Play some Music','Call Your Best Friend', 'Call your family', 'Go for a swim', 'Take a walk to the Park', 'Going to a Nearby Festival'],'Study':['Study in the Living Room','Study Your Best Subject', 'Study Your Worst Subject', 'Study with a Friend'], 
'Relax':['Buy a must-read book (and read it)', 'Do Yoga', 'Take a shower','Watch your favorite video', 'Call your Best Friend and Talk about the Day']},'Night':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Play Video Games','Surf the Web', 'Play some Music', 'Go Out for a Walk', 'Catch up with Friends', 'Watch Your Favorite TV Show'],'Study':['Study for Your Next Class','Read at a nearby Lake', 'Reread Your Favorite Book', 'Study with Classical Music', 'Making Some Bake Goods'],
'Relax':['Take an Early Bed','Take Shower', 'Call Your Family', 'Call you Friend about your Day']},'Late-Night':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],'Fun':['Sleeping', 'Brush your teeth', 'Taking a Bath'],'Study':['Nerd! You Should be Asleep', 'Learn to Code', 'Learn to Hum a New Song', 'Learn to Say Hi in a Different Language', 'Look up Recent News Topics'], 
'Relax':['Good Night','Buy a must-read book (and read it)', 'Take a Shower', 'Listen to Instrumental Music']}}


Friday_and_Saturday_defaults ={'Morning':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Jogging','Running', 'Hiking in Mountain', 'Surfing','Biking', 'Take a Ride to a Park', 'Falling Back Asleep', 'Going to a Festival'],
'Study':[ 'Study for Your Next Exam','Learn something new', 'Study with Your Friend in class', 'Learn how to Make a New Dish'], 
'Relax':['Work at the Garden','reading books', 'Do Some Exercise', 'Talk a Walk to the Garden', 'Stretch']},
'Afternoon':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Go Shopping','Go to the Grocery Store','Have a Pool Party', 'Go to a Pet Store and visit your favorite animal', 'Read Your Favorite Comic', 'Take a Swim', 'Go to an amazement park', 'Watch the New Movie'],
'Study':['Study for your upcoming exam','Study with your favorite Music','Learn how to say Hi in a language you do not know'], 
'Relax':['Listen to Music','reading books', 'Play some Music', 'Bake Goods for your Favorite Person', 'Surf the Web']},
'Evening':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Dress Up for a Fancy Dinner','Watch a Movie', 'Go for a Ride', 'Make Something Health', 'Make a Healthy Dinner'],
'Study':['Learn to make a New Dinner Dish','Learn to Relax', 'Read Economist', 'Read Some News Magazine', 'Play Video/ Computer Games'], 
'Relax':['Hangout with your Friends','reading books', 'Take a Walk at the Park', 'Take a Nap', 'Call your Family']},
'Night':{'Food':[ 'Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Go to a Fancy Restaurant','Go to the mall for some new clothes', 'Walk to a Park and talk to People', 'Go for a Swim'],
'Study':[ 'Learn to Knit','Study for Your Upcoming Test','Learn to Make a Nice Cup of Coffee','Learn something about wine-tasting', 'Learn to Fold a New Origami'], 
'Relax':['Before Sleep Yoga','reading books', 'Call Your Family', 'Listen to Some Sweet Music', 'Pray or Meditate', 'Surf the Web']},
'Late-Night':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Sleeping', 'Brush your teeth', 'Taking a Bath', 'Go to the Theater to watch a Midnight Premiere', 'Go to the Bar(only if you are 21 or older)', 'Do some Before Sleep Stretches', 'A House Party'],
'Study':['Nerd! You Should be asleep', 'Read an non-academic book', 'Learn a new set of before sleep exercise', 'Read your favorite part of a novel'], 
'Relax':['Good Night','Reading books', 'Sleep', 'Read your least favorite book', 'Listen to some classical Music']}}

Sunday_defaults ={'Morning':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Jogging','Running', 'Hiking in Mountain', 'Surfing'],'Study':['Doing Homework', 'Work on Research paper'], 
'Relax':['Reading a Good Sci-Fi Book', 'Getting a Massage', 'Listing to Classical Music' ]},'Afternoon':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Going to Beach', 'Going to Downtown', 'Going Kayaking'],'Study':['Instead of Studying do some household chorus','Clean Up your room','Do Dishes','Taking the trash out'], 
'Relax':['Reading a Classical Novel','Go to the park', 'Listing to Smooth music' ]},'Evening':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Playing vide games', 'Skyping with Friends','Signing out loud in the shower', 'Take your Dog for a walk'],'Study':['Last Minute Studying', 'Memorizing','Getting Prepare for Mondays Lesson'], 
'Relax':['Talk with your parent','Talk to your grandpa', 'Take a nap', 'Read a romantic Novel', 'Relax in the beach']},'Night':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Watching Movie','Playing an instrument', 'Singing in the shower'],'Study':['Reviewing','Last Minute Homework!', 'Learn to Code', 'Learn a new language', 'Learn how to paint'], 
'Relax':['Chill infront of fireplace','reading books', 'Going to Bed Early']},'Late-Night':{'Food':['Click our Cook Book for amazing recipes','Click our Menu for restaurants close to your location'],
'Fun':['Playing Xbox', 'Watching T.V.', 'Listinig to Music', 'Playing Board Game'],'Study':['Nerd! You Should be Sleep'], 
'Relax':['Good Night','Reading books', 'Sleeping', 'Brush your teeth', 'Taking a Bath']}}

def makeOptions (values, selected):
    lista = []
    for i in values:
        if i == selected:
            lista.append('<option selected value ='+i+'>'+i+'</option>')
        else:
            lista.append('<option value ='+i+'>'+i+'</option>')
    string = ''.join(lista)
    return string

def get_message1(n):
    if n == 0:
        return 'having fun'
    if n == 1:
        return 'eating'
    if n == 2:
        return 'studying so much'
    if n == 3:
        return 'relaxing'
def get_message2(n):
    if n == 0:
        return 'have fun!'
    if n == 1:
        return 'go out to eat or cook something!'
    if n == 2:
        return 'learn/study something!'
    if n == 3:
        return 'relax a little bit more.'


def get_date (tz):
    now = datetime.datetime.now(tz)
    year = str(now.year)
    month = str(now.month)
    weekday = str(now.strftime('%A'))
    day =str(now.day)
    hour = str(now.hour)
    hour_time = get_hour(hour)

    return year,month,weekday,day,hour_time

def get_hour (n):
    n = int(n)
    if n >= 5 and n <= 11 :
        return 'Morning'
    if n >= 12 and n <= 15 :
        return 'Afternoon '
    if n >= 16 and n <= 18:
        return 'Evening'
    if n >= 19 and n <=21:
        return 'Night'
    return 'Late-Night'

def get_subcats(user,day,hour_time,category):
    if day == 'Sunday':
        user.Sunday_subcats[hour_time][category]
    elif day == 'Friday' or day == 'Saturday':
        user.Friday_and_Saturday_subcats[hour_time][category]
    else:
        return user.Monday_through_Thursday_subcats[hour_time][category]


class UTC(datetime.tzinfo ):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-0)

    def dst(self, dt):
        return datetime.timedelta(0)

class EDT(datetime.tzinfo ):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-4)

    def dst(self, dt):
        return datetime.timedelta(0)

class CDT(datetime.tzinfo ):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5)

    def dst(self, dt):
        return datetime.timedelta(0)

class MDT(datetime.tzinfo ):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-6)

    def dst(self, dt):
        return datetime.timedelta(0)

class PDT(datetime.tzinfo ):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=-7)

    def dst(self, dt):
        return datetime.timedelta(0)

def timezone_function(string):
    if string == 'EDT':
        return EDT ()
    if string == 'CDT':
        return CDT ()
    if string == 'MDT':
        return MDT ()
    if string == 'PDT':
        return PDT ()


class All_Users(ndb.Model):
    username = ndb.UserProperty()
    timezone = ndb.StringProperty()
    Monday_through_Thursday_subcats = ndb.JsonProperty()
    Friday_and_Saturday_subcats = ndb.JsonProperty()
    Sunday_subcats = ndb.JsonProperty()
    Food_score =ndb.IntegerProperty()
    Fun_score =ndb.IntegerProperty()
    Relax_score =ndb.IntegerProperty()
    Study_score =ndb.IntegerProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            return self.redirect(users.create_login_url('/'))
        logout_url = users.create_logout_url('/')
        all_users = All_Users.query()
        user_information = all_users.filter(All_Users.username == user).get()
        if user_information == None:
            user_information = All_Users(username = user,timezone = 'EDT', Monday_through_Thursday_subcats = Monday_through_Thursday_defaults, 
            Sunday_subcats = Sunday_defaults, Friday_and_Saturday_subcats = Friday_and_Saturday_defaults,Food_score=0,Fun_score=0,Relax_score=0,Study_score=0)
            user_information.put()
        year,month,weekday,day,hour_time = get_date(timezone_function(user_information.timezone))
        list_of_scores = [user_information.Fun_score,user_information.Food_score,user_information.Study_score,user_information.Relax_score]
        subcats_message = ''
        if max(list_of_scores) - min(list_of_scores) >= 5:
            index_biggest = list_of_scores.index(max(list_of_scores))
            index_smallest = list_of_scores.index(min(list_of_scores))
            message_part1 = get_message1(index_biggest)
            message_part2 = get_message2(index_smallest)
            subcats_message = 'Instead of '+message_part1+' you should '+message_part2
        template_values = {'day':weekday, 'hour_time':hour_time,'user': user,  'logout_url':logout_url, 'fun':get_subcats(user_information,weekday,hour_time,'Fun'),
        'food':get_subcats(user_information,weekday,hour_time,'Food'),'study':get_subcats(user_information,weekday,hour_time,'Study')
        ,'relax':get_subcats(user_information,weekday,hour_time,'Relax'), 'subcats_message':subcats_message}
        template = jinja_environment.get_template('home.html')
        self.response.out.write(template.render(template_values))
    def post(self):
        logout_url = users.create_logout_url('/')
        hour_time = self.request.get('hour_time')
        user = users.get_current_user()
        all_users = All_Users.query()
        user_information = all_users.filter(All_Users.username == user).get()
        fun = self.request.get('fun')
        message = ''
        if fun != '':
            message = 'Have fun!'
            user_information.Fun_score += 1
        food = self.request.get('food')
        if food != '':
            message = 'Bon appetite!'
            user_information.Food_score += 1
        relax = self.request.get('relax')
        if relax != '':
            message = 'Take your time chilling!'
            user_information.Relax_score += 1
        study = self.request.get('study')
        if study != '':
            message = 'Good luck!'
            user_information.Study_score += 1
        user_information.put()
        

        # self.response.write(fun)
        # self.response.write(food)
        # self.response.write(relax)
        # self.response.write(study)
        template_values = {'hour_time':hour_time, 'user':user , 'logout_url':logout_url, 'message':message}
        template = jinja_environment.get_template('home_after_submit.html')
        self.response.out.write(template.render(template_values))
        # logging.info('frfer')

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            return self.redirect(users.create_login_url('/'))
        all_users = All_Users.query()
        user_information = all_users.filter(All_Users.username == user).get()
        year,month,weekday,day,hour_time = get_date(timezone_function(user_information.timezone))
        timezone_dropdown = makeOptions(['UTC','EDT','CDT','MDT','PDT'], user_information.timezone)
        template_values = {'fun':get_subcats(user_information,weekday,hour_time,'Fun'),
        'food':get_subcats(user_information,weekday,hour_time,'Food'),'study':get_subcats(user_information,weekday,hour_time,'Study')
        ,'relax':get_subcats(user_information,weekday,hour_time,'Relax'), 'timezone_dropdown':timezone_dropdown}
        template = jinja_environment.get_template('profile.html')

        self.response.out.write(template.render(template_values))
    def post(self):
        submit = self.request.get('submit')
        fun = self.request.get('fun')
        user = users.get_current_user()
        all_users = All_Users.query()
        user_information = all_users.filter(All_Users.username == user).get()
        year,month,weekday,day,hour_time = get_date(timezone_function(user_information.timezone))
        if submit == 'Change Time':
            user_information.timezone = self.request.get('mydropdown')
            user_information.put()
        if submit == 'Add':
            addrelax =self.request.get('addrelax')
            addfun = self.request.get('addfun')
            addstudy =self.request.get('addstudy')
            if addstudy != '':
                get_subcats(user_information,weekday,hour_time,'Study').append(addstudy)
            if addfun != '':
                get_subcats(user_information,weekday,hour_time,'Fun').append(addfun)
            if addrelax != '':
                get_subcats(user_information,weekday,hour_time,'Relax').append(addrelax)
            user_information.put()
        if submit == 'Delete':
            fun_deletes = self.request.get_all('fun')
            study_deletes = self.request.get_all('study')
            relax_deletes = self.request.get_all('relax')
            for i in fun_deletes:
                get_subcats(user_information,weekday,hour_time,'Fun').remove(str(i))
            for i in study_deletes:
                get_subcats(user_information,weekday,hour_time,'Study').remove(str(i))
            for i in relax_deletes:
                get_subcats(user_information,weekday,hour_time,'Relax').remove(str(i))
            user_information.put()
        self.get()

            

            




app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/profile', ProfileHandler),
], debug=True)

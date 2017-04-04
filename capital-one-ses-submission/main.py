#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import OrderedDict
import csv
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import jinja2
import json
import logging
import random
# import requests
import urllib2
from operator import eq
import os
import webapp2


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# def get_lat_lng():
#     send_url = 'http://freegeoip.net/json'
#     r = requests.get(send_url)
#     j = json.loads(r.text)
#     lat = j['latitude']
#     lon = j['longitude']
#     console.log(lat)
#     console.log(lon)

def replace_spaces(query):
    return query.lower().replace(',','').replace(' ', '%20')

def get_current_latitude():
    url = 'http://freegeoip.net/json'
    response = urllib2.urlopen(urllib2.Request(url, headers={'Accept': 'application.json'}))
    location_data = json.load(response)
    latitude = location_data['latitude']
    return latitude

def get_current_longitude():
    url = 'http://freegeoip.net/json'
    response = urllib2.urlopen(urllib2.Request(url, headers={'Accept': 'application.json'}))
    location_data = json.load(response)
    longitude = location_data['longitude']
    return longitude

def get_latitude(location):
    google_url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&sensor=false'
    response = urllib2.urlopen(urllib2.Request(google_url, headers={'Accept': 'application.json'}))
    location_data = json.load(response)
    latitude = location_data['results'][0]['geometry']['location']['lat']
    return latitude

def get_longitude(location):
    google_url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&sensor=false'
    response = urllib2.urlopen(urllib2.Request(google_url, headers={'Accept': 'application.json'}))
    location_data = json.load(response)
    longitude = location_data['results'][0]['geometry']['location']['lng']
    return longitude

def get_api_contents(search_term, latitude, longitude):
    auth = 'Bearer 0F3JznLA0qsIEAU0FRfrhuX8sJLnyHGT2Fsye18cZ50eujlFbiPSCHYbAIkVM6dv6EpZVyev_kLIqg1NwVsHf5UoLTbX9d_klxBooyOFlWNv6svWWdXB39_MFaXdWHYx'
    yelp_url = 'https://api.yelp.com/v3/businesses/search?term=' + search_term + '&limit=3&latitude=' + str(latitude) + '&longitude=' + str(longitude)
    response = urllib2.urlopen(urllib2.Request(yelp_url, headers={'Authorization': auth, 'Accept': 'application.json'}))
    businesses_data = json.load(response)
    place = businesses_data['businesses'][0]['name']
    template_vars = {
        'name': place
    }
    return template_vars

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # get_lat_lng()
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/about.html')
        self.response.write(template.render())

class CoffeeHandler(webapp2.RequestHandler):
    def get(self):
        current_lat = get_current_latitude()
        current_lng = get_current_longitude()
        # place = get_api_contents('coffee', current_lat, current_lng)
        # logging.info(place)
        template = jinja_environment.get_template('templates/coffee.html')
        template_vars = get_api_contents('coffee', current_lat, current_lng)
        self.response.write(template.render(template_vars))

class DonutsHandler(webapp2.RequestHandler):
    def get(self):
        current_lat = get_current_latitude()
        current_lng = get_current_longitude()
        # place = get_api_contents('donuts', current_lat, current_lng)
        # logging.info(place)
        template = jinja_environment.get_template('templates/donuts.html')
        template_vars = get_api_contents('donuts', current_lat, current_lng)
        self.response.write(template.render(template_vars))

class DrinksHandler(webapp2.RequestHandler):
    def get(self):
        current_lat = get_current_latitude()
        current_lng = get_current_longitude()
        # place = get_api_contents('drinks', current_lat, current_lng)
        # logging.info(place)
        template = jinja_environment.get_template('templates/drinks.html')
        template_vars = get_api_contents('drinks', current_lat, current_lng)
        self.response.write(template.render(template_vars))

class ResultHandler(webapp2.RequestHandler):
    def get(self):
        location = self.request.get('searchInput')
        location = replace_spaces(location)
        place = get_api_contents('donuts', get_latitude(location), get_longitude(location))
        logging.info(place)
        template = jinja_environment.get_template('templates/result.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    ('/coffee', CoffeeHandler),
    ('/donuts', DonutsHandler),
    ('/drinks', DrinksHandler),
    ('/result', ResultHandler)
], debug=True)

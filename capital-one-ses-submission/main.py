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
import urllib
from operator import eq
import os
import webapp2
# import yelp


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/about.html')
        self.response.write(template.render())

class CoffeeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/coffee.html')
        self.response.write(template.render())

class DonutsHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/donuts.html')
        self.response.write(template.render())

class DrinksHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/drinks.html')
        self.response.write(template.render())

class ResultHandler(webapp2.RequestHandler):
    def get(self):
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
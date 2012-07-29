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
import webapp2
import logging
try:
    import simplejson as json
except ImportError:
    import json

from models import *

from google.appengine.ext.webapp import template
from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):
    def get(self):
        """
            main page. mostly handles authenticating
            the user and setting up the necessary templates
        """
        current_user = users.get_current_user()
        if not current_user:
            self.error(403)
            return
        
        e = current_user.email()
        try:
            current_resident = Resident.all().filter('email = ', e)[0]
        except IndexError:
            logging.info("%s tried to login" % e)
            self.error(403)
            self.response.out.write("<h3>Couldn't find a resident with email address:</h3> %s" % e)
            return
            
        template_values = { 
            "resident": current_resident,
            "admin": users.is_current_user_admin()
        } 
        self.response.out.write(template.render("templates/create_review.html", template_values))
            
class ResidentApiHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get("name")
        email = self.request.get("email")
        
        r = Resident(name=name, email=email)
        r.put()
        
        self.response.out.write("successfully created resident with name [%s] and email [%s]"% (name, email))

app = webapp2.WSGIApplication([
        ('/',               MainHandler),
        ('/api/resident/',  ResidentApiHandler),
    ], debug=True)
    
def main():
    # App Engine reuses your request handlers when you specify a main function
    logging.getLogger().setLevel(logging.DEBUG)
    webapp.util.run_wsgi_app(app)   

if __name__ == '__main__':
    main()

#!/usr/bin/env python
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
    # homepage,  handles auth and templates
    def get(self):
        current_user = users.get_current_user()
        if not current_user:
            self.error(403); return
        
        e = current_user.email()
        try:
            current_resident = Resident.all().filter('email = ', e)[0]
        except IndexError:
            logging.info("%s tried to login" % e)
            self.error(403)
            self.response.out.write("<h3>Couldn't find a resident with email address: %s</h3>" % e)
            return
            
        template_values = { 
            "resident": current_resident,
            "admin": users.is_current_user_admin()
        } 
        self.response.out.write(template.render("templates/index.html", template_values))
            
class ResidentApiHandler(webapp2.RequestHandler):
    def get(self):
        """
            TODO: remove this once the 5 residents are in the db
        """
        name = self.request.get("name")
        email = self.request.get("email")
        gender = self.request.get("gender")
        
        r = Resident(name=name, email=email, gender=gender)
        r.put()
        
        self.response.out.write("created resident with name [%s] and email [%s]"% (name, email))
        
class ExpenseApiHandler(webapp2.RequestHandler):
    def post(self):
        pay_to = self.request.get("pay_to")
        owner = self.request.get("owner_id")
        title = self.request.get("title")
        cost = self.request.get("cost")
        date = self.request.get("date")
        memo = self.request.get("memo")
        
        e = Expense(owner=owner, title=title, cost=cost, date=date, memo=memo)
        e.put()
        
        self.response.out.write("")
        
class RequestApiHandler(webapp2.RequestHandler):
    def post(self):
        expense = self.request.get("expense_id")
        recipient = self.request.get("recipient_id")
        amount = self.request.get("amount")
        
        r = Request(expense=expense, recipient=recipient, amount=amount)
        r.put()
        
        self.response.out.write("")
        
class PaymentApiHandler(webapp2.RequestHandler):
    def post(self):
        amount = request.get("amount")
        request = request.get("request_id") # NB: this breaks the "request" var
        
        p = Payment(request=request, amount=amount)
        p.put()
        
        self.response.out.write("")

app = webapp2.WSGIApplication([
        ('/',               MainHandler),
        ('/api/resident/',  ResidentApiHandler),
        ('/api/expense/',   ExpenseApiHandler),
        ('/api/request/',   RequestApiHandler),
        ('/api/payment/',   PaymentApiHandler),
    ], debug=True)
    
def main():
    # App Engine reuses your request handlers when you specify a main function
    logging.getLogger().setLevel(logging.DEBUG)
    webapp.util.run_wsgi_app(app)   

if __name__ == '__main__':
    main()

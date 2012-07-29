from google.appengine.ext import db

class Resident(db.Model):
    name = db.StringProperty()
    is_current_resident = db.BooleanProperty(default=True)
    email = db.EmailProperty()
    gender = db.StringProperty()
    
class Expense(db.Model):
    owner = db.ReferenceProperty(Resident)
    cost = db.FloatProperty()
    date = db.DateProperty()
    title = db.StringProperty()
    pay_to = db.StringProperty()
    memo = db.TextProperty()
    is_valid = db.BooleanProperty(default=True) # allow cancelled expenses
    
class Request(db.Model):
    """an explicit request for money from one resident to another"""
    expense = db.ReferenceProperty(Expense)
    recipient = db.ReferenceProperty(Resident)
    amount = db.FloatProperty()
    is_valid = db.BooleanProperty(default=True) # allow cancelled requests
    
class Payment(db.Model):
    """an indication that someone has paid off a request"""
    request = db.ReferenceProperty(Request)
    amount = db.FloatProperty()
    date = db.DateProperty(auto_now=True)
    acknowleged = db.BooleanProperty(default=False)
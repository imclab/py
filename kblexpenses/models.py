from google.appengine.ext import db

class Resident(db.Model):
    name = db.StringProperty()
    is_current_resident = db.BooleanProperty(default=True)
    email_address = db.EmailProperty()
    
class Expense(db.Model):
    paid_by = db.ReferenceProperty(Resident)
    cost = db.FloatProperty()
    date = db.DateProperty()
    title = db.StringProperty()
    memo = db.TextProperty()
    
class Request(db.Model):
    """an explicit request for money from one resident to another"""
    expense = db.ReferenceProperty(Expense)
    to = db.ReferenceProperty(Resident)
    amount = db.FloatProperty()
    
class Payment(db.Model):
    """an indication that someone has paid off a request"""
    request = db.ReferenceProperty(Request)
    amount = db.FloatProperty()
    datetime = db.DateTimeProperty()
    acknowleged = db.BooleanProperty()
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(80), unique=True, nullable = False)
    email =  db.Column(db.String(80), unique=True, nullable = False)  
    password =  db.Column(db.String(80), nullable = False)
    role =  db.Column(db.String(80), nullable = False)
    lastLoggedIn =  db.Column(db.DateTime, default=datetime.now())
    address = db.Column(db.String, nullable=True)
    pincode = db.Column(db.String(6), nullable=True)
    
    #service professional fields
    experience = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    services_provided = db.Column(db.String(200), nullable=True)
    resume = db.Column(db.String(255), nullable=True)
    
    def __init__(self, username, email, role, password, address=None, pincode=None, experience=None, services_provided=None, resume=None):
      self.username=username
      self.email=email  
      self.role=role
      self.password = bcrypt.generate_password_hash(password).decode('utf-8')
      self.address = address
      self.pincode = pincode
      self.experience = experience
      self.services_provided = services_provided
      self.resume = resume
      
      if role == 'professional':
            self.is_active = False
      else:
            self.is_active = True
            
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    services = db.relationship('Service', backref='category', lazy=True)

    def __init__(self, name):
        self.name = name


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)  
    price = db.Column(db.Float, nullable=False)  
    time_required = db.Column(db.DateTime, nullable=False)  
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    def __init__(self, name, description, price, time_required, category_id):
        self.name = name
        self.description = description
        self.price = price
        self.time_required = time_required
        self.category_id = category_id

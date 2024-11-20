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
    mobile = db.Column(db.String(10), nullable=True)
    
    #service professional fields
    experience = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    resume = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    flagged = db.Column(db.Boolean, default=False, nullable=False)
    services_provided = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', back_populates='professionals_specialization')
    service_requests_as_customer = db.relationship('ServiceRequest', foreign_keys='ServiceRequest.customer_id', back_populates='customer')
    service_requests_as_professional = db.relationship('ServiceRequest', foreign_keys='ServiceRequest.professional_id', back_populates='professional')
    
    def __init__(self, username, email, role, password, address=None, pincode=None, mobile=None, 
                 experience=None, services_provided=None, resume=None, rating=None, flagged=False):
      self.username=username
      self.email=email  
      self.role=role
      self.password = bcrypt.generate_password_hash(password).decode('utf-8')
      self.address = address
      self.pincode = pincode
      self.mobile = mobile
      self.experience = experience
      self.services_provided = services_provided
      self.resume = resume
      self.rating = rating
      self.flagged = flagged
      
      if role == 'professional':
            self.is_active = False
      else:
            self.is_active = True
            
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    categoryImage = db.Column(db.String(255), nullable=True)
    services = db.relationship('Service', back_populates='category', cascade='all, delete')
    professionals_specialization = db.relationship('User', back_populates='category')
    def __init__(self, name, categoryImage=None):
        self.name = name
        self.categoryImage = categoryImage

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)  
    price = db.Column(db.Float, nullable=False)  
    time_required = db.Column(db.String, nullable=False)  
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='services')
    service_requests = db.relationship('ServiceRequest', back_populates='service')
    
    def __init__(self, name, description, price, time_required, category_id):
        self.name = name
        self.description = description
        self.price = price
        self.time_required = time_required
        self.category_id = category_id

    

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key referencing User
    professional_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Foreign key referencing User
    
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    
    # Using Enum for service_status to restrict values
    service_status = db.Column(db.String(20), default="requested", nullable=False)  # 'requested', 'assigned', 'closed'
    
    remarks = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    rebooked = db.Column(db.Boolean, default=False, nullable=True)
    
    # Relationships
    service = db.relationship('Service', back_populates='service_requests')
    customer = db.relationship('User', foreign_keys=[customer_id], back_populates='service_requests_as_customer')
    professional = db.relationship('User', foreign_keys=[professional_id], back_populates='service_requests_as_professional')
    
    def __init__(self, service_id, customer_id, professional_id=None, 
                 date_of_request=datetime.utcnow, date_of_completion=None, 
                 service_status="requested", remarks=None, rebooked=False):
        self.service_id = service_id
        self.customer_id = customer_id
        self.professional_id = professional_id
        self.date_of_request = date_of_request
        self.date_of_completion = date_of_completion
        self.service_status = service_status
        self.remarks = remarks
        self.rebooked = rebooked

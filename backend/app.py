import csv
from flask import Flask, Response, jsonify, make_response, request, send_file, send_from_directory
from sqlalchemy import func
from tools import workers, tasks, mailer
from config import Config
from models import *
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token, unset_jwt_cookies
from werkzeug.utils import secure_filename
from flask_caching import Cache
import os
import io
from celery.result import AsyncResult

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
cache = Cache(app)
mailer.init_app(app)

celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    timezone='Asia/Kolkata',
    enable_utc=False,
    broker_connection_retry_on_startup = True
)

celery.Task = workers.ContextTask
app.app_context().push()

def create_admin():
    existing_admin = User.query.filter_by(role="admin").first()
    
    if existing_admin:
        return jsonify({"message":"Admin already exists"}), 200
    
    try:
        admin = User(username="admin", email="admin@atoz.com", role="admin", password="pass")
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message":"Admin created successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Exception":str(e)}), 500
        
with app.app_context():
    db.create_all()
    create_admin()

CORS(app, supports_credentials=True, expose_headers=["Content-Disposition"])

@app.route("/celery-test")
def celery_test():
    task = tasks.add.delay(1,2)
    return {"task_id":task.id}

@app.route("/get-celery-result/<task_id>")
def getCeleryResult(task_id):
    result = AsyncResult(task_id, app=celery)
    if result.ready():
        return {"result":result.result}, 200
    else:
        return {"message": "Task not yet completed"}, 405
    
@app.route("/")
def home():
    return "Hello World"


@app.route("/register", methods=["POST"])
def register():
    
    username = request.form.get("username")
    email = request.form.get("email")
    role = request.form.get("role")
    password = request.form.get("password")
    address = request.form.get('address')
    pincode = request.form.get('pincode')
    mobile = request.form.get('mobile')
    if not username or not email or not password or not role or not address or not pincode:
        return jsonify({"error":"All fields required"}), 400
    
    existingUser = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
    
    if existingUser:
         return jsonify({"message":"Username/email already exists"}), 200
     
    if role == 'professional':
        experience = request.form.get('experience')
        services_provided = request.form.get('services_provided')
        resume = request.files.get('resume')
        
        if not experience or not services_provided or not resume:
            return jsonify({"error":"All fields required"}), 400   
        
        pdf_filename = secure_filename(username + "_resume.pdf")
        pdf_path = os.path.join(app.config["RESUME_FOLDER"], pdf_filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        resume.save(pdf_path)  
    
    try:
        if role == 'professional':
            user = User(username=username, email=email, role=role, password=password, 
                    address=address, pincode=pincode, mobile=mobile, experience=experience, 
                    services_provided=services_provided, resume=pdf_filename)
        else:
             user = User(username=username, email=email, role=role, password=password, 
                    address=address, pincode=pincode, mobile=mobile)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"User created successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Exception":str(e)}), 500
   
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error":"All fields required"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    if user.is_active == False:
        return jsonify({"error": "Your profile access is disabled. Kindly contact admin for more details."}), 401
    access_token = create_access_token(identity={"email":email, "role":user.role, "id":user.id})
   
    user.lastLoggedIn = datetime.now()
    db.session.commit()
    
    return jsonify({"message":"Login successful", "access_token":access_token}), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user= get_jwt_identity()
    user= User.query.filter_by(id=current_user['id']).first()
    
    if user.role != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    
    return "Hey {user.username}, you can access this resource", 200


@app.route('/getuserdata', methods=['GET'])
@jwt_required()
def getuserdata():
    current_user= get_jwt_identity()

    user= User.query.filter_by(id=current_user['id']).first()
        
    if not user:
        return jsonify({"error":"User not found"}), 404
    
    userdata = {"id":user.id, "username":user.username, "email":user.email, "role":user.role,
                "address":user.address, "pincode":user.pincode, "mobile": user.mobile, "is_active": user.is_active}
    return jsonify({"message":"User found","user":userdata}), 200


# Profile update
@app.route('/updateProfile', methods=['POST'])
@jwt_required()
def update_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    if not user:
        return jsonify({"error":"User not found"}), 404
    print("Data:",request.form.get('username'), request.form.get('address'), request.form.get('pincode'))
    user.username = request.form.get('username')
    if(request.form.get('password') != ''):
        password = request.form.get('password')
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    user.address = request.form.get('address')
    user.pincode = request.form.get('pincode')
    user.mobile = request.form.get('mobile')
    
    db.session.commit()
    return jsonify({"message":"Profile updated successfully"}), 200
    

@app.route("/logout", methods=["GET", "POST"])
@jwt_required()
def logout():
    response = jsonify({"message":"Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@app.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    name = request.form.get('name')
    image = request.files.get('categoryImage')
        
    if not name or not image:
        return jsonify({"error":"All fields required"}), 400   
    category = Category.query.filter_by(name=name).first()
    if category:
        return jsonify({"error":"Category already exists"}), 400
        
    image_filename = secure_filename(name + ".jpg")
    image_path = os.path.join(app.config["CATEGORY_IMAGES"], image_filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    image.save(image_path)
      
    new_category = Category(name=name, categoryImage=image_filename)
    db.session.add(new_category)
    db.session.commit()
    # Clear the cached categories data after creating a new category
    cache.delete('categories')
    cache.delete('services')
    return jsonify({'message': 'Category created'}), 201

@app.route('/categories', methods=['GET'])
@cache.cached(timeout=30, key_prefix='categories')
def get_categories():
    categories = Category.query.all()
    categories_data = [{'id': category.id, 'name': category.name, 
                        'categoryImage': category.categoryImage,
                        'services': [service.name for service in category.services],
                        'professionals': [professional.username for professional in category.professionals_specialization],
                        } 
                       for category in categories]
                       
    return jsonify({"message":"Categories found","categories":categories_data}), 200

# Define a route to serve category images
@app.route('/images/<filename>')
def serve_image(filename):
    image_directory = app.config["CATEGORY_IMAGES"] # Adjust this to match your path
    if not os.path.isfile(os.path.join(image_directory, filename)):
        return send_from_directory(image_directory, "default_image.jpg")
    return send_from_directory(image_directory, filename)

@app.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    name = request.form.get('name')
    image = request.files.get('categoryImage')
    category = Category.query.filter_by(id=id).first()
    category.name = name
    
    if image:
        if category.categoryImage:
            os.remove(app.config["CATEGORY_IMAGES"] + "/" + category.categoryImage)
    
        image_filename = secure_filename(name + ".jpg")
        image_path = os.path.join(app.config["CATEGORY_IMAGES"], image_filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image.save(image_path)
        category.categoryImage = image_filename
    db.session.add(category)
    db.session.commit()
    
    # Clear the cached categories data after updating a category
    cache.delete('categories')
    return jsonify({'message': 'Category updated'})

@app.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    category = Category.query.filter_by(id=id).first()
    if not category:
        return jsonify({"error":"Category not found"}), 404
    
    try:
        db.session.delete(category) 
        if category.categoryImage:
            os.remove(app.config["CATEGORY_IMAGES"] + "/" + category.categoryImage)
        db.session.commit()
         
        # Clear the cached categories data after deleting a category
        cache.delete('categories')
        return jsonify({"message":"Category deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Exception":str(e)}), 500
    
@app.route('/categories/<int:category_id>/services', methods=['GET'])
@cache.memoize(timeout=10)
def get_services_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    services_data = [{'id': service.id, 'name': service.name,
                      'price': service.price, 'time_required': service.time_required,
                      'category_id': service.category_id} for service in category.services]
    return jsonify({'services': services_data})

#fetch one service details
@app.route('/service/<int:id>', methods=['GET'])
@cache.memoize()
def get_service(id):
    service = Service.query.get_or_404(id)
    service_data = {
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': service.price,
        'time_required': service.time_required,
        'category_id': service.category_id
    }
    return jsonify({"message":"Service found","service":service_data}), 200
#Fetch one category details
@app.route('/categories/<int:id>', methods=['GET'])
@cache.memoize()
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify({'category': {
        'id': category.id,
        'name': category.name,
        'categoryImage': category.categoryImage
    }})
# Routes for Services
@app.route('/services', methods=['POST'])
@jwt_required() 
def create_service():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    data = request.json
    new_service = Service(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        time_required= data['time_required'],
        category_id=data['category_id']
    )
    db.session.add(new_service)
    db.session.commit()
    
    # Clear the cached services data after creating a new service
    cache.delete('services')
    return jsonify({'message': 'Service created'}), 201

@app.route('/services', methods=['GET'])
@cache.cached(timeout=30, key_prefix='services')
def get_services():
    services = Service.query.all()
    service_data =[]
    for service in services:
        service_data.append({
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': service.price,
            'time_required': service.time_required,  
            'category_id': service.category_id
        })
    return jsonify({"message":"Services found","services":service_data}), 200


@app.route('/services/<int:id>', methods=['PUT'])
@jwt_required() 
def update_service(id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    data = request.json
    service = Service.query.get_or_404(id)
    service.name = data['name']
    service.description = data.get('description', service.description)
    service.price = data['price']
    service.time_required = data['time_required']
    service.category_id = data['category_id']
    db.session.commit()
    
    # Clear the cached services data after updating service
    cache.delete('services')
    return jsonify({'message': 'Service updated'})

@app.route('/services/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    
    # Clear the cached services data after deleting a service
    cache.delete('services')
    return jsonify({'message': 'Service deleted'})

# Return list of all professionals
@app.route('/professionals', methods=['GET'])
@jwt_required()
@cache.cached(timeout=30, key_prefix='professionals')
def get_professionals():
    current_user = get_jwt_identity()
    
    # Authorization check
    if current_user["role"] != "admin":
        return jsonify({"message": "You are not authorized to access this resource"}), 403

    # Helper function to transform User objects into dictionaries
    def format_professional(professional):
        return {
            'id': professional.id,
            'username': professional.username,
            'email': professional.email,
            'services_provided': professional.category.name if professional.category else None,
            'resume': professional.resume,
            'experience': professional.experience,
            'address': professional.address,
            'pincode': professional.pincode,
            'mobile': professional.mobile,
            'is_active': professional.is_active,
            'flagged': professional.flagged
        }

    # Query and transform professionals
    available_professionals = User.query.filter_by(role='professional', is_active=True).all()
    new_professionals = User.query.filter_by(role='professional', is_active=False).all()

    available_professionals_data = [format_professional(p) for p in available_professionals]
    new_professionals_data = [format_professional(p) for p in new_professionals]

    return jsonify({
        'new_professionals': new_professionals_data,
        'available_professionals': available_professionals_data
    }), 200

# Approve/reject new professional
@app.route('/professionals/<int:id>', methods=['PUT', 'DELETE'])
@jwt_required()
def approve_or_delete_professionals(id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    professional = User.query.filter_by(id=id).first() 
    if request.method == 'PUT':
        professional.is_active = True
        cache.delete('professionals')
        db.session.commit()
        return jsonify({'message': 'Professional approved'})
    elif request.method == 'DELETE':
        db.session.delete(professional)
        os.remove(app.config["RESUME_FOLDER"] + "/" + professional.resume)
        db.session.commit()
        cache.delete('professionals')
        return jsonify({'message': 'Professional rejected'})
    
    return jsonify({'message': 'Invalid request'})

#View resume pdf of professionals
@app.route("/view_resume/<int:id>", methods=["GET"])
def view_catalogue(id):
    professional = User.query.filter_by(id=id).first() 
    if not professional:
        return jsonify({"error":"professional not found"}), 404
    pdf = professional.resume
    pdf_path = os.path.join(app.config["RESUME_FOLDER"], pdf)
    return send_file(pdf_path, as_attachment=False)


# Return list of all customers
@app.route('/customers', methods=['GET'])
@jwt_required()
@cache.cached(timeout=10, key_prefix='customers')
def get_customers():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    customers = User.query.filter_by(role='customer').all()
    customer_data = []
    for customer in customers:
        customer_data.append({
            'id': customer.id,
            'username': customer.username,
            'email': customer.email,
            'mobile': customer.mobile,
            'address': customer.address,
            'pincode': customer.pincode,
            'flagged': customer.flagged
        })
    return jsonify({'customers': customer_data}), 200

@app.route('/customers/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        
        # Clear the cached customers data after deleting a customer
        cache.delete('customers')
        return jsonify({'message': 'User deleted'})
    else:
        return jsonify({'message': 'User not found'}), 404

#Block users
@app.route('/block_unblock_user/<int:id>/<string:status>', methods=['PUT'])
@jwt_required()
def block_user(id, status):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    user = User.query.filter_by(id=id).first()
    if user:
        if status == 'block':
            user.flagged = True
            db.session.commit()
            cache.delete('customers') if user.role == 'customer' else cache.delete('professionals')
            return jsonify({'message': 'User blocked'}), 200
        elif status == 'unblock':
            user.flagged = False
            db.session.commit()
            cache.delete('customers') if user.role == 'customer' else cache.delete('professionals')
            return jsonify({'message': 'User unblocked'}), 200
        
    else:
        return jsonify({'message': 'User not found'}), 404


# Create a route to book a service request
@app.route('/service_requests', methods=['POST'])
def create_service_request():
    data = request.get_json()
    
    service_request = ServiceRequest(
        service_id=data['service_id'],
        customer_id=data['customer_id'],
        professional_id=data.get('professional_id'),  
        date_of_request=datetime.fromisoformat(data.get('date_of_request')),
        date_of_completion=None,
        service_status=data.get('status'),
        remarks="",
        rebooked=data.get('rebooked')
    )
    try:
        db.session.add(service_request)
        db.session.commit()
        
        # Clear the cached service requests data after creating a service request
        cache.delete('service_requests')
        
    except Exception as e: 
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Service request created successfully', 'service_request_id': service_request.id}), 201

#get professionals by their category
@app.route('/professionals_by_category/<int:category_id>', methods=['GET'])
@jwt_required()
@cache.memoize()
def get_professionals_by_category(category_id):
    professionals = User.query.filter_by(role='professional', services_provided=category_id).all()
    professional_data = []
    for professional in professionals:
        professional_data.append({
            'id': professional.id,
            'username': professional.username,
            'email': professional.email,
            'services_provided': professional.category.name,
            'experience': professional.experience,
            'pincode': professional.pincode,
            'rating': professional.rating
        })
    return jsonify({'professionals': professional_data}), 200

#Get all service requests
@app.route('/service_requests', methods=['GET'])
@jwt_required()
@cache.cached(timeout=20, key_prefix='service_requests')
def get_service_requests():
    service_requests = ServiceRequest.query.all()
    service_request_data = []
    for service_request in service_requests:
        service_request_data.append({
            'id': service_request.id,
            'service_name': service_request.service.name,
            'service_id': service_request.service_id,
            'price': service_request.service.price,
            'time_required': service_request.service.time_required,
            'category': service_request.service.category.name,   
            'category_id': service_request.service.category_id,
            'customer_id': service_request.customer_id,
            'customer_name': service_request.customer.username,
            'role': service_request.customer.role,
            'professional_id': service_request.professional_id,
            'assigned_professional': service_request.professional.username,
            'booked_on': service_request.date_of_request,
            'closed_on': service_request.date_of_completion,
            'status': service_request.service_status,
            'remarks': service_request.remarks,
            'rebooked': service_request.rebooked
        })
        
    return jsonify({'service_requests': service_request_data}), 200

#Professional accepting/rejecting service requests
@app.route('/service_requests/<int:id>/<string:status>', methods=['PUT'])
def update_service_request(id, status):
    service_request = ServiceRequest.query.filter_by(id=id).first()
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    if status == 'accepted':
        service_request.service_status = 'accepted'
    elif status == 'rejected':
        service_request.service_status = 'rejected'
        service_request.date_of_completion = datetime.now()
    elif status == 'completed':
        service_request.service_status = 'completed'
        service_request.date_of_completion = datetime.now()
    db.session.commit()
    
    # Clear the cached service requests data after updating a service request
    cache.delete('service_requests')
    return jsonify({'message': 'Service request'+status}), 200

#Customer updating service requests
@app.route('/service_requests/customer/<int:id>/<string:status>', methods=['PUT'])
def update_service_request_customer(id, status):
    service_request = ServiceRequest.query.filter_by(id=id).first()
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    if status == 'cancelled':
        service_request.service_status = 'cancelled'
        service_request.date_of_completion = datetime.now()
    elif status == 'completed':
        service_request.service_status = 'completed'
        service_request.date_of_completion = datetime.now()
        service_request.remarks = request.form.get('remarks')
        rating = request.form.get('rating')
        service_request.rating = rating

        # Update professional rating
        professional = User.query.filter_by(id=service_request.professional_id).first()
        
        current_rating = professional.rating
        if current_rating is None:
            professional.rating = rating
        else:
            new_rating = (float(current_rating)+float(rating)) / 2
            professional.rating = new_rating
            
    db.session.commit()
    
    # Clear the cached service requests data after updating a service request
    cache.delete('service_requests')
    return jsonify({'message': 'Service request '+status}), 200

@app.route('/service_requests/rebook/<int:id>', methods=['PUT'])
def rebook_service_request(id):
    service_request = ServiceRequest.query.filter_by(id=id).first()
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    service_request.rebooked = True
    db.session.commit()
    
    # Clear the cached service requests data after updating a service request
    cache.delete('service_requests')
    return jsonify({'message': 'Service request rebooked'}), 200

#Reschedule service request
@app.route('/service_requests/<int:id>/reschedule', methods=['PUT'])
def reschedule_ServiceRequest(id):
    service_request = ServiceRequest.query.filter_by(id=id).first()
    if not service_request:
        return jsonify({'error': 'Service request not found'}), 404
    
    service_request.date_of_request = datetime.fromisoformat(request.form.get('rescheduled_date'))
    db.session.commit()
    
    # Clear the cached service requests data after updating a service request
    cache.delete('service_requests')
    return jsonify({'message': 'Service request rescheduled'}), 200

# Route handlers for search functionalities
@app.route('/search/customers', methods=['POST'])
def search_customers():
    query = request.form.get('query')
    search_type = request.form.get('type')
    text_query = f"%{query}%"
    result = []
    if search_type == 'service_name':
        result = (Service.query.join(Category).join(User, User.services_provided == Category.id)
        .filter(Service.name.like(text_query)).all())
    
    elif search_type == 'location':
        result = ( Service.query.join(Category)
            .join(User, User.services_provided == Category.id)
            .filter(User.address.like(text_query), User.role == 'professional').all())
    
    elif search_type == 'pincode':
        result = ( Service.query.join(Category)
            .join(User, User.services_provided == Category.id)
            .filter(User.pincode.like(text_query), User.role == 'professional').all())
        
    if result:
        results = []
        for result in result:
            results.append({
            'name': result.name,
            'id': result.id,
            'price': result.price,
            'time_required': result.time_required,
            'category': result.category.name,
            'category_id': result.category_id
            })
        return jsonify({'results': results}), 200
    
    return jsonify({'message': 'Invalid search'}), 400

@app.route('/search/professionals', methods=['POST'])
def search_professionals():
    query = request.form.get('query')
    search_type = request.form.get('type')
    user_id = request.form.get('user_id')
    text_query = f"%{query}%"
    result = []
    
    if search_type == 'date_booked':
        result = ServiceRequest.query.filter(ServiceRequest.professional_id == user_id, 
                                    ServiceRequest.date_of_request.like(text_query)).all()
    
    elif search_type == 'date_closed':
        result = ServiceRequest.query.filter(ServiceRequest.professional_id == user_id, 
                                     ServiceRequest.date_of_completion.like(text_query)).all()
    
    elif search_type == 'status':
        result = ServiceRequest.query.filter(ServiceRequest.professional_id == user_id, 
                                     ServiceRequest.service_status.like(text_query)).all()
    
    elif search_type == 'location':
        result = ServiceRequest.query.join(User, ServiceRequest.customer_id == User.id).filter(
            ServiceRequest.professional_id == user_id,
            User.address.like(text_query)).all()
        
    elif search_type == 'pincode':
        result = ServiceRequest.query.join(User, ServiceRequest.customer_id == User.id).filter(
            ServiceRequest.professional_id == user_id,
            User.pincode.like(text_query)).all()
        
    results = []
    if result:
        for result in result:
            results.append({
            'id': result.id, 
            'customer_name': result.customer.username,
            'assigned_professional': result.professional.username,
            'service_name': result.service.name,
            'category': result.service.category.name,
            'date_booked': result.date_of_request,
            'date_closed': result.date_of_completion if result.date_of_completion else 'N/A',
            'status': result.service_status,
            'address': result.customer.address,
            'pincode': result.customer.pincode
            })
        return jsonify({'results': results}), 200
    return jsonify({'message': 'Invalid search'}), 400

@app.route('/search/admin', methods=['POST'])
def search_admin():
    query = request.form.get('query')
    textquery = f"%{query}%"
    search_type = request.form.get('type')
    
    result = []
    if search_type == 'id':
        result = User.query.filter(User.id == query).all()
        
    elif search_type == 'email':
        result = User.query.filter(User.email.like(textquery)).all()
    
    elif search_type == 'name':
        result = User.query.filter(User.username.like(textquery)).all()
    
    if result:
        results = []
        for result in result:
            results.append({
                'id': result.id, 
                'name': result.username,
                'email': result.email, 
                'role': result.role
            })
        return jsonify({'results': results}), 200
    
    if search_type == 'status':
        result = ServiceRequest.query.filter(ServiceRequest.service_status.like(textquery)).all()
        if result:
            results = []
            for result in result:
                results.append({
                'id': result.id, 
                'service_name': result.service.name,
                'category': result.service.category.name,
                'status': result.service_status,
                'date_booked': result.date_of_request,
                'date_closed': (result.date_of_completion if result.date_of_completion else 'N/A'),
                'assigned_professional': result.professional.username,
                'customer_name': result.customer.username
            })
            return jsonify({'results': results}), 200
        
    return jsonify({'message': 'Invalid search'}), 400

#Chart summary 
@app.route('/request_summary', methods=['GET'])
@jwt_required()
def request_summary():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    try:
        if user.role == 'admin':
            summary = (db.session.query(ServiceRequest.service_status, func.count(ServiceRequest.id))
            .group_by(ServiceRequest.service_status).all())
            data = {status: count for status, count in summary}
            return jsonify(data), 200

        elif user.role == 'professional':
            summary = (db.session.query(ServiceRequest.service_status, func.count(ServiceRequest.id))
            .filter(ServiceRequest.professional_id == user.id).filter(ServiceRequest.service_status != 'cancelled')
            .group_by(ServiceRequest.service_status).all())
            data = {status: count for status, count in summary}
            return jsonify(data), 200
        
        elif user.role == 'customer':
            summary = (db.session.query(ServiceRequest.service_status, func.count(ServiceRequest.id))
            .filter(ServiceRequest.customer_id == user.id)
            .group_by(ServiceRequest.service_status).all())
            data = {status: count for status, count in summary}
            return jsonify(data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ratings_summary', methods=['GET'])
@jwt_required()
def ratings_summary():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    rated_requests = []   
    # Admin: all ratings
    if user.role == 'admin':
        rated_requests = db.session.query( ServiceRequest.rating,func.count(ServiceRequest.rating)
        ).filter(ServiceRequest.rating.isnot(None)).group_by(ServiceRequest.rating).all()
        
        not_rated_count = db.session.query(func.count(ServiceRequest.id)
        ).filter(ServiceRequest.service_status == 'completed').filter(ServiceRequest.rating.is_(None)).scalar()

    # Professional: ratings for requests assigned to them
    elif user.role == 'professional':
        rated_requests = db.session.query(ServiceRequest.rating,func.count(ServiceRequest.rating)
        ).filter(ServiceRequest.rating.isnot(None),ServiceRequest.professional_id == user.id
        ).group_by(ServiceRequest.rating).all()
        
        not_rated_count = db.session.query(func.count(ServiceRequest.id)
            ).filter(ServiceRequest.service_status == 'completed').filter(
            ServiceRequest.rating.is_(None), ServiceRequest.professional_id == user.id).scalar()

    # Customer: ratings they provided
    elif user.role == 'customer':
        rated_requests = db.session.query(ServiceRequest.rating,func.count(ServiceRequest.rating)
        ).filter(ServiceRequest.rating.isnot(None), ServiceRequest.customer_id == user.id
        ).group_by(ServiceRequest.rating).all()
        
        not_rated_count = db.session.query(func.count(ServiceRequest.id)
            ).filter(ServiceRequest.service_status == 'completed').filter(
            ServiceRequest.rating.is_(None), ServiceRequest.customer_id == user.id).scalar()

    # Format ratings data into a dictionary with keys for ratings 1-5 and "Not Rated Yet"
    ratings_summary = {str(i): 0 for i in range(1, 6)}
    ratings_summary["Not Rated Yet"] = not_rated_count

    # Populate ratings summary with actual counts
    for rating, count in rated_requests:
        ratings_summary[str(int(rating))] = count
    return jsonify(ratings_summary), 200

@app.route('/generate_csv_report', methods=['GET'])
@jwt_required()
def generate_report():
    task = tasks.generate_csv_report.delay()
    return jsonify({'task_id': task.id}), 200

@app.route('/download_report/<task_id>', methods=['GET'])
@jwt_required()
def download_report(task_id):
    result = AsyncResult(task_id, app=celery)
    if result.ready():
        filepath=result.get()
        if "/mnt/d" in filepath:
            filepath = filepath.replace("/mnt/d", "")
        filename = filepath.split('/')[-1]
        response = make_response(send_file(filepath, as_attachment=True))
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response, 200
    else:
        return {"message": "Task not yet completed"}, 405
    

if __name__ == "__main__":
    app.run(debug=True)
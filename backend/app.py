from flask import Flask, jsonify, request, send_file
from config import Config
from models import *
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token, unset_jwt_cookies
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

def create_admin():
    existing_admin = User.query.filter_by(role="admin").first()
    
    if existing_admin:
        return jsonify({"message":"Admin already exists"}), 200
    
    try:
        admin = User(username="admin", email="admin@gmail.com", role="admin", password="pass")
        db.session.add(admin)
        db.session.commit()
        return jsonify({"message":"Admin created successfully"}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"Exception":str(e)}), 500
        
with app.app_context():
    db.create_all()
    create_admin()

CORS(app, supports_credentials=True)

#Testing routes
@app.route("/")
def hello():
    return "Hello world!"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")
    address = data.get('address')
    pincode = data.get('pincode')

    if not username or not email or not password or not role or not address or not pincode:
        return jsonify({"error":"All fields required"}), 400
    
    existingUser = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
    
    if existingUser:
         return jsonify({"message":"User already exists"}), 200
     
    if role == 'professional':
        experience = data.get('experience')
        services_provided = data.get('services_provided')
        
        if not experience or not services_provided:
            return jsonify({"error":"All fields required"}), 400     
    
    try:
        if role == 'professional':
            user = User(username=username, email=email, role=role, password=password, 
                    address=address, pincode=pincode, experience=experience, 
                    services_provided=services_provided)
        else:
             user = User(username=username, email=email, role=role, password=password, 
                    address=address, pincode=pincode)
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
    
    userdata = {"username":user.username, "email":user.email, "role":user.role}
    return jsonify({"message":"User found","user":userdata}), 200

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
    data = request.json
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created'}), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_data = [{'id': category.id, 'name': category.name} for category in categories]
    return jsonify({"message":"Categories found","categories":categories_data}), 200

@app.route('/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message":"You are not authorized to access this resource"}), 403
    data = request.json
    category = Category.query.get_or_404(id)
    category.name = data['name']
    db.session.commit()
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
        db.session.commit()
        return jsonify({"message":"Category deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"Exception":str(e)}), 500
    

# Routes for Services
@app.route('/services', methods=['POST'])
@jwt_required() 
def create_service():
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
    return jsonify({'message': 'Service created'}), 201

@app.route('/services', methods=['GET'])
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
    data = request.json
    service = Service.query.get_or_404(id)
    service.name = data['name']
    service.description = data.get('description', service.description)
    service.price = data['price']
    service.time_required = data['time_required']
    service.category_id = data['category_id']
    db.session.commit()
    return jsonify({'message': 'Service updated'})

@app.route('/services/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted'})

if __name__ == "__main__":
    app.run(debug=True)
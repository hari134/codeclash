from flask import request ,jsonify, Blueprint
from utils.db import get_collection 

auth_routes = Blueprint('auth_routes',__name__)

@auth_routes.route('/register',methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    usn = request.json.get('usn')
    
    users = get_collection('users')

    # Check if the username already exists
    if users.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'})

    # Insert the new user into the database
    users.insert_one({'username': username, 'password': password, 'usn':usn,'email':email})

    return jsonify({'message': 'Registration successful'})

@auth_routes.route('/login',methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    users = get_collection('users')

    # Check if the username and password match
    if users.find_one({'username': username, 'password': password}):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'})


@auth_routes.route('/all_users',methods=['GET'])
def get_all_users():
    users = get_collection('users')
    data = users.find({},{"_id":0})
    _data = []
    for d in data:
        _data.append(d)
    return jsonify({'message': _data})
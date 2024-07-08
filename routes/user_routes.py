from flask import Blueprint, jsonify, request
from models import User, db
from flask_jwt_extended import create_access_token

userRoutes = Blueprint('user', __name__)

@userRoutes.route('/user', methods=['GET'])
def getUsers():
    users = User.query.all()
    if users:
        user_dicts = [user.userToDict() for user in users]
        return jsonify(user_dicts)
    else:
        return jsonify({"error": "No users found"}), 404

@userRoutes.route('/user/register', methods=['POST'])
def addUser():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing name or password"}), 400
    
    # Check if user with the same name already exists
    existingUser = User.query.filter_by(username=username).first()
    if existingUser:
        return jsonify({"error": "user with this name already exists"}), 400
    
    # Password Hashing - Create a new user instance and set password
    newUser = User(username=username)
    newUser.setPassword(password)
    
    # Add to database and commit
    db.session.add(newUser)
    db.session.commit()

    accessToken = create_access_token(identity=username)

    return jsonify({"success": "user added successfully", "Access Token is": accessToken}), 201

@userRoutes.route('/user/login')
def userLogin():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password"})

    # Query for database check
    user = User.query.filter_by(username=username).first()

    if not user or not user.checkPassword(password):
        return jsonify({"error": "Invalid username or password"})
    
    # If username and password are correct genereate JWT
    accessToken = create_access_token(identity=username)
    
    # Succes
    return jsonify({"success": "Login Succesfully", "access token is ": accessToken})
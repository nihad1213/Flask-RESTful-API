from flask import Blueprint, jsonify, request
from models import Admin, db

adminRoutes = Blueprint('admin', __name__)

@adminRoutes.route('/admin', methods=['GET'])
def getAdmins():
    admins = Admin.query.all()
    if admins:
        admin_dicts = [admin.adminToDict() for admin in admins]
        return jsonify(admin_dicts)
    else:
        return jsonify({"error": "No admins found"}), 404

@adminRoutes.route('/admin/register', methods=['POST'])
def addAdmin():
    data = request.json
    adminName = data.get('adminName')
    password = data.get('password')

    if not adminName or not password:
        return jsonify({"error": "Missing name or password"}), 400
    
    # Check if admin with the same name already exists
    existingAdmin = Admin.query.filter_by(adminName=adminName).first()
    if existingAdmin:
        return jsonify({"error": "Admin with this name already exists"}), 400
    
    # Password Hashing - Create a new admin instance and set password
    newAdmin = Admin(adminName=adminName)
    newAdmin.setPassword(password)
    
    # Add to database and commit
    db.session.add(newAdmin)
    db.session.commit()

    return jsonify({"success": "Admin added successfully"}), 201
    

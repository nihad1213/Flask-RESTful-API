from flask import Blueprint, jsonify, request
from models import Company, db

cmpRoutes = Blueprint('cmp', __name__)

@cmpRoutes.route('/company', methods=['GET'])
def getCompanies():
    companies = Company.query.filter_by(approved=False).all()
    if companies:
        cmp_dicts = [cmp.companyToDict() for cmp in companies]
        return jsonify(cmp_dicts)
    else:
        return jsonify({"error": "No companies found"}), 404
    
@cmpRoutes.route('/company', methods=['POST'])
def addCompany():
    data = request.json
    name = data.get('name')
    approved = data.get('approved')

    if not name:
        return jsonify({"error": "Missing name"}), 400
    
    # Check if Company with the same name already exists
    existingCMP = Company.query.filter_by(name=name).first()
    if existingCMP:
        return jsonify({"error": "company with this name already exists"}), 400
    
    newCMP = Company(name=name, approved=approved)
    
    # Add to database and commit
    db.session.add(newCMP)
    db.session.commit()

    return jsonify({"success": "company added successfully"}), 201    

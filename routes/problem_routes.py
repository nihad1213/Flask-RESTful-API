from flask import Blueprint, jsonify, request
from datetime import datetime
from models import db, Problem

problemRoutes = Blueprint('problem', __name__)


@problemRoutes.route('/problems', methods=['GET'])
def listProblems():
    try:
        # Query all problems from the database
        problems = Problem.query.all()

        # Serialize problems into a list of dictionaries
        problems_list = [problem.problemToDict() for problem in problems]

        # Return JSON response with list of problems
        return jsonify({"problems": problems_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@problemRoutes.route('/problem', methods=['POST'])
def createProblem():
    data = request.json

    userID = data.get('user_id')
    content = data.get('content')

    if not userID or not content:
        return jsonify({"error": "Missing required fields"}), 400

    new_problem = Problem(userID=userID, content=content)

    try:
        db.session.add(new_problem)
        db.session.commit()
        return jsonify({"success": "Problem created successfully"}), 201
    except Exception as e:
        # Rollback in case of error
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def userToDict(self):
        return {
            "id": self.id,
            "username": self.username
        }

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adminName = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def adminToDict(self):
        return {
            "id": self.id,
            "adminName": self.adminName
        }

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    
    def companyToDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "approved": self.approved
        }

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def problemToDict(self):
        return {
            "id": self.id,
            "user_id": self.userID,
            "content": self.content,
            "created_at": self.created_at
        }


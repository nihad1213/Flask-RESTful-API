# Importing Modules and Models
from flask import Flask, Blueprint
from models import db
from models import User, Admin, Company, Problem
from flask_jwt_extended import JWTManager

# Creating Flask App
app = Flask(__name__)
jwt = JWTManager(app) 

# Configuration of App
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['JWT_SECRET_KEY'] = "Nihad1213"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# Importing Routes
from routes.admin_routes import adminRoutes
from routes.user_routes import userRoutes
from routes.company_routes import cmpRoutes
from routes.problem_routes import problemRoutes

app.register_blueprint(adminRoutes)
app.register_blueprint(userRoutes)
app.register_blueprint(cmpRoutes)
app.register_blueprint(problemRoutes)

@app.route('/')
def index():
    return 'Index Page'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables based on models

    app.run(debug=True)

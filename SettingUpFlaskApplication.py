import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize the Flask application
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://yourusername:yourpassword@localhost/fitness_center'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

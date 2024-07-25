import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize the Flask application
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://yourusername:yourpassword@localhost/fitness_center'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Define the Member model
class Member(db.Model):
    """
    Model for the members table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    age = db.Column(db.Integer)

# Define the WorkoutSession model
class WorkoutSession(db.Model):
    """
    Model for the workout_sessions table
    """
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    date = db.Column(db.Date)
    duration = db.Column(db.Integer)  # Duration in minutes

# Define the Member schema
class MemberSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for the Member model
    """
    class Meta:
        model = Member

# Define the WorkoutSession schema
class WorkoutSessionSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for the WorkoutSession model
    """
    class Meta:
        model = WorkoutSession

# Initialize schemas
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# CRUD Routes for Members
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], email=data['email'], age=data['age'])
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member)

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.query.get(member_id)
    return member_schema.jsonify(member) if member else ('', 404)

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    member = Member.query.get(member_id)
    if member:
        data = request.get_json()
        member.name = data['name']
        member.email = data['email']
        member.age = data['age']
        db.session.commit()
        return member_schema.jsonify(member)
    return ('', 404)

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Member.query.get(member_id)
    if member:
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted successfully'})
    return ('', 404)

# Routes for Managing Workout Sessions
@app.route('/workouts', methods=['POST'])
def add_workout():
    data = request.get_json()
    new_workout = WorkoutSession(member_id=data['member_id'], date=data['date'], duration=data['duration'])
    db.session.add(new_workout)
    db.session.commit()
    return workout_session_schema.jsonify(new_workout)

@app.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    workout = WorkoutSession.query.get(workout_id)
    if workout:
        data = request.get_json()
        workout.date = data['date']
        workout.duration = data['duration']
        db.session.commit()
        return workout_session_schema.jsonify(workout)
    return ('', 404)

@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_member_workouts(member_id):
    workouts = WorkoutSession.query.filter_by(member_id=member_id).all()
    return workout_sessions_schema.jsonify(workouts)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)

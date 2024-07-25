from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector
from mysql.connector import Error

# Initialize Flask and Marshmallow
app = Flask(__name__)
ma = Marshmallow(app)

# Database connection function
def connect_to_db():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword",
            database="fitness_center"
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")

# Member Schema
class MemberSchema(ma.Schema):
    """Schema for Member serialization and deserialization."""
    class Meta:
        fields = ('id', 'name', 'email', 'phone')

# Workout Session Schema
class WorkoutSessionSchema(ma.Schema):
    """Schema for Workout Session serialization and deserialization."""
    class Meta:
        fields = ('id', 'member_id', 'session_date', 'activity', 'duration')

# Initialize schemas
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# CRUD operations for Members
@app.route('/members', methods=['POST'])
def add_member():
    """Adds a new member to the database."""
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        conn.commit()
        return member_schema.jsonify({'name': name, 'email': email, 'phone': phone})
    except Error as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Retrieves a member by their ID."""
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Members WHERE id = %s", (member_id,))
        member = cursor.fetchone()
        return member_schema.jsonify(member)
    except Error as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Updates a member's information."""
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Members SET name = %s, email = %s, phone = %s WHERE id = %s",
            (name, email, phone, member_id)
        )
        conn.commit()
        return member_schema.jsonify({'id': member_id, 'name': name, 'email': email, 'phone': phone})
    except Error as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Deletes a member from the database."""
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Members WHERE id = %s", (member_id,))
        conn.commit()
        return jsonify({'message': 'Member deleted successfully'})
    except Error as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# CRUD operations for Workout Sessions
@app.route('/workouts', methods=['POST'])
def add_workout():
    """Schedules a new workout session."""
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    activity = request.json['activity']
    duration = request.json['duration']
    
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO WorkoutSessions (member_id, session_date, activity, duration) VALUES (%s, %s, %s, %s)",
            (member_id, session_date, activity, duration)
        )
        conn.commit()
        return workout_session_schema.jsonify({'member_id': member_id, 'session_date': session_date, 'activity': activity, 'duration': duration})
    except Error as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_member_workouts(member_id):
    """Retrieves all workout sessions for a specific member."""
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (member_id,))
        workouts = cursor.fetchall()
        return workout_sessions_schema.jsonify(workouts)
    except Error as e:
        return jsonify({'message': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)

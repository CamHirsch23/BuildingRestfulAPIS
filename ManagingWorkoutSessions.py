# Route to add a new workout session
@app.route('/workouts', methods=['POST'])
def add_workout():
    data = request.get_json()
    new_workout = WorkoutSession(member_id=data['member_id'], date=data['date'], duration=data['duration'])
    db.session.add(new_workout)
    db.session.commit()
    return workout_session_schema.jsonify(new_workout)

# Route to update a workout session by ID
@app.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    workout = WorkoutSession.query.get_or_404(workout_id)
    data = request.get_json()
    workout.date = data['date']
    workout.duration = data['duration']
    db.session.commit()
    return workout_session_schema.jsonify(workout)

# Route to get all workout sessions for a specific member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_member_workouts(member_id):
    workouts = WorkoutSession.query.filter_by(member_id=member_id).all()
    return workout_sessions_schema.jsonify(workouts)

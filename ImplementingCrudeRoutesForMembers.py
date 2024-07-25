# Route to add a new member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], email=data['email'], age=data['age'])
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member)

# Route to get a member by ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = Member.query.get_or_404(member_id)
    return member_schema.jsonify(member)

# Route to update a member by ID
@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    member = Member.query.get_or_404(member_id)
    data = request.get_json()
    member.name = data['name']
    member.email = data['email']
    member.age = data['age']
    db.session.commit()
    return member_schema.jsonify(member)

# Route to delete a member by ID
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted successfully'})

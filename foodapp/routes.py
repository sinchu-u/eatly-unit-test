from flask import render_template, request, redirect, url_for, jsonify
from models import User
from utils import calculate_daily_calories

def register(app, db):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            users = User.query.all()
            return render_template('index.html', users=users)

        elif request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password_hash = request.form.get('password_hash')
            age = float(request.form.get('age'))
            height = float(request.form.get('height'))
            weight = float(request.form.get('weight'))
            gender = request.form.get('gender')

            user = User(
                name=name,
                email=email,
                password_hash=password_hash,
                age=age,
                height=height,
                weight=weight,
                gender=gender
            )
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('user_profile', user_id=user.id))

    @app.route('/user/<int:user_id>')
    def user_profile(user_id):
        user = User.query.get_or_404(user_id)
        calories = calculate_daily_calories(user.weight, user.height, user.age, user.gender)
        return render_template('user_profile.html', user=user, calories=calories)

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        users_data = [{
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "height": user.height,
            "weight": user.weight,
            "gender": user.gender
        } for user in users]
        return jsonify(users_data), 200

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        try:
            user = User(
                name=data['name'],
                email=data['email'],
                password_hash=data['password_hash'],
                age=float(data['age']),
                height=float(data['height']),
                weight=float(data['weight']),
                gender=data['gender']
            )
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "User created successfully", "user_id": user.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        calories = calculate_daily_calories(user.weight, user.height, user.age, user.gender)

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "height": user.height,
            "weight": user.weight,
            "gender": user.gender,
            "daily_calories": calories
        }), 200

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
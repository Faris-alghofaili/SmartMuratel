from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .modules import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    try:
        if request.method == 'POST':
            # Use request.get_json() to read JSON data sent by fetch()
            data = request.get_json(force = True)
            print(data)
            name = data.get("name")
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            confirm_password = data.get("confirm_password")

            # Basic validation
            if not name or not username or not email or not password or not confirm_password:
                return jsonify({"message": "All fields are required!"}), 400
            if User.query.filter_by(email = email).first():
                return jsonify({"message": "Email is already exits"}),400 
            if  User.query.filter_by(Username = username).first():
                return jsonify({"message": "Username is already exits"}),400 
            

            
            if password != confirm_password:
                return jsonify({"message": "Passwords do not match!"}), 400

            # Simulate user creation (add actual database logic here)
            new_user = User(
                first_name = name,
                Username = username,
                email = email,
                password_hash = generate_password_hash(password,method='sha256')  ,
                is_admin = False
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            print("Account created for:", username)

            # Success response
            return jsonify({"message": "Account created successfully!", "redirect": url_for('auth.sign_in')}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal server error"}), 500

    return render_template("sign_up.html")

@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    try:
        if request.method == 'POST':
            # ✅ Force JSON parsing
            data = request.get_json(force=True)
            email = data.get("email")
            password = data.get("password")

            if not email and not password:
                return jsonify({"message": "Please enter both email and password."}), 400

            # Example authentication check (replace with real logic)
            user = User.query.filter_by(email = email).first()
            if user:
                if check_password_hash(user.password_hash,password):
                        login_user(user, remember = True)
                        return jsonify({"message": "Login successful!", "redirect": url_for('views.home')}), 200
            else:
                return jsonify({"message": "Invalid email or password."}), 401

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "Internal server error"}), 500

    return render_template("sign_in.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.sign_in'))

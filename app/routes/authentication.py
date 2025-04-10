from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, logout_user, current_user
from app.controllers.auth_controller import register_user, user_login, generate_api_key, regenerate_api_key
from app.models import APIUsage

authentication_blueprint = Blueprint('authentication', __name__, url_prefix='/auth')


# ---------- Register ----------
@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                'email': request.form.get('email'),
                'password': request.form.get('password')
            }
        return register_user(data)
    return render_template('register.html')


# ---------- Login ----------
@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                'email': request.form.get('email'),
                'password': request.form.get('password')
            }
        return user_login(data)
    return render_template('login.html')


# ---------- Logout ----------
@authentication_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    session.pop('plain_api_key', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('authentication.login'))


# ---------- API Key Management ----------
@authentication_blueprint.route('/generate-api-key', methods=['POST'])
@login_required
def generate_key():
    return generate_api_key(current_user)


@authentication_blueprint.route('/regenerate-api-key', methods=['POST'])
@login_required
def regenerate_key():
    return regenerate_api_key(current_user)


# ---------- Dashboard ----------
@authentication_blueprint.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    api_key = session.get('plain_api_key') 
    usages = APIUsage.query.filter_by(user_id=current_user.id).order_by(APIUsage.timestamp.desc()).all()
    return render_template('dashboard.html', api_key=api_key, usages=usages)




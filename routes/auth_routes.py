from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from db_setup import db, bcrypt
from models.db import db
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from db_setup import db, bcrypt
from models.db import db
from werkzeug.security import check_password_hash
import random
import string
from flask import jsonify


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def auth_screen():
    return render_template('login.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash("Passwords do not match", "danger")
        return redirect(url_for('auth.auth_screen'))

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("User already exists", "warning")
        return redirect(url_for('auth.auth_screen'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, full_name=full_name, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash("Registered successfully! Please log in.", "success")
    return redirect(url_for('auth.auth_screen'))

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('login_email')
    password = request.form.get('login_password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['email'] = user.email
        session['name'] = user.full_name
        flash(f"Welcome back, {user.full_name}!", "success")  # ✅ Flash on login
        return redirect(url_for('home.dashboard'))
    else:
        flash("Invalid credentials", "danger")
        return redirect(url_for('auth.auth_screen'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('auth.auth_screen'))



# ========== FORGOT PASSWORD (STEP 1: ENTER EMAIL) ==========
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found", "danger")
            return redirect(url_for('auth.forgot_password'))

        session['reset_email'] = user.email
        session['reset_name'] = user.full_name

        captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        session['captcha'] = captcha

        return render_template(
            'forgot_password.html',
            name=user.full_name,
            email=user.email,
            captcha=captcha
        )

    return render_template('forgot_password_email.html')


# ========== RESET PASSWORD (STEP 2: SET NEW PASSWORD) ==========
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    email = session.get('reset_email')
    name = session.get('reset_name')
    entered_captcha = request.form.get('captcha_input')  # ✅ match input name from HTML
    password = request.form.get('new_password')          # ✅ match input name from HTML
    confirm_password = request.form.get('confirm_password')
    captcha_from_session = session.get('captcha', '')

    if not (name and email):
        flash("Session expired. Please try again.", "warning")
        return redirect(url_for('auth.forgot_password'))

    if not entered_captcha or entered_captcha.strip().upper() != captcha_from_session.strip().upper():
        flash("Invalid CAPTCHA", "danger")
        return redirect(url_for('auth.forgot_password'))

    if password != confirm_password:
        flash("Passwords do not match", "danger")
        return redirect(url_for('auth.forgot_password'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash("User not found", "danger")
        return redirect(url_for('auth.auth_screen'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user.password_hash = hashed_password
    db.session.commit()

    session.pop('reset_email', None)
    session.pop('reset_name', None)
    session.pop('captcha', None)

    flash("Password reset successful. Please log in.", "success")
    return redirect(url_for('auth.auth_screen'))



@auth_bp.route('/refresh-captcha')
def refresh_captcha():
    new_captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    session['captcha'] = new_captcha
    return jsonify({'captcha': new_captcha})


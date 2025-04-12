import os
import random
import string
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.db import db
from models.password import Password
from flask_jwt_extended import jwt_required
from models.encryption import encrypt_password, decrypt_password
from utils.email_utils import send_otp_email_view  # ✅ OTP helper
from models.user import User

password_bp = Blueprint('password', __name__)

@password_bp.route('/generate-password', methods=['GET', 'POST'])
def generate_password():
    if 'user_id' not in session:
        return redirect(url_for('auth.auth_screen'))

    generated_password = None

    if request.method == 'POST':
        name = request.form.get('password_name')
        length = int(request.form.get('length'))

        use_lowercase = 'lowercase' in request.form
        use_uppercase = 'uppercase' in request.form
        use_numbers = 'numbers' in request.form
        use_special = 'special' in request.form

        if not (use_lowercase or use_uppercase or use_numbers or use_special):
            flash("Please select at least one character type (lowercase, uppercase, numbers, special).", "warning")
            return redirect(url_for('password.generate_password'))

        existing_password = Password.query.filter_by(user_id=session['user_id'], password_name=name).first()
        if existing_password:
            flash("This password name already exists. Please choose a unique name.", "danger")
            return redirect(url_for('password.generate_password'))

        characters = ''
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_special:
            characters += string.punctuation

        generated_password = ''.join(random.choice(characters) for _ in range(length))

        encrypted_password = encrypt_password(generated_password)
        new_password = Password(
            user_id=session['user_id'],
            password_name=name,
            generated_password=encrypted_password
        )

        db.session.add(new_password)
        db.session.commit()

    return render_template('password_generator.html', generated_password=generated_password)


@password_bp.route('/view_password', methods=['GET', 'POST'])
def view_password():
    if 'user_id' not in session:
        return redirect(url_for('auth.auth_screen'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if request.method == 'POST':
        password_name = request.form.get('password_name')
        otp_input = request.form.get('otp')

        # If OTP field is filled, validate it
        if otp_input:
            session_otp = session.get('otp')
            session_password_name = session.get('otp_password_name')

            if otp_input == session_otp and password_name == session_password_name:
                # OTP matched — fetch and decrypt password
                password_entry = Password.query.filter_by(user_id=user_id, password_name=password_name).first()
                if password_entry:
                    decrypted_password = decrypt_password(password_entry.generated_password)
                    session.pop('otp', None)  # Cleanup session
                    session.pop('otp_password_name', None)
                    return render_template('view_password.html', password=decrypted_password, name=password_name)
                else:
                    flash("Password not found.", "danger")
            else:
                flash("Invalid OTP or password name mismatch.", "danger")
            return render_template('view_password.html', show_otp=True, password_name=password_name)

        # First-time password name submit — send OTP
        password_entry = Password.query.filter_by(user_id=user_id, password_name=password_name).first()
        if password_entry:
            otp = send_otp_email_view(user.email)
            if otp:
                session['otp'] = otp
                session['otp_password_name'] = password_name
                flash("OTP sent to your registered email.", "info")
                return render_template('view_password.html', show_otp=True, password_name=password_name)
            else:
                flash("Failed to send OTP. Please try again.", "danger")
        else:
            flash("Password not found.", "danger")

    return render_template('view_password.html')


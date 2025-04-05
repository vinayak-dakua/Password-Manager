from flask import Blueprint, render_template, session, redirect, url_for
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import random
import string
from flask import Blueprint, render_template, request, session, redirect, url_for
from models.db import db
from models.password import Password
from flask_jwt_extended import jwt_required


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

        # ✅ Check if at least one option is selected
        if not (use_lowercase or use_uppercase or use_numbers or use_special):
            flash("Please select at least one character type (lowercase, uppercase, numbers, special).", "warning")
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

        new_password = Password(
            user_id=session['user_id'],
            password_name=name,
            generated_password=generated_password
        )
        db.session.add(new_password)
        db.session.commit()

    return render_template('password_generator.html', generated_password=generated_password)



@password_bp.route('/view_password', methods=['GET', 'POST'])
#@jwt_required()
def view_password():
    if request.method == 'POST':
        password_name = request.form.get('password_name')
        user_id = session.get('user_id')  # ✅ Pulling user ID from session

        if not password_name:
            flash("Please enter the name of the password to view.", "warning")
            return redirect(url_for('password.view_password'))

        password_entry = Password.query.filter_by(user_id=user_id, password_name=password_name).first()

        if password_entry:
            return render_template('view_password.html', password=password_entry.generated_password, name=password_name)
        else:
            flash("Password not found.", "danger")
            return redirect(url_for('password.view_password'))

    return render_template('view_password.html')


from flask import Blueprint, render_template, session, redirect, url_for

home_bp = Blueprint('home', __name__)

@home_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.auth_screen'))

    return render_template('home.html', user=session.get('name'), email=session.get('email'))

@home_bp.route('/help')
def help():
    return render_template('help.html')

@home_bp.route('/about')
def about():
    return render_template('about.html')

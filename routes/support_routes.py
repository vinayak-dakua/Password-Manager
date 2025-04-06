# routes/support_routes.py
from flask import Blueprint, render_template, session, redirect, url_for

support_bp = Blueprint('support', __name__)

@support_bp.route('/help')
def help_screen():
    if 'user_id' not in session:
        return redirect(url_for('auth.auth_screen'))
    return render_template('help.html')

@support_bp.route('/about')
def about_screen():
    if 'user_id' not in session:
        return redirect(url_for('auth.auth_screen'))
    return render_template('about.html')

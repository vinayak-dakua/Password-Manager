from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config
from models.db import db
from routes.auth_routes import auth_bp
from routes.home_routes import home_bp
from routes.password_routes import password_bp
from routes.support_routes import support_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)  # ✅ This is the key part you were missing
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(password_bp)
app.register_blueprint(support_bp)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        try:
            from models import user, password  # Import models
            db.create_all()
            print("✅ Tables created successfully in Supabase!")
        except Exception as e:
            print("❌ Error while creating tables:", e)

    return app

# Run app creation directly
if __name__ == "__main__":
    create_app()

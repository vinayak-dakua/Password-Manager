from urllib.parse import quote_plus
import os

class Config:
    DB_USERNAME = "postgres"
    DB_PASSWORD = quote_plus("Vinayak@123")
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "password_manager_db"

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Vinayak%40123@localhost:5432/password_manager_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'


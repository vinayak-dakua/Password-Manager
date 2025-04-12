from urllib.parse import quote_plus
import os
from urllib.parse import quote_plus


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

    # server db
    SQLALCHEMY_DATABASE_URI = "postgresql://vinayak:aXhdz4Tv3sC4HgWqelKWq8NH7Zn1ZYDK@dpg-cvp6j8a4d50c73bp1uo0-a.oregon-postgres.render.com/password_manager_db_mj9t"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'

    # Local DB URI (commented out)
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Vinayak%40123@localhost:5432/password_manager_db"


    # SQLALCHEMY_DATABASE_URI ="postgresql://postgres:dakuavinayak@db.flkobipivaxgkxruqzno.supabase.co:5432/postgres"



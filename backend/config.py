import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    JWT_SECRET_KEY = "hello"
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
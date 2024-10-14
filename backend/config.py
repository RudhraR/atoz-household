import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    JWT_SECRET_KEY = "hello"
    RESUME_FOLDER = os.path.join(os.getcwd(), "professional_resume")
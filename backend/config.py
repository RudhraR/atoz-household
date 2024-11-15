import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    JWT_SECRET_KEY = "hello"
    RESUME_FOLDER = os.path.join(os.getcwd(), "professional_resume")
    CATEGORY_IMAGES = os.path.join(os.getcwd(), "category_images")
    
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 30
    CACHE_REDIS_PORT = 6379
    
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025  
    
    CSV_REPORT_EXPORT_FOLDER = os.path.join(os.getcwd(), "csv_reports")
    
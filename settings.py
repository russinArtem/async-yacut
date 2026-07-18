import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///yacut.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key-here')
    DISK_TOKEN = os.getenv('DISK_TOKEN')

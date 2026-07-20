import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///yacut.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key-here')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
    API_HOST = 'https://cloud-api.yandex.net/'
    API_VERSION = 'v1'
    MAX_ORIGINAL_LENGTH = 2048
    MAX_SHORT_LENGTH = 16
    SHORT_LENGTH = 6
    MAX_SHORT_GENERATION_ATTEMPTS = 10

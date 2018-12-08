import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    parent/base configurations class
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:Biochemistry01-@localhost/Jamii_FlaskApp' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class DevelopmentConfig(Config):
    """
    development configurations
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    production configurations
    """
    DEBUG = False


class TestingConfig(Config):
    """
    testing configurations
    """
    TESTING = True
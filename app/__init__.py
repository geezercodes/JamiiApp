import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)

#initializing db
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#login 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category='info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASSWORD')

ADMINS = ['geezerP@yahoo.com']

mail=Mail(app)
from app.views import views
from app.models import models
from app.forms import forms
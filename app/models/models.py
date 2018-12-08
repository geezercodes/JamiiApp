from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db,login_manager,app
from datetime import date, datetime


db.metadata.clear()

class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(60), unique = True)
    password_hash = db.Column(db.String(120))
    is_active = db.Column(db.Boolean())
    business = db.relationship('Business', backref = 'owner', lazy = True)
    reviews = db.relationship('Review', backref = 'review_owner', lazy = True)

    
    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod   
    def Verify_secret_token(token):
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id) 
           



    def __repr__(self):
        return "<User: {}>".format(self.username,self.email,self.password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    #password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #checks whether password_hash is equal to password given
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Business(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    BusinessName = db.Column(db.String())
    BusinessLocation = db.Column(db.String())
    date_established  = db.Column(db.Date(), default = datetime.utcnow)
    business_description = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    reviews = db.relationship('Review', backref = 'business_review', lazy = True)


    def __init__(self,BusinessName,BusinessLocation,date_established,business_description):
        self.BusinessName = BusinessName
        self.BusinessLocation = BusinessLocation
        self.date_established = date_established
        self.business_description = business_description



    def __repr__(self):
        return f'{self.BusinessName} was established on {self.date_established} and is located at {self.BusinessLocation}'    


class Review(db.Model):
  
    id = db.Column(db.Integer(), primary_key = True)
    review_headline = db.Column(db.String(30))
    comment = db.Column(db.String())
    rating = db.Column(db.Integer, nullable=False)
    business_id = db.Column(db.Integer(), db.ForeignKey('business.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Title: {self.review_headline}, comment: {self.comment}>'
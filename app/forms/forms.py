from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, TextAreaField, IntegerField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.models import User, Business, Review
from datetime import date

#register form
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')


   

#login formself
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


#businesses form
class BusinessForm(FlaskForm):
    BusinessName = StringField('BusinessName', validators = [DataRequired()])
    BusinessLocation = StringField('BusinessLocation', validators = [DataRequired()])
    date_established = DateTimeField('date_established', default = date.today(), format = '%d/%m/%Y',validators = [DataRequired(message = 'You need to enter the start date')])      
    business_description = TextAreaField('Give the discription of your business')
    submit = SubmitField('Submit')

class BusinessSearchForm(FlaskForm):
    BusinessName = StringField('BusinessName', validators = [DataRequired()])
    BusinessLocation = StringField(validators = [DataRequired()])
    date_established = DateTimeField('date_established', default = date.today(), format = '%d/%m/%Y',validators = [DataRequired(message = 'You need to enter the start date')]) 
    business_description = TextAreaField('Give the discription of your business')
    submit =SubmitField()





#review form
class ReviewForm(FlaskForm):
    review_headline = StringField('Review Headline', validators = [DataRequired()])
    comment = TextAreaField('Comment', validators = [DataRequired()])
    submit = SubmitField('Leave a Comment')

class RequestResetForm(FlaskForm):
     email = StringField('Email', validators=[DataRequired(),Email()])
     submit = SubmitField('Request Password Reset')

     def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.You must register first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password')
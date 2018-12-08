from flask import render_template, flash, url_for, redirect, request, abort
from app import app, db,mail
from app.forms.forms import RegisterForm, LoginForm, BusinessForm, ReviewForm,BusinessSearchForm,RequestResetForm,ResetPasswordForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models.models import User, Business, Review
from flask_mail import Message
from app import ADMINS


#home route
@app.route('/')
def home():
    return render_template('home.html')

#register route
@app.route('/registration', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account for {form.username.data} created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'register', form = form)

#login route
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            flash('You have successfully logged in', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful!! Please check email and password', 'danger')
    return render_template('login.html',title = 'login',form = form)

#logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#create business route
@app.route('/Business', methods = ['GET', 'POST'])
@login_required
def BusinessFunction():
    form = BusinessForm()
    if form.validate_on_submit():
        business = Business(BusinessName = form.BusinessName.data, owner = current_user, Businesslocation = form.BusinessLocation.data,
            date_established = form.date_established.data, business_description = form.business_description.data )
        db.session.add(business)
        db.session.commit()
        flash(f'Your Business {business.BusinessName} has successfully been registered', 'success')
        return redirect(url_for('available'))
    else:
        flash('Your business not registered please check on your details and try again', 'danger')
    return render_template('business.html',title = 'Business', form = form, legend = 'Register Business', btn = 'Register')


 


#route that display all registered businesses
@app.route('/available-business', methods =[ 'GET', 'POST']) 
def available():
    form = BusinessSearchForm()
    business = Business.query.all()
    location = Business.query.filter_by(BusinessLocation = form.BusinessLocation.data).all()
    if location:
        return redirect('location.html', location = location, form = form)

    return render_template('success.html', business = business, form = form)

#route that get business by id
@app.route('/business/<int:business_id>')
@login_required
def single_business(business_id):
    business = Business.query.get_or_404(business_id)
    return render_template('businessQuery.html', business = business)


#update a business route
@app.route('/business/<int:business_id>/update', methods = ['POST', 'GET'])
@login_required
def update_business(business_id):
    business = Business.query.get_or_404(business_id)
    if business.owner != current_user:
        abort(403)
    form = BusinessForm()
    if form.validate_on_submit():
        business.BusinessName = form.BusinessName.data
        business.BusinessLocation = form.BusinessLocation.data
        business.business_description = form.business_description.data
        db.session.commit()
        flash(f'Your business has been updated', 'success')
        return redirect(url_for('single_business', business_id = business.id))
    elif request.method == 'GET':
        form.BusinessName.data = business.BusinessName
        form.BusinessLocation.data = business.BusinessLocation
        form.business_description.data = business.business_description
    return render_template('business.html', title = 'update', form = form, legend = 'Update Business', btn = 'Update')





#route to delete a business
@app.route('/business-delete/<int:business_id>', methods = ['POST'])
@login_required
def deletebusiness(business_id):
    qry = db_session.query(Business).filter(Business.id==id)
        
    business = qry.first()
    if Business:
        form = BusinessForm(formdata=request.form, obj=Business)
        if request.method == 'POST' and form.validate():
            business = Business.query.get_or_404(business_id)
            db.session.delete(business)
            db.session.commit()
            flash('Your business has been deleted', 'success')
            return redirect(url_for('available'))
        return render_template('delete.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)


#route to post a review
@app.route('/business/<int:business_id>/review', methods = ['GET', 'POST'])
@login_required
def review(business_id):
    form = ReviewForm()
    business = Business.query.get_or_404(business_id)
    if form.validate_on_submit():
        review = Review(review_headline = form.review_headline.data,comment = form.comment.data )
        db.session.add(review)
        db.session.commit()
        flash('Thank you for your feedback')
        return redirect(url_for('get_review', business_id = business.id))
    return render_template('review.html', form = form)


#route to get all reviews
@app.route('/business/<int:business_id>/reviews')
def get_review(business_id):
    reviews = Review.query.get_or_404(business_id)
    return render_template('all_reviews.html', reviews = reviews)


    
def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',sender='geezerP@yahoo.com',recipients=[user.email])

    msg.body=f'''To reset your password,visit the following link:
{url_for('reset_token',token=token,_external=True)}
If you did not make this request then simply ignore this message and no change will be made.
'''
    mail.send(msg)   

@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',form=form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',form=form)


from .forms import SignupForm, LoginForm
from . import auth
import requests
from flask import request, redirect, url_for, render_template, flash
from app.models import User, db
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        user = User(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Hello {user.first_name}, thanks for signing up!', 'success')
        return redirect(url_for('auth.login'))
        
    else:
        return render_template('signup.html', form=form)

@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        
        queried_user = User.query.filter(User.email == email).first()
        print(f"Query: {User.query.filter(User.email == email)}")
        print(f"Queried User: {queried_user}")

        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello {queried_user.first_name}', 'success') 
            return redirect(url_for('main.profile'))
        else:
            flash('No Such User', 'danger')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
    
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'danger')
    return redirect(url_for('auth.login'))
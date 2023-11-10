from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from .forms import selectPokemon, SignupForm, LoginForm
from .models import User
from .models import db  
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def pokemonForm():
    form = selectPokemon()
    if request.method == 'POST':
        pokemonName = request.form['pokemon'].lower()
        r = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1292')
        data = r.json()['results']
        pokemonUrl = ''
        for pokemon in data:
            if pokemon["name"] == pokemonName:
                pokemonUrl = pokemon['url']
                break
        if pokemonUrl:
            stats = requests.get(pokemonUrl).json()
            return render_template('card.html', pokemonName=pokemonName, stats=stats)
        else:
            return render_template('holyshit.html')
    else:
        return render_template('pokemonForm.html', form=form)

@app.route('/card')
def card():
    pokemonName = "Charizar"
    return render_template('card.html', pokemonName=pokemonName)

@app.route('/holyshit', methods=["GET", "POST"])
def holyShit():
    if request.method == "GET":
        return render_template('holyshit.html')
    else:
        return render_template('pokemonForm.html')

@app.route('/signup', methods=["GET", "POST"])
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
        return redirect(url_for('login'))
        
    else:
        return render_template('signup.html', form=form)
    
@app.route('/profile', methods=["GET"])
def profile():
    if current_user.is_authenticated:
        name = current_user.first_name
    else:
        name = "Someone"
    return render_template('profile.html', name=name)

@app.route('/login', methods=["GET", "POST"])
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
            return redirect(url_for('profile'))
        else:
            flash('No Such User', 'danger')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
    
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'danger')
    return redirect(url_for('login'))
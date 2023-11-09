from flask import request, render_template,redirect, url_for

import requests
from app import app
from .forms import selectPokemon, SignupForm, LoginForm


myPokemons = []
REGISTERED_USERS = [{'email': 'lee@leedyer.com', 'password': 'lee'}]

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
        for user in REGISTERED_USERS:
            print(user)
            # if user['email'] == email:
            #     return "User already registered, please login" #change to an error.html with nav
        REGISTERED_USERS.append({(first_name + ' ' + last_name):{'email': email, 'password': password}})
        print(REGISTERED_USERS)
        return render_template('profile.html')
        
    else:
        return render_template('signup.html', form=form)
    
@app.route('/profile', methods=["GET"])
def profile():
    return render_template('profile.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']
        for user in REGISTERED_USERS:
            if user['email'] == email:
                if user['password'] == password:
                    return render_template('profile.html')
        return render_template('holyShit.html')
    else:
        return render_template('login.html', form=form)
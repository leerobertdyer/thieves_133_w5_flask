import requests
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from . import main
from .forms import selectPokemon
from app.models import db, Pokemon, User

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    form = selectPokemon
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', form=form))
    else:
        return redirect(url_for('auth.login'))
    
@main.route('/card') #Unneeded route
def card():
    pokemonName = "Charizar"
    return render_template('/includes/card.html', pokemonName=pokemonName)

@main.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        team = user.team
        all_pokemons = Pokemon.query.all()
        print(all_pokemons)
        print(team)
        form = selectPokemon()
        if request.method == 'POST':
            pokemonName = request.form['pokemon'].lower()
            if len(team) > 5:
                flash(f"{user.username}'s team is full!", 'danger') 
                return render_template('profile.html', form=form)
            if pokemonName in team:
                flash(f"{pokemonName} is already on your team! Try another...", 'warning')
                return redirect(url_for('main.profile'))    
            elif pokemonName in all_pokemons:
                user = User.query.get(current_user.id)
                pokemon = Pokemon.query.get(pokemonName)
                #ADD TO THE USERS TEAM
                #RETURN A RENDER OF THE PROFILE WITH NEW TEAM  
            else:
                r = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=1292')
                data = r.json()['results']
                pokemonUrl = ''
                for pokemon in data:
                    if pokemon["name"] == pokemonName:
                        pokemonUrl = pokemon['url']
                        break
                if pokemonUrl:
                    statsGrabber = requests.get(pokemonUrl).json()
                    sprite = statsGrabber['sprites']['other']['official-artwork']['front_default']
                    ability = statsGrabber['abilities'][0]['ability']['name']
                    hp = statsGrabber['stats'][0]['base_stat']
                    att = statsGrabber['stats'][1]['base_stat']
                    df = statsGrabber['stats'][2]['base_stat'] #NEED TO ADD THE DATABASE STUFF HERE...
                    
                    return render_template('profile.html', user=user, pokemonName=pokemonName, sprite=sprite, ability=ability, hp=hp, att=att, df=df, loggedIn=True, form=form)
                else:
                    return render_template('holyshit.html')
        else:
            return render_template('profile.html', form=form, team=team, user=user)        
    else:
        return redirect(url_for('auth.login'))


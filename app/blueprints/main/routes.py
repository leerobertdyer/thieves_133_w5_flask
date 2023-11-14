import requests
from flask import render_template, request
from flask_login import current_user
from . import main
from .forms import selectPokemon

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
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

@main.route('/card')
def card():
    pokemonName = "Charizar"
    return render_template('card.html', pokemonName=pokemonName)

@main.route('/profile', methods=["GET"])
def profile():
    if current_user.is_authenticated:
        name = current_user.first_name
    else:
        name = "Someone"
    return render_template('profile.html', name=name)
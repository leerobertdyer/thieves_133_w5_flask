from flask import Flask, render_template, request
import requests

app = Flask(__name__)

myPokemons = []

@app.route('/', methods=['GET', 'POST'])
def pokemonForm():
    if request.method == 'POST':
        pokemonName = request.form['pokemonName'].lower()
        r = requests.get('https://pokeapi.co/api/v2/pokemon/')
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
            return render_template('pokemonForm.html')
    else:
        return render_template('pokemonForm.html')

@app.route('/card')
def card():
    pokemonName = "Charizar"
    return render_template('card.html', pokemonName=pokemonName)

@app.route('/holyshit')
def holyShit():
    return render_template('holyshit.html')


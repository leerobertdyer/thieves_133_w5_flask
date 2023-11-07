from flask import Flask, render_template, request
import requests

app = Flask(__name__)

myPokemons = []

@app.route('/', methods=['GET', 'POST'])
def pokemonForm():
    if request.method == 'POST':
        pokemonName = request.form['pokemonName'].lower()
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
        return render_template('pokemonForm.html')

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


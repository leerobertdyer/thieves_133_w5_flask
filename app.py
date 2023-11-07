from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def pokemonForm():
    return render_template('pokemonForm.html')

@app.route('/card')
def card():
    return render_template('card.html')
@app.route('/holyshit')
def holyShit():
    return render_template('holyshit.html')


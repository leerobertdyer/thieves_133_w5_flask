import requests
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from . import main
from .forms import selectPokemon
from app.models import db, Pokemon, User

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    form = selectPokemon()
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', form=form))
    else:
        return redirect(url_for('auth.login'))
    
@main.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        team = user.team
        all_pokemons = Pokemon.query.all()
        print('all_pokemons: ', all_pokemons)
        form = selectPokemon()
        if request.method == 'POST':
            pokemonName = request.form['pokemon'].lower()
            pokemonExists = any(pokemonName == pokemon.name for pokemon in team)
            pokemonFound = any(pokemonName == pokemon.name for pokemon in all_pokemons)
            if user.team.count() > 5:
                print("right here", user.team.count())
                flash(f"{user.username}'s team is full!", 'danger') 
                return render_template('profile.html', form=form)
            if pokemonExists:
                flash(f"{pokemonName} is already on your team! Try another...", 'warning')
                return render_template('profile.html', form=form) 
            elif pokemonFound:
                pokemon = Pokemon.query.get(pokemonName)
                user.team.append(pokemon)
                db.session.commit()
                return render_template('profile.html', form=form)
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
                    pokemon = Pokemon(
                        name=pokemonName,
                        sprite=sprite,
                        ability=ability,
                        hp=hp,
                        att=att,
                        df=df
                    )
                    user.team.append(pokemon)
                    db.session.commit()
                    return render_template('profile.html', form=form)
                else:
                    return render_template('holyshit.html', pokemonName=pokemonName)
        else:
            return render_template('profile.html', form=form)        
    else:
        return redirect(url_for('auth.login'))

@main.route('/delete/<pokemon>')
@login_required
def delete(pokemon):
    teamMember = Pokemon.query.get(pokemon)
    if teamMember:
        current_user.team.remove(teamMember)
        db.session.commit()
        flash(f"You have released the {teamMember.name}!", 'danger')
        return redirect(url_for('main.home'))

@main.route('/fight<team>')
def fight(team):
    return render_template('fight.html')
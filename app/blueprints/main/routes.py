import requests
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from . import main
from .forms import selectPokemon
from app.models import db, Pokemon, User
import random

@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    form = selectPokemon()
    if current_user.is_authenticated:
        return redirect(url_for('main.profile', form=form))
    else:
        return redirect(url_for('auth.login'))
    
@main.route('/profile', methods=["GET", "POST"])
def profile():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        team = user.team
        print('team: ', team)
        for poke in team:
            print(poke)
        all_pokemons = Pokemon.query.all()
        print('all_pokemons: ', all_pokemons)
        form = selectPokemon()
        if request.method == 'POST':
            pokemonName = request.form['pokemon'].lower()
            pokemonExists = any(pokemonName == pokemon.name for pokemon in team)
            pokemonFound = any(pokemonName == pokemon.name for pokemon in all_pokemons)
            if user.team.count() > 5:
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
                    flash(f"{pokemonName} not found! Please try again...", "danger")
                    return render_template('profile.html', form=form)
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
    
@main.route('/fight', methods=["GET", "POST"])
@login_required
def fight():
    opponent = request.args.get('opponent')
    user2 = User.query.filter_by(username=opponent).first()
    # print('opponent: ', opponent)
    # print('opposingTeam: ', opposingTeam)
    if len(current_user.team.all()) < 1:
        print(f'{current_user.username} LOST!')
        flash(f'{current_user.username} LOST!', 'danger')
        return redirect(url_for("main.profile"))
    elif len(user2.team.all()) < 1:
        print(f'{current_user.username} wins!', 'success')
        flash(f'{current_user.username} wins!', 'success')
        return redirect(url_for('main.profile'))
    rand1 = random.choice(current_user.team.all())
    rand2 = random.choice(user2.team.all())
    print(rand1.to_dict())
    print(rand2.to_dict())
    def battle(p1, p2):
        r1 = p1.to_dict()
        r2 = p2.to_dict()
        while r1['hp'] > 0 and r2['hp'] > 0:
            r2['df'] = r2['df'] - r1['att']
            print('after a hit from p1, p2s df = ', r2['df'])
            if r2['df'] < 0:
                print('p2s df was destroyed, remaining dmg = ', r2['df'])
                r2['hp'] = r2['hp'] + r2['df']
                print('p2 now has ', r2['hp'], 'hit points')
            r1['df'] = r1['df'] - r2['att']
            print('after a hit from p2, p1s df = ', r1['df'])
            if r1['df'] < 0:
                print('p1s def was destroyed, remaining dmg = ', r1['df'])
                r1['hp'] = r1['hp'] + r1['df']
                print('p1 now has ', r1['hp'], 'hit points')
            print('Round over, going back to p1 att...')
            if r1['hp'] <= 0:
                print(f"{current_user.username} lost their {r1['name']}!")
                flash(f"{current_user.username} lost their {r1['name']}!", 'danger')
                current_user.team.remove(p1)
                return 'p1'
            elif r2['hp'] <= 0:
                print(f"{user2.username} lost their {r2['name']}!")
                flash(f"{user2.username} lost their {r2['name']}!", 'danger')
                user2.team.remove(p2)
                return 'p2'
    xDiv = battle(rand1, rand2)
    db.session.commit()
    return render_template('fight.html', index=0, opponent=opponent, p1=rand1.to_dict(), p2=rand2.to_dict(), xDiv=xDiv)

@main.route('/waiting-room', methods=["GET", "POST"])
def waiting_room():
    readyPlayers = {}
    all_users = User.query.all()
    for user in all_users:
        if user.team.count() == 6:
            readyPlayers[user.username] = [pokemon.name for pokemon in user.team.all()]
    print(readyPlayers)
    return render_template('waiting_room.html', readyPlayers=readyPlayers)


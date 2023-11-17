from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class selectPokemon(FlaskForm):
    pokemon = StringField('Pokemon: ', validators=[DataRequired()])
    submit =  SubmitField('Submit')
    
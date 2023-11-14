from . import errors
from flask import render_template, request

@errors.route('/holyshit', methods=["GET", "POST"])
def holyShit():
    if request.method == "GET":
        return render_template('holyshit.html')
    else:
        return render_template('pokemonForm.html')


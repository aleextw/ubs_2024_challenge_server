from flask import Blueprint, render_template

from utils import constants

instructions_blueprint = Blueprint('instructions_blueprint', __name__)


@instructions_blueprint.get(constants.ASTEROID_ROOT)
def asteroid_instructions():
    return render_template("markdown.html", title="Asteroid", filename=constants.ASTEROID_ROOT)


@instructions_blueprint.get(constants.DECODER_ROOT)
def decoder_instructions():
    return render_template("markdown.html", title="Decoder", filename=constants.DECODER_ROOT)

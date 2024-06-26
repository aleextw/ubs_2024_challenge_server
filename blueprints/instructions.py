from flask import Blueprint, render_template

from utils import constants

instructions_blueprint = Blueprint("instructions_blueprint", __name__)


@instructions_blueprint.get(constants.LAB_WORK_ROOT)
def lab_work_instructions():
    return render_template(
        "markdown.html", title="Lab Work", filename=constants.LAB_WORK_ROOT
    )

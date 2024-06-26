import time

from flask import Blueprint, request, jsonify

from utils import constants
from utils.utils import get_logger

challenger_blueprint = Blueprint("challenger_blueprint", __name__)


logger = get_logger()


@challenger_blueprint.post(constants.LAB_WORK_CHALLENGER)
def lab_work_challenger():
    start = time.time()
    json_request = request.json
    test_cases = json_request["test_cases"]
    from manager.challenger_manager import get_latest_answer_stored

    formatted_answers = get_latest_answer_stored().answer

    end = time.time()
    time_elapsed = round(end - start, 2)
    logger.info(
        "solved "
        + str(len(test_cases))
        + " lab work testcases in "
        + str(time_elapsed)
        + " seconds"
    )

    ### Fake challenger testing ###
    # Empty response
    # formatted_answers = []

    # Partial response
    # formatted_answers = formatted_answers[:2]

    # Full response, wrong answers
    # formatted_answers[0]["1000"][-1] = 5
    # formatted_answers[0]["2000"][-1] = 5

    # Excessive response
    # formatted_answers = formatted_answers + formatted_answers

    return jsonify(formatted_answers), 200

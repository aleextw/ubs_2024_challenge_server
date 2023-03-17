import json
import logging
import os


def get_logger():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger()


logger = get_logger()

import requests
from passlib.context import CryptContext
from utils import constants
from utils.constants import REQUEST_TIMEOUT, TO_GUESS, POSSIBLE_VALUES, NUM_SLOTS, HISTORY, DECODER_ROOT

MODE = None


def set_mode(mode):
    global MODE
    MODE = mode


def get_mode():
    return MODE


def generate_status(error_message):
    status = constants.PASS
    if error_message != "":
        status = constants.FAIL + " - " + error_message

    return status


def call_team_url_verify_answer(team_url, question_endpoint, parameters):
    output_received = {}
    response = {}
    url_to_call = team_url + question_endpoint
    error_message = ""
    try:
        if question_endpoint == DECODER_ROOT:
            to_guess = parameters[TO_GUESS]
            possible_values = parameters[POSSIBLE_VALUES]
            from processing_logic.decoder import format_attempt_history, verify_decoder_answer
            history = format_attempt_history(parameters[HISTORY])
            active_session = parameters["active_session"]

            decoder_parameters = {POSSIBLE_VALUES: possible_values, NUM_SLOTS: len(to_guess), HISTORY: history}
            response = requests.post(url_to_call, json=decoder_parameters, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            output_received = response.json()
            error_message, points_scored = verify_decoder_answer(to_guess, output_received["answer"], len(history),
                                                                 team_url, active_session)
            return output_received, points_scored, error_message

        else:
            test_cases = parameters["test_cases"]
            answers = parameters["answers"]
            max_points = parameters["max_points"]
            response = requests.post(url_to_call, json=test_cases, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            output_received = response.json()
            error_message, points_scored = verify_answers(output_received, answers, max_points)
            return output_received, points_scored, error_message

    except requests.exceptions.Timeout:
        error_message = "request timed out"
    except requests.exceptions.InvalidURL:
        error_message = "invalid teamUrl"
    except Exception as error:
        error_message = "team server failed to process with an error of " + str(error)
        logger.info("team server " + url_to_call + " has a request code of " + str(error))

    return output_received, 0, error_message


def call_coordinator_url_post_score(callbackUrl, runId, scoreObtained, message):
    error_message = ""
    try:
        headers, payload = format_response_to_coordinator(runId, scoreObtained, message)
        if callbackUrl != "":
            if len(headers) > 0:
                r = requests.post(callbackUrl, json=payload,
                                  headers=headers, timeout=10)
            else:
                r = requests.post(callbackUrl, json=payload, timeout=10)
            logger.info("request posted to coordinator with status code: " + str(r.status_code))

            if r.status_code != 200:
                error_message = "status code: " + str(r.status_code) + ", response: " + str(r.text)

    except requests.exceptions.Timeout:
        logger.info("request to coordinator timed out")
        error_message = "request to coordinator timed out"
    except requests.exceptions.HTTPError:
        logger.info("invalid callbackUrl")
        error_message = "invalid callbackUrl"
    finally:
        return error_message


def verify_answers(output_received, output_expected, max_points):
    points_scored = 0
    error_message = ""
    try:
        score_per_test_case = max_points / len(output_expected)
        if len(output_received) != len(output_expected):
            error_message = "missing testcase from response"
        else:
            for answer in output_received:
                test_case = answer["input"]

                if test_case in output_expected:
                    if answer["origin"] == output_expected[test_case]["origin"] and answer["score"] == \
                            output_expected[test_case]["score"]:
                        points_scored += score_per_test_case
                else:
                    continue
    except KeyError as e:
        error_message = "missing "+str(e)+" key from response"
    except Exception as e:
        print(e)
        error_message = "missing answers from response"
    return error_message, int(points_scored)


def format_response_to_coordinator(runId, scoreObtained, message):
    try:
        access_token = os.environ['AUTH_TOKEN']

        headers = {"Authorization": access_token}

        payload = {"runId": runId,
                   "score": str(int(scoreObtained)),
                   "message": message}


    except KeyError as e:
        headers = {}
        payload = {"runId": runId,
                   "score": str(int(scoreObtained)),
                   "message": message
                   }

    return headers, payload


def convert_string_to_list(convert_string):
    return json.loads(convert_string)


def verify_hash(plaintext):
    myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
    myctx.default_scheme()
    password_hash = '$5$rounds=535000$D4XUeAh/sysM87zq$sKqtnCqEML5OQb3PyR4jeQ/SmzsOCd0Ua9fF.khYJP6'
    try:
        if os.environ['MODE'] == "DEV" or os.environ['MODE'] == "PROD":
            password_hash = '$5$rounds=535000$6XJaEAIDqBAn.Q0e$q0VO79bWtkzG9rl7AkOi0mQvosm39leY7wP7erBrG95'

    except KeyError as e:
        password_hash = '$5$rounds=535000$D4XUeAh/sysM87zq$sKqtnCqEML5OQb3PyR4jeQ/SmzsOCd0Ua9fF.khYJP6'
    return myctx.verify(plaintext, password_hash)


def create_hash(plaintext):
    myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
    myctx.default_scheme()
    return myctx.hash(plaintext)

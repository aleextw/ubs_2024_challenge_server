import logging
import os

import requests
from passlib.context import CryptContext
from utils import constants
from utils.constants import (
    REQUEST_TIMEOUT,
)
from itertools import zip_longest


def get_logger():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger()


logger = get_logger()


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
        test_cases = parameters["test_cases"]
        answers = parameters["answers"]
        max_points = parameters["max_points"]
        response = requests.post(url_to_call, json=test_cases, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        output_received = response.json()
        error_message, points_scored = calculate_score(
            output_received, answers, max_points
        )

        return output_received, points_scored, error_message

    except requests.exceptions.Timeout:
        error_message = "request timed out"
    except requests.exceptions.InvalidURL:
        error_message = "invalid teamUrl"
    except Exception as error:
        error_message = "team server failed to process with an error of " + str(error)
        logger.info(
            "team server " + url_to_call + " has a request code of " + str(error)
        )

    return output_received, 0, error_message


def call_coordinator_url_post_score(callbackUrl, runId, scoreObtained, message):
    error_message = ""
    try:
        headers, payload = format_response_to_coordinator(runId, scoreObtained, message)
        if callbackUrl != "":
            if len(headers) > 0:
                r = requests.post(
                    callbackUrl, json=payload, headers=headers, timeout=10
                )
            else:
                r = requests.post(callbackUrl, json=payload, timeout=10)
            logger.info(
                "request posted to coordinator with status code: " + str(r.status_code)
            )

            if r.status_code != 200:
                error_message = (
                    "status code: " + str(r.status_code) + ", response: " + str(r.text)
                )

    except requests.exceptions.Timeout:
        logger.info("request to coordinator timed out")
        error_message = "request to coordinator timed out"
    except requests.exceptions.HTTPError:
        logger.info("invalid callbackUrl")
        error_message = "invalid callbackUrl"
    finally:
        return error_message


def calculate_score(actual: dict, expected: dict, max_points: int) -> int:
    """
    If a line is wrong, skips it and proceeds to the next line (if exists)

    If team submission is only partial, will return partial score
    """
    score = 0
    error_message = ""
    increment = max_points // (len(expected) * 10)

    try:
        if len(actual) > len(expected):
            error_message += "Response longer than anticipated,"
            actual = actual[: len(expected)]

        for team_answer, expected_answer in zip_longest(actual, expected):
            if team_answer is None:
                error_message += "Missing testcase(s) from response,"
                break

            for k, v in expected_answer.items():
                if (comp := team_answer.get(k, None)) is None:
                    error_message += "Partial submission(s) for testcase(s),"
                    break

                for a, b in zip_longest(v, comp):
                    if b is None or a != b:
                        break
                else:
                    score += increment
    except Exception as e:
        print(e)
        error_message = "Missing answers from response,"

    return error_message, score


def format_response_to_coordinator(runId, scoreObtained, message):
    try:
        access_token = os.environ["AUTH_TOKEN"]

        headers = {"Authorization": access_token}

        payload = {"runId": runId, "score": str(int(scoreObtained)), "message": message}

    except KeyError:
        headers = {}
        payload = {"runId": runId, "score": str(int(scoreObtained)), "message": message}

    return headers, payload


def verify_hash(plaintext):
    myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
    myctx.default_scheme()
    password_hash = (
        "$5$rounds=535000$8q2XTj3WzvqmyVCp$mQMt42CrEZ4jfbKr1Fr9wiSJ/XZuoyvsZpBD6JY93i/"
    )
    try:
        if os.environ["MODE"] == "DEV" or os.environ["MODE"] == "PROD":
            password_hash = "$5$rounds=535000$9pOjWdILslH.ciiD$/nDLz.OOKJMuosBx8TSJR3qNCDIlKnyl0X3KsVSz6v."

    except KeyError:
        password_hash = "$5$rounds=535000$8q2XTj3WzvqmyVCp$mQMt42CrEZ4jfbKr1Fr9wiSJ/XZuoyvsZpBD6JY93i/"
    return myctx.verify(plaintext, password_hash)


def create_hash(plaintext):
    myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
    myctx.default_scheme()
    return myctx.hash(plaintext)

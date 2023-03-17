import os

from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

try:
    if os.environ['MODE'] == "DEV" or os.environ['MODE'] == "PROD":
        print("starting up with environment:", os.environ['MODE'])
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'].replace("://", "ql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

except KeyError as e:
    print("starting up with environment: LOCAL")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "codeitsuisse.db"))

    app.config["SQLALCHEMY_DATABASE_URI"] = database_file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Base = declarative_base()

from utils import constants
from utils.constants import ALERT_RECORDS, TO_GUESS, POSSIBLE_VALUES, HISTORY, DECODER_ROOT

from blueprints.simulate_challenger import challenger_blueprint
from blueprints.instructions import instructions_blueprint

from manager.record_manager import get_all_records, delete_records, count_records, add_record, get_latest_records
from utils.utils import get_logger, verify_hash, call_team_url_verify_answer, call_coordinator_url_post_score, \
    generate_status, set_mode
from processing_logic import decoder, asteroid

try:
    if os.environ['MODE'] == "DEV" or os.environ['MODE'] == "PROD":
        set_mode(os.environ['MODE'])
except:
    set_mode("LOCAL")

logger = get_logger()

db.create_all()
app.register_blueprint(instructions_blueprint)
app.register_blueprint(challenger_blueprint)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/vnd.microsoft.icon')


@app.post('/latestrecords')
def latest_records_endpoint():
    json_request = request.json
    password = json_request['password']
    if verify_hash(password):
        return jsonify(get_latest_records())
    else:
        response = {'error': "unauthorized access"}
        return jsonify(response), 401


@app.post('/countrecords')
def count_records_endpoint():
    json_request = request.json
    password = json_request['password']
    if verify_hash(password):
        return jsonify(count_records())
    else:
        response = {'error': "unauthorized access"}
        return jsonify(response), 401


@app.post('/deleterecords')
def delete_records_endpoint():
    logger.info("received a request to delete records")
    json_request = request.json
    password = json_request['password']
    if verify_hash(password):
        start, end = delete_records()
        response = {'message': "deleted records with recordId from " + str(start) + " to " + str(end)}
        return jsonify(response), 200
    else:
        response = {'error': "unauthorized access"}
        return jsonify(response), 401


@app.post('/allrecords')
def return_all_records():
    json_request = request.json
    password = json_request['password']
    if verify_hash(password):
        return jsonify(get_all_records())
    else:
        response = {'error': "unauthorized access"}
        return jsonify(response), 401


@app.post(constants.DECODER_EVALUATE)
def decoder_evaluate():
    json_request = request.json
    logger.info("Evaluation Request received for decoder")
    logger.info(json_request)

    output_expected, possible_values, previous_attempts, active_session = decoder.get_question_for_team(json_request)
    parameters = {
        TO_GUESS: output_expected,
        POSSIBLE_VALUES: possible_values,
        HISTORY: previous_attempts,
        "answers": output_expected,
        "active_session": active_session
    }

    return evaluate(json_request,
                    parameters,
                    constants.DECODER_EVALUATE,
                    constants.DECODER_ROOT)


@app.post(constants.ASTEROID_EVALUATE)
def asteroid_evaluate():
    json_request = request.json
    logger.info("Evaluation Request received for Asteroid")
    logger.info(json_request)

    answers, test_cases = asteroid.generate_test_cases(constants.ASTEROID_TEST_CASES)

    parameters = {
        "test_cases": test_cases,
        "answers": answers,
        "max_points": constants.ASTEROID_MAX_POINTS
    }

    return evaluate(json_request,
                    parameters,
                    constants.ASTEROID_EVALUATE,
                    constants.ASTEROID_ROOT)


def evaluate(json_request, parameters, url_endpoint, question_endpoint):
    team_url = json_request['teamUrl']
    if team_url.endswith("/"):
        team_url = team_url[:-1]

    output_received, score, error_message = call_team_url_verify_answer(team_url, question_endpoint,
                                                                        parameters)
    status = generate_status(error_message)

    coordinator_error_message = call_coordinator_url_post_score(json_request['callbackUrl'], json_request['runId'],
                                                                score, status)

    if question_endpoint == DECODER_ROOT:
        answers = parameters[TO_GUESS]
        add_record(json_request['runId'], url_endpoint, answers, output_received, answers, score,
                   coordinator_error_message, status, team_url)
    else:
        test_cases = parameters["test_cases"]
        answers = parameters["answers"]
        add_record(json_request['runId'], url_endpoint, test_cases, output_received, answers, score,
                   coordinator_error_message, status, team_url)

    if count_records() >= ALERT_RECORDS:
        logger.error("approaching max row limit for db, please purge some records")

    if status == constants.PASS:
        return "", 200
    else:
        return jsonify({"message": status}), 400


if __name__ == '__main__':
    app.run()

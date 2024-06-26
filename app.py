import os

from utils.db import db
from flask import Flask, request, jsonify, send_from_directory
from sqlalchemy.orm import declarative_base

app = Flask(__name__)

try:
    if os.environ["MODE"] == "DEV" or os.environ["MODE"] == "PROD":
        print("starting up with environment:", os.environ["MODE"])
        SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
        app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

except KeyError:
    print("starting up with environment: LOCAL")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "codeitsuisse.db"))

    app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db.init_app(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Base = declarative_base()

from utils import constants
from utils.constants import (
    ALERT_RECORDS,
)

from blueprints.simulate_challenger import challenger_blueprint
from blueprints.instructions import instructions_blueprint
from blueprints.simulate_coordinator import coordinator_blueprint

from manager.record_manager import (
    get_all_records,
    delete_records,
    count_records,
    add_record,
    get_latest_records,
)
from utils.utils import (
    get_logger,
    verify_hash,
    call_team_url_verify_answer,
    call_coordinator_url_post_score,
    generate_status,
    set_mode,
)
from processing_logic import lab_work

try:
    if os.environ["MODE"] == "DEV" or os.environ["MODE"] == "PROD":
        set_mode(os.environ["MODE"])
except Exception:
    set_mode("LOCAL")

logger = get_logger()

with app.app_context():
    db.create_all()

app.register_blueprint(instructions_blueprint)
app.register_blueprint(challenger_blueprint)
app.register_blueprint(coordinator_blueprint)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.post("/latestrecords")
def latest_records_endpoint():
    json_request = request.json
    password = json_request["password"]
    if verify_hash(password):
        return jsonify(get_latest_records())
    else:
        response = {"error": "unauthorized access"}
        return jsonify(response), 401


@app.post("/countrecords")
def count_records_endpoint():
    json_request = request.json
    password = json_request["password"]
    if verify_hash(password):
        return jsonify(count_records())
    else:
        response = {"error": "unauthorized access"}
        return jsonify(response), 401


@app.post("/deleterecords")
def delete_records_endpoint():
    logger.info("received a request to delete records")
    json_request = request.json
    password = json_request["password"]
    if verify_hash(password):
        start, end = delete_records()
        response = {
            "message": "deleted records with recordId from "
            + str(start)
            + " to "
            + str(end)
        }
        return jsonify(response), 200
    else:
        response = {"error": "unauthorized access"}
        return jsonify(response), 401


@app.post("/allrecords")
def return_all_records():
    json_request = request.json
    password = json_request["password"]
    if verify_hash(password):
        return jsonify(get_all_records())
    else:
        response = {"error": "unauthorized access"}
        return jsonify(response), 401


@app.get("/healthcheck")
def healthcheck_endpoint():
    return jsonify({}), 200


@app.post(constants.LAB_WORK_EVALUATE)
def lab_work_evaluate():
    json_request = request.json
    logger.info("Evaluation Request received for Lab Work")
    logger.info(json_request)

    answers, test_cases = lab_work.generate_test_cases(constants.LAB_WORK_TEST_CASES)

    parameters = {
        "test_cases": test_cases,
        "answers": answers,
        "max_points": constants.LAB_WORK_MAX_POINTS,
    }

    return evaluate(
        json_request, parameters, constants.LAB_WORK_EVALUATE, constants.LAB_WORK_ROOT
    )


def evaluate(json_request, parameters, url_endpoint, question_endpoint):
    team_url = json_request["teamUrl"]
    if team_url.endswith("/"):
        team_url = team_url[:-1]

    output_received, score, error_message = call_team_url_verify_answer(
        team_url, question_endpoint, parameters
    )
    status = generate_status(error_message)

    coordinator_error_message = call_coordinator_url_post_score(
        json_request["callbackUrl"], json_request["runId"], score, status
    )

    test_cases = parameters["test_cases"]
    answers = parameters["answers"]
    add_record(
        json_request["runId"],
        url_endpoint,
        test_cases,
        output_received,
        answers,
        score,
        coordinator_error_message,
        status,
        team_url,
    )

    if count_records() >= ALERT_RECORDS:
        logger.error("approaching max row limit for db, please purge some records")

    if status == constants.PASS:
        return "", 200
    else:
        return jsonify({"message": status}), 400


if __name__ == "__main__":
    app.run()

from flask import Blueprint, request, jsonify

from utils import constants
from utils.utils import get_logger

coordinator_blueprint = Blueprint("coordinator_blueprint", __name__)


logger = get_logger()


@coordinator_blueprint.post(constants.COORDINATOR)
def coordinator():
    json_request = request.json
    logger.info(f"received payload: {json_request}")
    return jsonify({}), 200

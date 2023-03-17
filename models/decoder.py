from dataclasses import dataclass
from datetime import datetime

import pytz
from sqlalchemy import Sequence

from app import db


@dataclass
class DecoderRecord(db.Model):
    tz = pytz.timezone('Asia/Singapore')
    date_time: str
    attemptId: int
    team_url: str
    run_id: str
    session: str
    output_expected: list
    output_received: list
    possible_values: list
    right_colour_right_position: int
    right_colour_wrong_position: int
    score: int
    coordinator_error_message: str
    status: str

    date_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now(tz))
    attemptId = db.Column(db.Integer, Sequence('attempt_id_seq', metadata=db.Model.metadata), primary_key=True)
    team_url = db.Column(db.Text, nullable=False)
    run_id = db.Column(db.Text, nullable=False)
    session = db.Column(db.Text, nullable=False)
    output_expected = db.Column(db.PickleType, nullable=False)
    output_received = db.Column(db.PickleType, nullable=True)
    possible_values = db.Column(db.PickleType, nullable=False)
    right_colour_right_position = db.Column(db.Integer, nullable=True)
    right_colour_wrong_position = db.Column(db.Integer, nullable=True)
    score = db.Column(db.Integer, nullable=True)
    coordinator_error_message = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=True)

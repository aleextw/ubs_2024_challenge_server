from dataclasses import dataclass
from datetime import datetime

import pytz
from sqlalchemy import Sequence

from app import db


@dataclass
class Record(db.Model):
    tz = pytz.timezone('Asia/Singapore')
    recordId: int
    runId: str
    urlCalled: str
    testCases: list
    outputReceived: list
    outputExpected: list
    scoreGiven: int
    dateTime: str
    coordinatorErrorMessage: str
    status: str
    teamUrl: str

    recordId = db.Column(db.Integer, Sequence('record_id_seq', metadata=db.Model.metadata), primary_key=True)
    runId = db.Column(db.Text, nullable=False)
    urlCalled = db.Column(db.Text, nullable=False)
    testCases = db.Column(db.PickleType, nullable=False)
    outputReceived = db.Column(db.PickleType, nullable=False)
    outputExpected = db.Column(db.PickleType, nullable=False)
    scoreGiven = db.Column(db.Integer, nullable=False)
    dateTime = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now(tz))
    teamUrl = db.Column(db.Text, nullable=False)
    coordinatorErrorMessage = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)

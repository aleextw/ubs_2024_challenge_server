from dataclasses import dataclass

from sqlalchemy import Sequence

from utils.db import db


@dataclass
class ChallengerAnswer(db.Model):
    answerId: int
    answer: dict

    answerId = db.Column(
        db.Integer,
        Sequence("answer_id_seq", metadata=db.Model.metadata),
        primary_key=True,
    )
    answer = db.Column(db.PickleType, nullable=False)

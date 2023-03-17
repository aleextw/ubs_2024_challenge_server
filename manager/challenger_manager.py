from sqlite3 import DatabaseError

from app import db
from models.challenger_answer import ChallengerAnswer


def create_answer(answer):
    return ChallengerAnswer(
        answer=answer
    )


def add_answer(answer):
    try:
        db.session.add(create_answer(answer))
        db.session.commit()
    except DatabaseError:
        print("No table found")


def get_latest_answer_stored():
    try:
        return db.session.query(ChallengerAnswer).order_by(
            ChallengerAnswer.answerId.desc()).first()
    except DatabaseError:
        print("No table found")

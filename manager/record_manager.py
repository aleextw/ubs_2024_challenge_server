from operator import and_

from app import db
from models.record import Record
from utils.constants import ROWS_TO_REMOVE


def create_record(runid, urlCalled, testCases, outputReceived, outputExpected, scoreGiven, errorMessage, status,
                  teamUrl):
    return Record(runId=runid, urlCalled=urlCalled, testCases=testCases, outputReceived=outputReceived,
                  outputExpected=outputExpected, scoreGiven=scoreGiven, coordinatorErrorMessage=errorMessage,
                  status=status, teamUrl=teamUrl)


def get_all_records():
    return db.session.query(Record).all()


def get_latest_records():
    return db.session.query(Record).order_by(Record.recordId.desc()).limit(20).all()


def get_first_record_id():
    record = db.session.query(Record).order_by(Record.recordId.asc()).first()
    return record.recordId


def delete_records():
    first_record_id = get_first_record_id()
    last_record_id = first_record_id
    for i in range(0, ROWS_TO_REMOVE - 1):
        last_record_id += 1
    db.session.query(Record).filter(
        and_(Record.recordId >= first_record_id, Record.recordId <= last_record_id)).delete()
    db.session.commit()
    return first_record_id, last_record_id


def count_records():
    return db.session.query(Record).count()


def add_record(runid, urlCalled, testCases, outputReceived, outputExpected, scoreGiven, errorMessage, status, teamUrl):
    db.session.add(create_record(runid, urlCalled, testCases, outputReceived, outputExpected, scoreGiven,
                                 errorMessage, status, teamUrl))
    db.session.commit()
    return db.session.query(Record).order_by(Record.recordId.desc()).first()

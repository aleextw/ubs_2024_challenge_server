from sqlite3 import DatabaseError

from app import db
from models.decoder import DecoderRecord


def create_decoder_record(output_expected, possible_values, session, json_request):
    return DecoderRecord(
        team_url=json_request["teamUrl"],
        run_id=json_request["runId"],
        session=session,
        output_expected=output_expected,
        possible_values=possible_values
    )


def update_current_attempt(team_url, session, output_received, right_colour_right_position, right_colour_wrong_position,
                           score, coordinator_error_message, status):
    decoder_record = db.session.query(DecoderRecord).filter_by(team_url=team_url, session=session) \
        .order_by(DecoderRecord.attemptId.desc()).first()
    try:
        decoder_record.output_received = output_received
        decoder_record.right_colour_right_position = right_colour_right_position
        decoder_record.right_colour_wrong_position = right_colour_wrong_position
        decoder_record.score = score
        decoder_record.coordinator_error_message = coordinator_error_message
        decoder_record.status = status
        print(decoder_record)
        db.session.commit()
    except AttributeError:
        print("No attribute found")
    except DatabaseError:
        print("No table found")


def add_decoder_record(output_expected, possible_values, active_session, json_request):
    try:
        db.session.add(create_decoder_record(output_expected, possible_values, active_session, json_request))
        db.session.commit()
    except DatabaseError:
        print("No table found")


def get_previous_decoder_records_by_team_and_session(team_url, session):
    try:
        return db.session.query(DecoderRecord).filter_by(team_url=team_url, session=session).order_by(
            DecoderRecord.attemptId.desc()).all()
    except DatabaseError:
        print("No table found")

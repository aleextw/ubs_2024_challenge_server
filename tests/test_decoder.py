import random

from app import db
from blueprints.simulate_challenger import derive_decoder_answer

from processing_logic.decoder import get_question_for_team, verify_decoder_answer, evaluate_answer, calculate_score, \
    get_result_as_integer
from utils import constants
from utils.constants import NUM_POSSIBLE_VALUES, NUM_SLOTS, DECODER_NUM_SLOTS

active_session = "21-21"
team_url = "abc"

SQLALCHEMY_DATABASE_URI = "sqlite://"
TESTING = True

db.create_all()


def test_get_question_for_team():
    json_request = {"teamUrl": "abc", "runId": "123"}
    to_guess, possible_values, history, local_test_session = get_question_for_team(json_request)
    assert len(possible_values) == constants.decoder_configuration[NUM_POSSIBLE_VALUES]
    assert len(to_guess) == constants.decoder_configuration[NUM_SLOTS]


def test_verify_decoder_answer_returns_error_when_submitted_array_is_unexpected_length():
    to_guess = ['a', 'b', 'f', 'd']
    submitted_answer = ['a', 'c', 'b', 'd', 'e']
    num_tries = 5

    error_msg, points_scored = verify_decoder_answer(to_guess, submitted_answer, num_tries, team_url, active_session)
    assert error_msg == "Submitted answer ['a', 'c', 'b', 'd', 'e'] does not match expected length of 4"
    assert points_scored == 0


def test_verify_decoder_answer():
    # when not correct
    to_guess = ['a', 'b', 'f', 'd', 'd']
    submitted_answer = ['a', 'c', 'b', 'd', 'e']
    num_tries = 4

    error_msg, points_scored = verify_decoder_answer(to_guess, submitted_answer, num_tries, team_url, active_session)
    assert error_msg == ""

    score_for_rr = 80 / DECODER_NUM_SLOTS
    score_for_rw = 80 / DECODER_NUM_SLOTS / 2
    assert points_scored == (score_for_rr * 2) + (score_for_rw * 1)

    # when correct and tries = 5
    to_guess = ['a', 'b', 'c', 'd', 'e']
    submitted_answer = ['a', 'b', 'c', 'd', 'e']
    num_tries = 5

    error_msg, points_scored = verify_decoder_answer(to_guess, submitted_answer, num_tries, team_url, active_session)
    assert error_msg == ""
    assert points_scored == 90

    # when correct and tries = 4
    to_guess = ['a', 'b', 'c', 'd', 'e']
    submitted_answer = ['a', 'b', 'c', 'd', 'e']
    num_tries = 4

    error_msg, points_scored = verify_decoder_answer(to_guess, submitted_answer, num_tries, team_url, active_session)
    assert error_msg == ""
    assert points_scored == 100

    # when correct and tries = 3
    to_guess = ['a', 'b', 'c', 'd', 'e']
    submitted_answer = ['a', 'b', 'c', 'd', 'e']
    num_tries = 3

    error_msg, points_scored = verify_decoder_answer(to_guess, submitted_answer, num_tries, team_url, active_session)
    assert error_msg == ""
    assert points_scored == 100


def test_evaluate_answer():
    to_guess = ['a', 'b', 'c', 'd']
    submitted_answer = ['d', 'c', 'b', 'a']
    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    assert right_symbol_right_position == 0
    assert right_symbol_wrong_position == 4

    to_guess = ['a', 'b', 'c', 'd']
    submitted_answer = ['e', 'd', 'c', 'g']
    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    assert right_symbol_right_position == 1
    assert right_symbol_wrong_position == 1

    to_guess = ['a', 'a', 'a', 'a']
    submitted_answer = ['b', 'b', 'b', 'b']
    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    assert right_symbol_right_position == 0
    assert right_symbol_wrong_position == 0

    to_guess = ['a', 'b', 'c', 'd']
    submitted_answer = ['a', 'b', 'c', 'd']
    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    assert right_symbol_right_position == 4
    assert right_symbol_wrong_position == 0


def test_evaluate_answer_should_not_award_score_for_duplicates():
    to_guess = ['a', 'b', 'a', 'd']
    submitted_answer = ['a', 'a', 'a', 'a']
    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    assert right_symbol_right_position == 2
    assert right_symbol_wrong_position == 0

    to_guess = ['a', 'a', 'a', 'd']
    submitted_answer = ['a', 'c', 'a', 'a']
    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    assert right_symbol_right_position == 2
    assert right_symbol_wrong_position == 1

    to_guess = ['a', 'b', 'c', 'd']
    submitted_answer = ['d', 'c', 'b', 'a']
    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    assert right_symbol_right_position == 0
    assert right_symbol_wrong_position == 4

    to_guess = ['a', 'b', 'b', 'b']
    submitted_answer = ['b', 'b', 'b', 'a']
    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    assert right_symbol_right_position == 2
    assert right_symbol_wrong_position == 2


def test_calculate_score():
    right_symbol_right_position = 1
    right_symbol_wrong_position = 2
    score = calculate_score(right_symbol_right_position, right_symbol_wrong_position)
    assert score == 32

    right_symbol_right_position = 0
    right_symbol_wrong_position = 1
    score = calculate_score(right_symbol_right_position, right_symbol_wrong_position)
    assert score == 8


def test_get_result_as_integer():
    right_symbol_right_position = 2
    right_symbol_wrong_position = 2
    result = get_result_as_integer(right_symbol_wrong_position, right_symbol_right_position)
    assert result == 22

    right_symbol_right_position = 1
    right_symbol_wrong_position = 0
    result = get_result_as_integer(right_symbol_wrong_position, right_symbol_right_position)
    assert result == 1

    right_symbol_right_position = 0
    right_symbol_wrong_position = 3
    result = get_result_as_integer(right_symbol_wrong_position, right_symbol_right_position)
    assert result == 30

    right_symbol_right_position = 0
    right_symbol_wrong_position = 0
    result = get_result_as_integer(right_symbol_wrong_position, right_symbol_right_position)
    assert result == 0


def test_challenger_logic():
    number_of_slots = 5
    possible_values = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    output_expected = random.choices(possible_values, k=number_of_slots)
    challenger_output = []
    history = []

    for i in range(0, 10):
        challenger_output = derive_decoder_answer(possible_values, number_of_slots, history)
        right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(output_expected, challenger_output)

        if right_symbol_right_position == number_of_slots:
            assert output_expected == challenger_output
            print("solved in", i, "moves")
            break

        int_result = get_result_as_integer(right_symbol_wrong_position, right_symbol_right_position)
        record = {'output_received': challenger_output, 'result': int_result}
        history.append(record)

    assert output_expected == challenger_output

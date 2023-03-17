import copy
import random
import string
from datetime import datetime, timedelta

from manager import decoder_manager
from manager.decoder_manager import update_current_attempt
from utils import constants
from utils.constants import NUM_SLOTS, NUM_POSSIBLE_VALUES, POINTS_FOR_RIGHT_SYMBOL_RIGHT_POSITION, \
    POINTS_FOR_RIGHT_SYMBOL_WRONG_POSITION, REMOVED, DECODER_BONUS_POINTS_FIRST_TIER, NUM_TRIES_FOR_FIRST_TIER, \
    NUM_TRIES_FOR_SECOND_TIER, DECODER_BONUS_POINTS_SECOND_TIER

alphabet_list = list(string.ascii_lowercase)


def get_current_session():
    now = datetime.now()
    now = now - timedelta(minutes=now.minute % 10,
                          seconds=now.second,
                          microseconds=now.microsecond)
    return now.strftime("%d-%H-%M")


def get_question_for_team(json_request):
    # get current session slot i.e  <Day>-<Hour>-<Min>
    active_session = get_current_session()
    team_url = json_request['teamUrl']
    # Check data base for team's question TODO: Read question from database
    # else generate new question
    previous_attempts = decoder_manager.get_previous_decoder_records_by_team_and_session(team_url, active_session)
    if len(previous_attempts) > 0:
        output_expected = previous_attempts[0].output_expected
        possible_values = previous_attempts[0].possible_values
    else:
        output_expected, possible_values = generate_question()
        previous_attempts = []
    decoder_manager.add_decoder_record(output_expected, possible_values, active_session, json_request)
    return output_expected, possible_values, previous_attempts, active_session


def generate_question():
    num_slots = constants.decoder_configuration[NUM_SLOTS]
    num_possible_values = constants.decoder_configuration[NUM_POSSIBLE_VALUES]

    possible_values = random.sample(alphabet_list, num_possible_values)
    output_expected = random.choices(possible_values, k=num_slots)

    return output_expected, possible_values


def evaluate_answer(to_guess, submitted_answer):
    copy_submitted_answer = copy.deepcopy(submitted_answer)
    copy_to_guess = copy.deepcopy(to_guess)
    right_symbol_right_position = 0
    right_symbol_wrong_position = 0

    for index, to_guess_symbol in enumerate(copy_to_guess):
        if to_guess_symbol == copy_submitted_answer[index] and to_guess_symbol != REMOVED:
            right_symbol_right_position += 1
            copy_submitted_answer[index] = REMOVED
            copy_to_guess[index] = REMOVED

    for to_guess_index, to_guess_symbol in enumerate(copy_to_guess):
        if to_guess_symbol != REMOVED:
            for submitted_index, submitted_symbol in enumerate(copy_submitted_answer):
                if to_guess_symbol == submitted_symbol:
                    right_symbol_wrong_position += 1
                    copy_submitted_answer[submitted_index] = REMOVED
                    copy_to_guess[to_guess_index] = REMOVED
                    break

    return right_symbol_right_position, right_symbol_wrong_position


def calculate_score(right_color_right_position, right_color_wrong_position):
    points_for_right_color_right_position = constants.decoder_configuration[POINTS_FOR_RIGHT_SYMBOL_RIGHT_POSITION]
    points_for_right_color_wrong_position = constants.decoder_configuration[POINTS_FOR_RIGHT_SYMBOL_WRONG_POSITION]

    score = (right_color_right_position * points_for_right_color_right_position) + \
            (right_color_wrong_position * points_for_right_color_wrong_position)
    return score


def verify_decoder_answer(to_guess, submitted_answer, num_times_submitted, team_url, active_session):
    num_slots = len(to_guess)
    points_scored = 0
    error_message = ""

    # validate submitted answer length
    if len(submitted_answer) != num_slots:
        error_message = "Submitted answer " + str(submitted_answer) + " does not match expected length of " + str(
            num_slots)
        return error_message, points_scored

    right_symbol_right_position, right_symbol_wrong_position = evaluate_answer(to_guess, submitted_answer)
    points_scored = calculate_score(right_symbol_right_position, right_symbol_wrong_position)
    from utils.utils import generate_status
    update_current_attempt(team_url, active_session, submitted_answer, right_symbol_right_position,
                           right_symbol_wrong_position, points_scored, error_message, generate_status(error_message))

    if right_symbol_right_position == num_slots and num_times_submitted <= NUM_TRIES_FOR_FIRST_TIER:
        points_scored = points_scored + DECODER_BONUS_POINTS_FIRST_TIER
    elif right_symbol_right_position == num_slots and num_times_submitted <= NUM_TRIES_FOR_SECOND_TIER:
        points_scored = points_scored + DECODER_BONUS_POINTS_SECOND_TIER

    return error_message, points_scored


def get_result_as_integer(right_colour_wrong_position, right_colour_right_position):
    if right_colour_wrong_position == 0 and right_colour_right_position == 0:
        return 0
    else:
        return (right_colour_wrong_position * 10) + right_colour_right_position


def format_attempt_history(previous_attempts):
    list_of_attempts = []
    for attempt in previous_attempts:
        if attempt.output_received is not None and len(attempt.output_received) > 0:

            formatted = {
                "output_received": attempt.output_received,
                 "result": get_result_as_integer(attempt.right_colour_wrong_position, attempt.right_colour_right_position)
             }

            list_of_attempts.append(formatted)

    return list_of_attempts

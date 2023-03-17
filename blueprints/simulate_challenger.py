import copy
import time
from itertools import product

from flask import Blueprint, request, jsonify

from utils import constants
from utils.constants import REMOVED

challenger_blueprint = Blueprint('challenger_blueprint', __name__)

from utils.utils import get_logger

logger = get_logger()

key_possible_values = []
value_all_combinations_tuple = []


@challenger_blueprint.post(constants.DECODER_CHALLENGER)
def decoder_challenger():
    start = time.time()
    json_request = request.json
    logger.info(json_request)

    possible_values = json_request['possible_values']
    number_of_slots = json_request['num_slots']
    history = json_request['history']
    answer = derive_decoder_answer(possible_values, number_of_slots, history)

    print('possible values: ', possible_values)
    print('history: ')
    for record in history:
        print("\t", record)
    print('answer: ', answer)

    end = time.time()
    response = {'answer': answer}

    time_elapsed = round(end - start, 2)
    logger.info("solved decoder in " + str(time_elapsed) + " seconds")
    return jsonify(response), 200


def derive_decoder_answer(possible_values, number_of_slots, history):
    global key_possible_values
    global value_all_combinations_tuple

    if key_possible_values != possible_values:
        key_possible_values = possible_values
        value_all_combinations_tuple = list_of_possible_solutions_tuple(possible_values, number_of_slots)

    combinations_remaining_tuple = copy.deepcopy(value_all_combinations_tuple)
    all_combinations_tuple = copy.deepcopy(combinations_remaining_tuple)

    answer = []
    count_removed = 0
    if len(history) == 0:
        index_to_use = 0
        for i in range(0, number_of_slots):
            if i != 0 and i % 2 == 0:
                index_to_use = index_to_use + 1
            answer.append(possible_values[index_to_use])
    elif len(history) == 1:
        index_to_use = len(possible_values) - 1
        for i in range(0, number_of_slots):
            if i != 0 and i % 2 == 0:
                index_to_use = index_to_use - 1
            answer.append(possible_values[index_to_use])
    else:
        for record in history:
            output_received = record['output_received']
            right_symbol_wrong_position, right_symbol_right_position = get_position_scores_from_integer(
                record['result'])

            if right_symbol_right_position == number_of_slots:
                return output_received

            if output_received in combinations_remaining_tuple:
                combinations_remaining_tuple.remove(tuple(output_received))

            if tuple(output_received) in all_combinations_tuple:
                all_combinations_tuple.remove(tuple(output_received))

            for potential_answer_tuple in copy.deepcopy(combinations_remaining_tuple):
                r_s_r_p, r_s_w_p = check_answer(list(potential_answer_tuple), output_received)
                if r_s_r_p != right_symbol_right_position or r_s_w_p != right_symbol_wrong_position:
                    combinations_remaining_tuple.remove(potential_answer_tuple)
                    count_removed += 1

        answer = get_best_combination_for_min_max_score(copy.deepcopy(combinations_remaining_tuple),
                                                        combinations_remaining_tuple, number_of_slots)

    print("all length:", len(all_combinations_tuple), "possible length:", len(combinations_remaining_tuple))
    return answer


def check_answer(to_guess, submitted_answer):
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


def get_position_scores_from_integer(result):
    right_symbol_right_position = result % 10
    right_symbol_wrong_position = 0
    if (result - right_symbol_right_position) > 0:
        right_symbol_wrong_position = (result - right_symbol_right_position) / 10
    return right_symbol_wrong_position, right_symbol_right_position


def get_best_combination_for_min_max_score(all_combinations_tuple, remaining_combinations_tuple, number_of_slots):
    template_score_dictionary = get_score_combinations(number_of_slots)
    min_max = 99999
    combinations = []

    for combination_tuple in all_combinations_tuple:
        scores = copy.deepcopy(template_score_dictionary)
        for remaining_tuple in remaining_combinations_tuple:
            rr, rw = check_answer(list(remaining_tuple), list(combination_tuple))
            key_str = "rr_" + str(rr) + "_rw_" + str(rw)
            scores[key_str] = scores[key_str] + 1

        max_score = max(scores.values())
        if min_max > max_score:
            min_max = max_score
            combinations = [combination_tuple]
        elif min_max == max_score:
            combinations.append(combination_tuple)

    for combi in combinations:
        if combi in remaining_combinations_tuple:
            return list(combi)

    return list(combinations.pop())


def get_score_combinations(number_of_slots):
    scores = {}
    for right_right in range(0, number_of_slots + 1):
        for right_wrong in range(0, number_of_slots - right_right + 1):
            key_str = "rr_" + str(right_right) + "_rw_" + str(right_wrong)
            scores[key_str] = 0
    return scores


def list_of_possible_solutions_tuple(possible_values, number_of_slots):
    results = []
    for combi in product(possible_values, repeat=number_of_slots):
        results.append(combi)
    return results


@challenger_blueprint.post(constants.ASTEROID_CHALLENGER)
def asteroid_challenger():
    start = time.time()
    json_request = request.json
    test_cases = json_request['test_cases']
    from manager.challenger_manager import get_latest_answer_stored
    answers = get_latest_answer_stored().answer
    formatted_answers = []
    for key, value in answers.items():
        formatted_answer = value
        formatted_answer["input"] = key
        formatted_answers.append(formatted_answer)

    end = time.time()
    time_elapsed = round(end - start, 2)
    logger.info("solved " + str(len(test_cases)) + " asteroid testcases in " + str(time_elapsed) + " seconds")
    return jsonify(formatted_answers), 200

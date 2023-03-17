# generate origin - should be length 3
# generate 2 strings of randomly generated length of up to 10
# calculate score of generated strings combined
# prepend and append strings to origin - A X B
# generate until length of total string is > total_length
# generate randomly between 3 - 10 such strings
# append/ prepend randomly to the prized task

# generate winning string
# generate losing string 80% of winning to ensure always win

# response should be the position of center point for origin
# response must have total score - closest one wins 100%
import os

import numpy
import random
import string

from manager.challenger_manager import add_answer
from utils.constants import asteroid_configuration
from utils.utils import get_mode

asteroids = list(string.ascii_uppercase)


def generate_question():
    asteroidLines = []
    numNoiseLines = random.randrange(asteroid_configuration["numNoiseLines"])

    # generate noise lines
    for i in range(0, numNoiseLines):
        line, score, originPosition = generate_line(
            asteroid_configuration["lineLength"] * asteroid_configuration["noiseLineModifier"],
            random.choice(asteroids))
        asteroidLines.append(line)

    # generate winning line
    winningLine, finalScore, winningOriginPosition = generate_line(asteroid_configuration["lineLength"],
                                                                   random.choice(asteroids))
    # winning line will always have the largest index in array of lines
    asteroidLines.append(winningLine)

    # permute length of asteroid lines to randomise position
    asteroidLinesSize = len(asteroidLines)
    permutedPositions = numpy.random.permutation(asteroidLinesSize).tolist()

    # get index of winning line in permutation
    finalWinningPosition = permutedPositions.index(asteroidLinesSize - 1)

    # generate final string based on the permutation of shuffled positions
    finalAsteroidLines = []
    for i in range(0, len(permutedPositions)):
        indexOfLine = permutedPositions[i]
        finalAsteroidLines.append(asteroidLines[indexOfLine])

    # add buffer between lines
    finalAsteroidLines = insert_buffer(finalAsteroidLines)

    # get final position of origin of winning line
    winningPositionOrigin = 0
    for i in range(0, finalWinningPosition * 2):
        winningPositionOrigin += len(finalAsteroidLines[i])

    winningPositionOrigin += winningOriginPosition
    return combine_string_list(finalAsteroidLines), finalScore, winningPositionOrigin


def generate_line(expected_length, origin_asteroid):
    origin = ''.join(origin_asteroid * asteroid_configuration["originLength"])
    leftList = []
    rightList = []
    current_line_length = 0

    while current_line_length < expected_length:
        not_same_asteroid = ""
        if len(leftList) != 0:
            not_same_asteroid = leftList[0]
        asteroid = get_random_asteroid(current_line_length, origin_asteroid, not_same_asteroid)
        left = get_asteroids(asteroid)
        leftList.insert(0, left)
        right = get_asteroids(asteroid)
        rightList.append(right)
        current_line_length = get_length(leftList) + get_length(rightList) + len(origin)

    totalScore = calculate_total_score(leftList, rightList)
    totalScore += asteroid_configuration["originLength"]

    finalAsteroidLine = combine_string_list(leftList) + origin + combine_string_list(rightList)
    pointOfOrigin = get_length(leftList) + int(asteroid_configuration["originLength"] / 2)

    return finalAsteroidLine, totalScore, pointOfOrigin


def calculate_total_score(leftList, rightList):
    score = 0
    for i in range(0, len(leftList)):
        score += calculate_score(leftList[i], rightList[-i - 1])
    return score


def get_length(string_list):
    return len(combine_string_list(string_list))


def combine_string_list(string_list):
    return ''.join(string_list)


def get_random_asteroid(length, origin_asteroid, not_same_asteroid):
    if length > asteroid_configuration["originLength"]:
        return random.choice([s for s in asteroids if s not in not_same_asteroid])
    else:
        return random.choice([s for s in asteroids if s not in origin_asteroid])


def get_asteroids(char):
    stringLength = random.randint(asteroid_configuration["minAsteroid"], asteroid_configuration["maxAsteroid"])
    return ''.join(char * stringLength)


def insert_buffer(input_list):
    inputListLength = len(input_list)
    new_list = []

    if inputListLength > 1:
        for i in range(1, inputListLength):
            left = input_list[i - 1]
            right = input_list[i]

            bufferChar = get_random_asteroid(0, [left[-1], right[0]], "")
            bufferAsteroids = get_asteroids(bufferChar)

            new_list.append(left)
            new_list.append(bufferAsteroids)

            if i == inputListLength - 1:
                new_list.append(right)
    else:
        new_list = input_list

    return new_list


def calculate_score(left, right):
    length = len(left + right)
    score = length
    for multiplier in asteroid_configuration["scoreMultiplier"]:
        if length >= multiplier:
            score = length * asteroid_configuration["scoreMultiplier"][multiplier]
            break
    return score


def generate_test_cases(num_test_cases):
    testCases = []

    for i in range(0, num_test_cases):
        line, score, origin = generate_question()
        testCase = {
            "line": line,
            "score": score,
            "origin": origin
        }
        testCases.append(testCase)

    return format_test_cases(testCases)


def format_test_cases(test_cases):
    results = {}
    formatted_tests = []

    counter = 1
    formatted_answers = {}
    for test_case in test_cases:
        key = test_case["line"]
        formatted_tests.append(test_case["line"])
        formatted_answers[key] = {}
        formatted_answers[key]["score"] = test_case["score"]
        formatted_answers[key]["origin"] = test_case["origin"]
        counter += 1

    results["test_cases"] = formatted_tests
    if get_mode() == "DEV" or get_mode() == "LOCAL":
        add_answer(formatted_answers)

    return formatted_answers, results

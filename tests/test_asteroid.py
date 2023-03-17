import math

import pytest

from processing_logic.asteroid import generate_line, generate_test_cases, calculate_score, get_random_asteroid
from utils.constants import asteroid_configuration


def test_generate_complex_line():
    expectedSize = 500
    expectedOriginAsteroid = "A"
    line, score, position = generate_line(expectedSize, expectedOriginAsteroid)

    assert len(line) >= expectedSize
    assert score >= expectedSize
    assert line[position] == expectedOriginAsteroid


def test_generate_simple_line():
    expectedSize = 10
    expectedOriginAsteroid = "G"
    line, score, position = generate_line(expectedSize, expectedOriginAsteroid)

    assert len(line) > expectedSize
    assert score >= expectedSize
    assert line[position] == expectedOriginAsteroid


def test_line_score():
    for i in range(0, 1000):
        expectedSize = asteroid_configuration["lineLength"]
        expectedNoiseSize = asteroid_configuration["lineLength"] * asteroid_configuration["noiseLineModifier"]
        expectedOriginAsteroid = "G"
        line, score, origin = generate_line(expectedSize, expectedOriginAsteroid)
        noiseLine, noiseScore, noiseOrigin = generate_line(expectedNoiseSize, expectedOriginAsteroid)
        # print("Run " + str(i) + " Score: " + str(score) + " | Noise Score: " + str(noiseScore))

        assert len(line) > len(noiseLine)
        assert score >= noiseScore
        assert line[origin] == expectedOriginAsteroid


def test_level1_scoring():
    left = "CCC"
    right = "C"
    score = calculate_score(left, right)
    assert score == 4


def test_level2_scoring_7():
    left = "BBBB"
    right = "BBB"
    score = calculate_score(left, right)
    assert score == 10.5


def test_level2_scoring():
    left = "BBBB"
    right = "BBBB"
    score = calculate_score(left, right)
    assert score == 12


def test_level3_scoring_10():
    left = "CCCCC"
    right = "CCCCC"
    score = calculate_score(left, right)
    assert score == 20


def test_level3_scoring():
    left = "CCCCCC"
    right = "CCCCC"
    score = calculate_score(left, right)
    assert score == 22


def test_division():
    assert 2 == int(math.ceil(3 / 2))


@pytest.mark.parametrize("num_test_cases", [10, 100])
def test_generate_asteroid(num_test_cases):
    answers, test_cases = generate_test_cases(num_test_cases)
    assert num_test_cases == len(test_cases["test_cases"])
    assert num_test_cases == len(answers)


def test_calculate_score_upon_line_generation():
    for i in range(0, 100):
        line, totalScore, origin = generate_line(1000, "X")
        # print(totalScore)

        position = 1
        updatedLine = []

        while position < len(line):
            if line[position] != line[position - 1]:
                line1 = line[0:position]
                line2 = line[position:]
                line = line2
                updatedLine.append(line1)
                position = 0
            position += 1

        updatedLine.append(line)
        # print(updatedLine)
        # print(len(updatedLine))

        score = 0
        for i in range(0, len(updatedLine) // 2):
            # print(updatedLine[i], updatedLine[-i - 1])
            currScore = calculate_score(updatedLine[i], updatedLine[-i - 1])
            # print(currScore)
            score += currScore

        score += 3
        # print("Total Score: " + str(score))

        assert totalScore == score

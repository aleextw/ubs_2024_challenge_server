from utils.utils import calculate_score


def test_calculate_score_empty_submission():
    team_submission = [{}]
    answer = [
        {
            "1000": [1, 2, 3, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [3, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 8],
            "5000": [5, 6, 7, 8, 9],
            "6000": [6, 7, 8, 9, 10],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        }
    ]

    expected = 0

    actual = calculate_score(team_submission, answer, 100)
    assert actual[1] == expected


def test_calculate_score_partial_submission_all_correct():
    team_submission = [
        {
            "1000": [1, 2, 3, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [3, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 8],
        }
    ]
    answer = [
        {
            "1000": [1, 2, 3, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [3, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 8],
            "5000": [5, 6, 7, 8, 9],
            "6000": [6, 7, 8, 9, 10],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        }
    ]

    expected = 40

    actual = calculate_score(team_submission, answer, 100)
    assert actual[1] == expected


def test_calculate_score_partial_submission_partial_correct():
    team_submission = [
        {
            "1000": [1, 2, 5, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [1, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 10],
        }
    ]
    answer = [
        {
            "1000": [1, 2, 3, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [3, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 8],
            "5000": [5, 6, 7, 8, 9],
            "6000": [6, 7, 8, 9, 10],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        }
    ]

    expected = 10

    actual = calculate_score(team_submission, answer, 100)
    assert actual[1] == expected


def test_calculate_score_full_submission_all_correct():
    team_submission = [
        {
            "1000": [1, 2, 3, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [3, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 8],
            "5000": [5, 6, 7, 8, 9],
            "6000": [6, 7, 8, 9, 10],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        }
    ]
    answer = [
        {
            "1000": [1, 2, 3, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [3, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 8],
            "5000": [5, 6, 7, 8, 9],
            "6000": [6, 7, 8, 9, 10],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        }
    ]

    expected = 100

    actual = calculate_score(team_submission, answer, 100)
    assert actual[1] == expected


def test_calculate_score_full_submission_partial_correct():
    team_submission = [
        {
            "1000": [1, 2, 3, 4, 6],
            "2000": [2, 3, 4, 5, 7],
            "3000": [3, 4, 5, 6, 8],
            "4000": [4, 5, 6, 7, 9],
            "5000": [5, 6, 7, 8, 10],
            "6000": [6, 7, 8, 9, 11],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        }
    ]
    answer = [
        {
            "1000": [1, 2, 3, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [3, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 8],
            "5000": [5, 6, 7, 8, 9],
            "6000": [6, 7, 8, 9, 10],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        }
    ]

    expected = 40

    actual = calculate_score(team_submission, answer, 100)
    assert actual[1] == expected


def test_calculate_score_full_submission_full_correct_truncate_length():
    team_submission = [
        {
            "1000": [1, 2, 3, 4, 6],
            "2000": [2, 3, 4, 5, 7],
            "3000": [3, 4, 5, 6, 8],
            "4000": [4, 5, 6, 7, 9],
            "5000": [5, 6, 7, 8, 10],
            "6000": [6, 7, 8, 9, 11],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        },
        {
            "1000": [1, 2, 3, 4, 6],
            "2000": [2, 3, 4, 5, 7],
            "3000": [3, 4, 5, 6, 8],
            "4000": [4, 5, 6, 7, 9],
            "5000": [5, 6, 7, 8, 10],
            "6000": [6, 7, 8, 9, 11],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        },
    ]
    answer = [
        {
            "1000": [1, 2, 3, 4, 5],
            "2000": [2, 3, 4, 5, 6],
            "3000": [3, 4, 5, 6, 7],
            "4000": [4, 5, 6, 7, 8],
            "5000": [5, 6, 7, 8, 9],
            "6000": [6, 7, 8, 9, 10],
            "7000": [7, 8, 9, 10, 11],
            "8000": [8, 9, 10, 11, 12],
            "9000": [9, 10, 11, 12, 13],
            "10000": [10, 11, 12, 13, 14, 15],
        }
    ]

    expected = 40

    actual = calculate_score(team_submission, answer, 100)
    assert actual[1] == expected

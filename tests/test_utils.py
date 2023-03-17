from utils.utils import verify_answers


def test_answer_verification_all_correct():
    answersExpected = {
        "ABC": {"origin": 20, "score": 20},
        "ABCD": {"origin": 30, "score": 40}
    }
    answersReceived = [
        {"input": "ABC", "origin": 20, "score": 20},
        {"input": "ABCD", "origin": 30, "score": 40}
    ]
    errorMessage, score = verify_answers(answersReceived, answersExpected, 100)
    assert '' == errorMessage
    assert 100 == score


def test_answer_verification_missing_answers():
    answersExpected = {
        "ABC": {"origin": 20, "score": 20},
        "ABCD": {"origin": 30, "score": 40}
    }
    answersReceived = [
        {"input": "ABC", "origin": 20, "score": 20}
    ]
    errorMessage, score = verify_answers(answersReceived, answersExpected, 100)
    assert 0 == 0
    assert 'missing testcase from response' == errorMessage


def test_answer_verification_missing_answers_key():
    answersExpected = {
        "ABC": {"origin": 20, "score": 20},
        "ABCD": {"origin": 30, "score": 40}
    }
    answersReceived = [
        {"input": "ABC", "origin": 20, "score": 20},
        {"input": "ABCDE", "origin": 30, "score": 40}
    ]
    errorMessage, score = verify_answers(answersReceived, answersExpected, 100)
    assert 50 == score
    assert '' == errorMessage


def test_answer_verification_half_correct():
    answersExpected = {
        "ABC": {"origin": 20, "score": 20},
        "ABCD": {"origin": 30, "score": 40}
    }
    answersReceived = [
        {"input": "ABC", "origin": 20, "score": 20},
        {"input": "ABCD", "origin": 40, "score": 40}
    ]
    errorMessage, score = verify_answers(answersReceived, answersExpected, 100)
    assert 50 == score
    assert '' == errorMessage

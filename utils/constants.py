DECODER_ROOT = "/decoder"
ASTEROID_ROOT = "/asteroid"
EVALUATE = "/evaluate"
CHALLENGER = "/challenger"

# configuration
ROWS_TO_REMOVE = 1000
REQUEST_TIMEOUT = 10
ALERT_RECORDS = 5000

# paths
# evaluate endpoints
DECODER_EVALUATE = DECODER_ROOT + EVALUATE
ASTEROID_EVALUATE = ASTEROID_ROOT + EVALUATE

# challenger endpoints
ASTEROID_CHALLENGER = CHALLENGER + ASTEROID_ROOT
DECODER_CHALLENGER = CHALLENGER + DECODER_ROOT

# number of test cases
ASTEROID_TEST_CASES = 10

# difficulty multiplier
DECODER_DIFFICULTY = 1
ASTEROID_DIFFICULTY = 1

# number of points awarded in total
DECODER_MAX_POINTS = 100 * DECODER_DIFFICULTY
ASTEROID_MAX_POINTS = 100 * ASTEROID_DIFFICULTY

# status messages
PASS = "PASS"
FAIL = "FAIL"

# decoder constants
TO_GUESS = "to_guess"
NUM_SLOTS = "num_slots"
NUM_POSSIBLE_VALUES = "num_possible_values"
POSSIBLE_VALUES = "possible_values"
HISTORY = "history"
REMOVED = "removed"

POINTS_FOR_RIGHT_SYMBOL_RIGHT_POSITION = "right_symbol_right_position"
POINTS_FOR_RIGHT_SYMBOL_WRONG_POSITION = "right_symbol_wrong_position"

DECODER_NUM_SLOTS = 5
NUM_TRIES_FOR_FIRST_TIER = 4
NUM_TRIES_FOR_SECOND_TIER = 5
DECODER_BONUS_POINTS_FIRST_TIER = 20.0
DECODER_BONUS_POINTS_SECOND_TIER = 10.0

decoder_configuration = {
    NUM_SLOTS: DECODER_NUM_SLOTS,
    NUM_POSSIBLE_VALUES: 7,
    POINTS_FOR_RIGHT_SYMBOL_RIGHT_POSITION: (DECODER_MAX_POINTS - DECODER_BONUS_POINTS_FIRST_TIER) / DECODER_NUM_SLOTS,
    POINTS_FOR_RIGHT_SYMBOL_WRONG_POSITION: (DECODER_MAX_POINTS - DECODER_BONUS_POINTS_FIRST_TIER) / DECODER_NUM_SLOTS / 2
}

asteroid_configuration = {
    "originLength": 3,
    "lineLength": 1000,
    "minAsteroid": 1,
    "maxAsteroid": 10,
    "noiseLineModifier": 0.6,
    "numNoiseLines": 5,
    "scoreMultiplier": {
        # length of combined line : multiplier
        10: 2,
        7: 1.5,
        6: 1,
    }
}

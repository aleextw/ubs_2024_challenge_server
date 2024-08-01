LAB_WORK_ROOT = "/"
LAB_WORK_FILENAME = "/lab_work"
EVALUATE = "/evaluate"
CHALLENGER = "/challenger"
COORDINATOR = "/coordinator"

# configuration
ROWS_TO_REMOVE = 1000
REQUEST_TIMEOUT = 10
ALERT_RECORDS = 5000

# paths
# evaluate endpoints
LAB_WORK_EVALUATE = LAB_WORK_ROOT + EVALUATE

# challenger endpoints
LAB_WORK_CHALLENGER = CHALLENGER + LAB_WORK_ROOT

# number of test cases
LAB_WORK_TEST_CASES = 5

# difficulty multiplier
LAB_WORK_DIFFICULTY = 1

# number of points awarded in total
LAB_WORK_MAX_POINTS = 100 * LAB_WORK_DIFFICULTY


# status messages
PASS = "PASS"
FAIL = "FAIL"

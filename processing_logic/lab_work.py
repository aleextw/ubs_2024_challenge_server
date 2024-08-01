import random
import copy

from manager.challenger_manager import add_answer
from utils.utils import get_mode


primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def gen_add(r=None):
    if r is None:
        return lambda x: x + x
    return lambda x: x + r


def gen_mult(r=None):
    if r is None:
        return lambda x: x * x
    return lambda x: x * r


def gen_cond(cond, t, f):
    return lambda x: t if x % cond == 0 else f


def generate_answer(labs):
    parsed_labs = []
    prod = 1

    for cell_counts, increment, condition in labs:
        operator, operand = increment
        if operator == "+":
            op = gen_add(operand if operand != "count" else None)
        else:
            op = gen_mult(operand if operand != "count" else None)

        data = {"items": cell_counts, "op": op, "cond": gen_cond(*condition)}

        parsed_labs.append(data)
        prod *= condition[0]

    inspection_count = [0] * len(parsed_labs)
    output = {}

    for epoch in range(10_000):
        for idx, lab in enumerate(parsed_labs):
            inspection_count[idx] += len(lab["items"])
            for item in lab["items"]:
                cell_count = lab["op"](item) % prod
                parsed_labs[lab["cond"](cell_count)]["items"].append(cell_count)

            lab["items"] = []

        if (epoch + 1) % 1000 == 0:
            output[str(epoch + 1)] = copy.copy(inspection_count)

    return output


def generate_question(difficulty):
    match difficulty:
        case 0:
            cell_count_bounds = [1, 5]
            increment_bounds = [2, 5]
        case 1:
            cell_count_bounds = [10, 50]
            increment_bounds = [2, 5]
        case 2:
            cell_count_bounds = [50, 100]
            increment_bounds = [5, 10]
        case 3:
            cell_count_bounds = [100, 200]
            increment_bounds = [10, 30]
        case 4:
            cell_count_bounds = [100, 10_000]
            increment_bounds = [30, 50]

    labs = []
    num_labs = random.randint(7, 10)
    random_primes = primes[:num_labs]
    random.shuffle(random_primes)

    for i in range(num_labs):
        cell_counts = []
        for _ in range(random.randint(1, 8)):
            cell_counts.append(random.randint(*cell_count_bounds))
        increment = [
            random.choice(["*", "+"]),
            random.choice(["count", random.randint(*increment_bounds)]),
        ]

        condition = [
            random_primes[i],
            *random.choices([j for j in range(num_labs) if j != i], k=2),
        ]

        labs.append([cell_counts, increment, condition])

    answer = generate_answer(copy.deepcopy(labs))

    return labs, answer


def generate_test_cases(num_test_cases):
    test_cases = []

    for i in range(num_test_cases):
        test_case, answer = generate_question(i)

        test_cases.append({"test_case": test_case, "answer": answer})

    return format_test_cases(test_cases)


def format_test_cases(test_cases):
    formatted_tests = []
    answers = []

    for test_case in test_cases:
        formatted_tests.append(obj_to_md_table(test_case["test_case"]))
        answers.append(test_case["answer"])

    if get_mode() in ("DEV", "LOCAL"):
        add_answer(answers)

    return answers, formatted_tests


def obj_to_md_table(test_case):
    col_max_length = [0] * 4
    rows = [[]]

    for idx, header in enumerate(["Lab", "Cell Counts", "Increment", "Condition"]):
        rows[-1].append(header)
        if col_max_length[idx] < len(header):
            col_max_length[idx] = len(header)

    condition_max_length = len(
        str(max((i[2][0] for i in test_case), key=lambda x: len(str(x))))
    )

    for idx, (cell_count, increment, condition) in enumerate(test_case):
        rows.append([])

        rows[-1].append(idx)

        cell_count_str = " ".join(map(str, cell_count))
        rows[-1].append(cell_count_str)
        if col_max_length[1] < len(cell_count_str):
            col_max_length[1] = len(cell_count_str)

        increment_str = f"count {increment[0]} {increment[1]}"
        rows[-1].append(increment_str)
        if col_max_length[2] < len(increment_str):
            col_max_length[2] = len(increment_str)

        condition_str = (
            f"{condition[0]:<{condition_max_length}} {condition[1]:<} {condition[2]:<}"
        )
        rows[-1].append(condition_str)
        if col_max_length[3] < len(condition_str):
            col_max_length[3] = len(condition_str)

    output = []
    for row in rows:
        temp = []
        for idx, col in enumerate(row):
            temp.append(f" {col:<{col_max_length[idx]}} ")
        output.append(f"|{'|'.join(temp)}|")

    # Create header divider row
    temp = []
    for i in range(4):
        temp.append("-" * (col_max_length[i] + 2))
    output.insert(1, f"|{'|'.join(temp)}|")

    return "\n".join(output)


def md_table_to_obj(test_case: str):
    rows = test_case.split("\n")
    rows = rows[2:]

    rows = [row[1:-1].split("|") for row in rows]

    parsed = []

    for row in rows:
        parsed.append([])

        # Cell counts
        parsed[-1].append([int(i) for i in row[1].strip().split(" ")])

        # Increment
        parsed[-1].append(
            [int(i) if i.isnumeric() else i for i in row[2].strip().split(" ")[1:]]
        )

        # Condition
        condition = row[3].split(" ")
        condition = [int(i) for i in condition if i != ""]
        parsed[-1].append(condition)

    return parsed

from processing_logic.lab_work import (
    generate_test_cases,
    generate_answer,
    obj_to_md_table,
    md_table_to_obj,
)
from app import app


def test_obj_to_md_table():
    test_case = [
        ([98, 89, 52], ["*", 2], [5, 6, 1]),
        ([57, 95, 80, 92, 57, 78], ["*", 13], [2, 2, 6]),
        ([82, 74, 97, 75, 51, 92, 83], ["+", 5], [19, 7, 5]),
        ([97, 88, 51, 68, 68, 76], ["+", 6], [7, 0, 4]),
        ([90, 56], ["*", "count"], [11, 3, 5]),
    ]

    expected_output = """| Lab | Cell Counts          | Increment     | Condition |
|-----|----------------------|---------------|-----------|
| 0   | 98 89 52             | count * 2     | 5  6 1    |
| 1   | 57 95 80 92 57 78    | count * 13    | 2  2 6    |
| 2   | 82 74 97 75 51 92 83 | count + 5     | 19 7 5    |
| 3   | 97 88 51 68 68 76    | count + 6     | 7  0 4    |
| 4   | 90 56                | count * count | 11 3 5    |"""
    actual_output = obj_to_md_table(test_case)
    assert actual_output == expected_output


def test_md_table_to_obj():
    test_case = """| Lab | Cell Counts          | Increment     | Condition |
|-----|----------------------|---------------|-----------|
| 0   | 98 89 52             | count * 2     | 5  6 1    |
| 1   | 57 95 80 92 57 78    | count * 13    | 2  2 6    |
| 2   | 82 74 97 75 51 92 83 | count + 5     | 19 7 5    |
| 3   | 97 88 51 68 68 76    | count + 6     | 7  0 4    |
| 4   | 90 56                | count * count | 11 3 5    |"""
    expected_output = [
        [[98, 89, 52], ["*", 2], [5, 6, 1]],
        [[57, 95, 80, 92, 57, 78], ["*", 13], [2, 2, 6]],
        [[82, 74, 97, 75, 51, 92, 83], ["+", 5], [19, 7, 5]],
        [[97, 88, 51, 68, 68, 76], ["+", 6], [7, 0, 4]],
        [[90, 56], ["*", "count"], [11, 3, 5]],
    ]
    actual_output = md_table_to_obj(test_case)
    assert actual_output == expected_output


def test_generate_labs():
    with app.app_context():
        answers, test_cases = generate_test_cases(5)
    assert len(test_cases["test_cases"]) == 5
    assert len(answers) == 5

    bounds = [
        [1, 5, 2, 5],
        [10, 50, 2, 5],
        [50, 100, 5, 10],
        [100, 200, 10, 30],
        [100, 10_000, 30, 50],
    ]

    for jdx, test_case in enumerate(test_cases["test_cases"]):
        parsed_test_case = md_table_to_obj(test_case)

        for idx, lab in enumerate(parsed_test_case):
            for cell_count in lab[0]:
                assert bounds[jdx][0] <= cell_count <= bounds[jdx][1]

            assert lab[1][1] == "count" or bounds[jdx][2] <= lab[1][1] <= bounds[jdx][3]

            assert lab[2][1] != idx
            assert lab[2][2] != idx


def test_generate_answer():
    test_case = [
        ([98, 89, 52], ["*", 2], [5, 6, 1]),
        ([57, 95, 80, 92, 57, 78], ["*", 13], [2, 2, 6]),
        ([82, 74, 97, 75, 51, 92, 83], ["+", 5], [19, 7, 5]),
        ([97, 88, 51, 68, 68, 76], ["+", 6], [7, 0, 4]),
        ([63], ["+", 1], [17, 0, 1]),
        ([94, 91, 51, 63], ["+", 4], [13, 4, 3]),
        ([61, 54, 94, 71, 74, 68, 98, 83], ["+", 2], [3, 2, 7]),
        ([90, 56], ["*", "count"], [11, 3, 5]),
    ]

    expected = {
        "1000": [1783, 17709, 17770, 17940, 17208, 17720, 295, 1220],
        "2000": [3872, 35439, 35630, 35987, 34561, 35334, 621, 2418],
        "3000": [6034, 53184, 53537, 54052, 51944, 52936, 945, 3589],
        "4000": [8065, 70944, 71453, 72133, 69377, 70543, 1259, 4745],
        "5000": [10145, 88737, 89393, 90208, 86815, 88165, 1550, 5901],
        "6000": [12304, 106488, 107304, 108282, 104212, 105775, 1870, 7057],
        "7000": [14379, 124242, 125217, 126354, 121622, 123384, 2188, 8217],
        "8000": [16405, 142042, 143160, 144441, 139088, 141007, 2474, 9364],
        "9000": [18574, 159788, 161066, 162509, 156475, 158606, 2796, 10537],
        "10000": [20688, 177545, 178984, 180582, 173879, 176215, 3116, 11694],
    }

    assert generate_answer(test_case) == expected

# Lab Work

## Instructions

You are the manager of several labs, whose job is to observe several petri dishes of yeast cells. Each lab is assigned a number of petri dishes with varying starting cell counts. Every day, two things occur:

- The number of cells in each dish increases by a certain amount (specified in your input).
- Each lab goes in numerical order, recounting the number of cells in each dish, and based on the number of cells in that dish, passes it on to another lab for further analysis.

This process repeats for 10,000 days.

As the manager of these labs, you want to know which labs have been working the hardest, and therefore want to know how many petri dishes each lab has analysed, at regular intervals.

Design an algorithm that tracks the number of petri dishes analysed by each lab, at intervals of 1000.

Expose a `POST` endpoint `/lab-work` for us to verify!

## Information

### Input

Your input is sent as a list of 'old-fashioned' (markdown) tables for you to parse, where each table constitutes one test case.
1. The `Lab` column indicates which lab the data corresponds to.
2. The `Cell counts` column indicates the starting cell counts of the petri dishes belonging to that lab.
   - Constraints: `0 < cell count < 10000`
3. The `Increment` column indicates how the number of cells grows every day
   - Constraints: Only addition or multiplication, operand can be integer `x` where `0 < x <= 100` or can be `count` itself
4. The `Condition` column consists of three numbers
   - The first number indicates the condition used to determine which lab the petri dish is passed to next
   - The second number is the lab which this dish will be passed to if the number of cells in the dish (after incrementing) is divisble by the first number
   - The third number is the lab which this dish will be passed to if the condition above is not satisfied 

#### Example Input

(The test case has been split into multiple lines for clarity)

```
[
   """
   |Lab | Cell counts             | Increment     | Condition |
   |----|-------------------------|---------------|-----------|
   |0   | 98 89 52                | count * 2     | 5  6 1    |
   |1   | 57 95 80 92 57 78       | count * 13    | 2  2 6    |
   |2   | 82 74 97 75 51 92 83    | count + 5     | 19 7 5    |
   |3   | 97 88 51 68 68 76       | count + 6     | 7  0 4    |
   |4   | 63                      | count + 1     | 17 0 1    |
   |5   | 94 91 51 63             | count + 4     | 13 4 3    |
   |6   | 61 54 94 71 74 68 98 83 | count + 2     | 3  2 7    |
   |7   | 90 56                   | count * count | 11 3 5    |
   """,
   ...
]
```

### Output

Your output should consist of a list of JSON objects (each corresponding to a test case), with keys corresponding to the day which the record was logged, and an array of the number of petri-dishes analysed by each lab, in the order of the lab numbers.

#### Example Output

```json
[
   {
      "1000": [1732, 17233, 17293, 17456, 16746, 17243, 285, 1184],
      "2000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349],
      "3000": [5875, 51750, 52093, 52591, 50541, 51511, 917, 3487],
      "4000": [7846, 69032, 69526, 70184, 67506, 68644, 1221, 4610],
      "5000": [9869, 86346, 86982, 87771, 84475, 85791, 1502, 5734],
      "6000": [11977, 103617, 104409, 105356, 101400, 102927, 1814, 6857],
      "7000": [13992, 120893, 121839, 122940, 118342, 120062, 2122, 7984],
      "8000": [15959, 138215, 139299, 140539, 135340, 137211, 2398, 9098],
      "9000": [18078, 155481, 156721, 158119, 152256, 154336, 2711, 10237],
      "10000": [20133, 172759, 174155, 175703, 169190, 171471, 3022, 11362]
   }
]
```

### Scoring

For each test case, partial marks will be given for each correct answer per iteration. For example, if you manage to submit the following, you will be granted 20% of the points for the test case:

```json
{
   "1000": [1732, 17233, 17293, 17456, 16746, 17243, 285, 1184],
   "2000": [3767, 34485, 34670, 35015, 33630, 34383, 601, 2349]
}
```
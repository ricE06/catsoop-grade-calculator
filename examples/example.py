"""
Sample code to output grade reports.
"""

from catsoop_grade_calculator import ScoreCalculator

tokens = {}
with open('token.txt', 'r') as file:
    for line in file:
        class_num, token = line.strip().split(' ')
        tokens[class_num] = token

sooper = ScoreCalculator(tokens)
report = sooper.report_all()
print(report)

# to write to a file, uncomment this code:
# with open("output.txt", "w") as file:
#     file.write(report)

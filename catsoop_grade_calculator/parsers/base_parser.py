"""
Abstract class for the different parsers.
"""

from typing import Optional, Callable
from .request import CatsoopRequests

class Parser():

    def __init__(self):
        pass

    def gen_assignment_dict(self, 
                            score: tuple[float], 
                            assignment_type: str,
                            assignment_name: str,
                            sub_assignment: Optional[str] = None) -> dict:
        out =  {'score': score,
                'assignment_type': assignment_type,
                'assignment_name': assignment_name}
        if sub_assignment is not None:
            out['sub_assignment'] = sub_assignment
        return out

    def add_score_to_dict(self, score_dict: dict,
                          line: str,
                          assignment_type: str,
                          score_type:  str,
                          default_max: Optional[float] = None,
                          return_name: Optional[bool] = False,
                          keyword: Optional[str] = None,
                          exact_case: Optional[bool] = False,
                          delimiter: Optional[str] = ":",
                          binary_x_string: Optional[str] = "\x98") -> Optional[str]:
        """
        Mutates the input score_dict to add an entry.
        Score_type is a string and takes one of 'fraction',
        'percent', or 'binary'.
        If keyword is not provided, it will check for assignment_type
        in the line of text.
        If default_max is not provided, it will look for the last
        two numbers (true score, max score). If it is, it will
        only look for the last number (the true score).
        If assignment_name is not provided, it will use the
        string before the `:` delimiter. If `:` is not found,
        it will use the assignment_type.
        If the return_name flag is set to True, it will return
        the string before the `:` delimiter.
        """

        def find_assignment_name():
            if delimiter not in line:
                return assignment_type
            return line.split(delimiter)[0]

        # check if line contains a score
        if keyword is None: keyword = assignment_type
        check_line = line if exact_case else line.lower()
        if keyword not in check_line:
            return find_assignment_name() if return_name else None

        # process the line for numbers, assign that to score
        if score_type == 'binary':
            raw_score = 0.0 if line[-1] == binary_x_string else 1.0
            default_max = 1.0
        else:
            all_nums = CatsoopRequests.get_numbers(line)
            score = (all_nums[-1], default_max) if default_max else all_nums[-2:]
            raw_score = all_nums[-1] if default_max else all_nums[-2]
        if not default_max: default_max = all_nums[-1]
        score = (raw_score, default_max)

        # add to dictionary
        score_dict.setdefault(assignment_type, []).append(self.gen_assignment_dict(
            score, assignment_type, find_assignment_name()))
        return find_assignment_name()

    def parse_html(self, inp_lines: list[str]) -> list[dict]:
        """
        Parses the preprocessed html into the following format to
        feed into the grade calculator: 
            list of:
                dictionaries with key, values:
                    score: a tuple with first element raw score, and second
                        element total score (both floats)
                    assignment_type: a string with a descriptor of 
                        the type of assignment
                    assignment_name: a string with the assignment name, 
                    sub_assignment: a subassignment descriptor, if applicable
        """
        out = {}

        headers = self.headers

        cur_type = None
        for line in inp_lines:
            for key_header in headers:
                if key_header in line.lower():
                    cur_type = key_header
            if cur_type is None:
                continue
            add_func = headers[cur_type].get('func', self.add_score_to_dict)
            args = headers[cur_type].get('args', [])
            kwargs = headers[cur_type].get('kwargs', {})
            add_func(out, line, *args, **kwargs)
        return out

    def calculate_score(self, score_data: dict[str, list[dict]]) -> float:
        """
        To be implemented by each parser. Computes a cumulative score
        and returns a float (out of 10.0).
        """
        pass

    def calculate_average_in_category(self, category_data: list[dict],
                                      normalize_each: Optional[bool] = True) -> float:
        """
        Given a grading category (labs, psets, etc.), returns the average
        score out of each assignment in the category as a float out of 1.

        Args:
            `category_data`: a list of dictionaries where each dictionary describes
                an assignment and its score
        Kwargs:
            `normalize_each`: boolean, if True will set the max score to 1 (i.e. equal)
                before adding up all the points.

        Returns: a float representing the average score out of 1. 
        """
        total_earned, total_possible = 0, 0

        def add_to_scores(score_pair: tuple[float]) -> None:
            """
            Adds the score to the total. Score_pair is a tuple with
            first element earned and second point possible.
            """
            earned, possible = score_pair
            if normalize_each:
                earned = earned / possible
                possible = 1
            nonlocal total_earned, total_possible
            total_earned += earned
            total_possible += possible
            return

        for assignment in category_data:
            add_to_scores(assignment['score'])

        return total_earned / total_possible

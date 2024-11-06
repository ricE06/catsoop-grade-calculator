"""
Parser for 6.101: Fundamentals of Programming (Python).
"""

from parsers.base_parser import Parser
from parsers.request import CatsoopRequests
import pprint

class PyParser(Parser):
    """
    Handles the 'Progress' page at py.mit.edu.
    """

    def __init__(self):
        self.assignment_types = {'midterm',
                                'final',
                                'reading',
                                'lab',
                                 'recitation'}

        self.headers = {'midterm': {'args': ['midterm', 'fraction'],
                                    'kwargs': {'keyword': 'midterm exam:'}},
                        'final': {'args': ['final', 'fraction'],
                                    'kwargs': {'keyword': 'final exam:'}},
                       'lab': {'args': ['lab', 'fraction'],
                               'kwargs': {'keyword': 'overall score:',}},
                        'reading': {'args': ['reading', 'percent'],
                                    'kwargs': {'default_max': 100,
                                               'keyword': '(',}},
                       'recitation': {'args': ['recitation', 'binary'],
                                         'kwargs':{'default_max': 1.0,
                                                   'keyword': 'day',
                                                   'binary_x_string': '*'}},
                        'will count for': {'args': ['weights', 'percent'],
                                    'kwargs': {'default_max': 1,
                                               'keyword': 'will count for',
                                               'delimiter': ' will count for',},},}
        super().__init__()
        return

    def calculate_score(self, score_data):
        """
        Computes the cumulative score given a score dictionary.
        Returns a dictionary of:
            best_score: tuple of two floats, the true score and the possible score
                At the end of the semester, possible score should be 100
            alt_scores: tuple of tuples of floats, other scores that you may
                have (some classes use multiple schemes and pick
                the best one)
            by_category: dictionary mapping assignment categories to grade floats
        """

        # get the auto-calculated weights
        weights_raw = score_data['weights']
        weights = {'participation': 0, 'midterm': 0, 'final': 0, 'lab': 50}
        for weight_dict in weights_raw:
            for weight_key in weights:
                if weight_key in weight_dict['assignment_name']:
                    weights[weight_key] = weight_dict['score'][0]
        weights['reading'] = weights['participation'] / 2
        weights['recitation'] = weights['participation'] / 2

        # get scores by assignment category 
        # note that 'weights' isn't in self.assignment_types
        by_category = {}
        for category in self.assignment_types:
            if category not in score_data: continue
            frac = self.calculate_average_in_category(score_data[category])
            by_category[category] = frac

        earned, possible = 0, 0
        for category, weight in weights.items():
            if category not in score_data: continue
            frac = by_category[category]
            delta_earned = weight*frac
            delta_possible = weight
            earned += delta_earned
            possible += delta_possible

        output = {'best_score': (earned, possible),
                  'alt_scores': tuple(),
                  'by_category': by_category}

        return output


if __name__ == "__main__":
    with open('../token.txt', 'r') as f:
        code_1, token_1 = f.readline().strip().split(' ')
        code_2, token_2 = f.readline().strip().split(' ')
    token = token_2
    print(token_2)
    raw_data = CatsoopRequests.request_data(token, class_code='6.101')
    print(raw_data.text)
    preprocessed = CatsoopRequests.preprocess_data(raw_data.text)
    pprint.pp(preprocessed)
    # for line in preprocessed:
        # print(CatsoopRequests.get_numbers(line))
    parser = PyParser()
    score_data = parser.parse_html(preprocessed)
    pprint.pp(score_data)
    out_score = parser.calculate_score(score_data)
    pprint.pp(out_score)

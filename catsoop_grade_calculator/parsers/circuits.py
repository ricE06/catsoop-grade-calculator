"""
Parser for 6.200: Circuits and Electronics.
"""

from .request import CatsoopRequests
from .base_parser import Parser
import pprint

class CircuitsParser(Parser):
    """
    Handles the 'Progress' page at circuits.mit.edu.
    """

    def __init__(self):
        self.assignment_types = {'midterm',
                                'final',
                                'pset',
                                'nanoquiz',
                                'lab',
                                 'participation'}

        self.headers = {'midterm': {'args': ['midterm', 'fraction'],
                                   'kwargs': {}},
                        'final': {'args': ['final', 'fraction']},
                       'problem sets': {'args': ['pset', 'fraction'],
                                        'kwargs': {}},
                       'labs': {'args': ['lab', 'fraction'],
                                'kwargs': {'keyword': 'total',
                                           'return_name': True}},
                       'nanoquizzes': {'args': ['nanoquiz', 'percent'],
                                       'kwargs': {'default_max': 100.00,
                                                  'exact_case': True}},
                       'participation': {'args': ['participation', 'binary'],
                                         'kwargs':{'default_max': 1.0,
                                                   'keyword': 'â'}}}

        super().__init__()

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
        output = {'by_category': {}}
        scheme_1 = {'midterm': 25,
                    'final': 40,
                    'pset': 15,
                    'lab': 15,
                    'nanoquiz': 5}
        scheme_2 = {'midterm': 23,
                    'final': 37,
                    'pset': 15,
                    'lab': 15,
                    'nanoquiz': 5,
                    'participation': 5}

        schemes = (scheme_1, scheme_2)
        scores = []

        by_category = {}
        for category in self.assignment_types:
            if category not in score_data: continue
            frac = self.calculate_average_in_category(score_data[category])
            by_category[category] = frac

        # we need to test both schemes
        for scheme_num, scheme in enumerate(schemes):
            earned, possible = 0, 0
            for category, weight in scheme.items():
                if category not in score_data: continue
                frac = by_category[category]
                delta_earned = weight*frac
                delta_possible = weight
                earned += delta_earned
                possible += delta_possible
            scores.append((earned, possible))

        # figure out which is better
        frac_1 = scores[0][0] / scores[0][1]
        frac_2 = scores[1][0] / scores[1][1]

        if frac_1 >= frac_2:
            output['best_score'] = scores[0]
            output['alt_scores'] = (scores[1],)
        else:
            output['best_score'] = scores[1]
            output['alt_scores'] = (scores[0],)
        output['by_category'] = by_category
        return output


if __name__ == "__main__":
    with open('../token.txt', 'r') as f:
        code_1, token_1 = f.readline().split(' ')
        code_2, token_2 = f.readline().split(' ')
    token = token_1
    raw_data = CatsoopRequests.request_data(token, class_code='6.200')
    preprocessed = CatsoopRequests.preprocess_data(raw_data.text)
    pprint.pp(preprocessed)
    for line in preprocessed:
        print(CatsoopRequests.get_numbers(line))
    parser = CircuitsParser()
    score_data = parser.parse_html(preprocessed)
    pprint.pp(score_data)
    out_score = parser.calculate_score(score_data)
    pprint.pp(out_score)
    best_score = out_score['best_score']
    pprint.pp(best_score[0] / best_score[1])

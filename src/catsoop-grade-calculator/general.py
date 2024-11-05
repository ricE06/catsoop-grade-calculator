"""
Provides a class to manage the different parsers.
"""

from parsers.request import CatsoopRequests
from parsers.circuits import CircuitsParser
from typing import Optional

class ScoreCalculator():

    parser_index = {'6.200': CircuitsParser,}
                    #'6.101': PyParser}

    def __init__(self, tokens: dict[str, str]) -> None:
        self.tokens = tokens
    
    def frac_to_percent(self, numer: float, denom: float) -> float:
        """
        Returns a float representing the percentage version of
        numer/denom, rounded.
        """
        return round(100 * numer / denom, 2)

    def generate_full_report(self, class_code: str, out_score: dict) -> str:
        """
        Given a class code and an out_score dictionary with
        attributes `best_score`, `alt_scores`, and `by_category`,
        generate a verbose report.
        """
        best = out_score['best_score']
        best_percent = self.frac_to_percent(*best)
        preface = '\n'.join(line.lstrip() for line in 
                        f"""==================================
                            GRADE REPORT FOR {class_code}: 
                            ==================================
                            OVERALL GRADE: ..........{best_percent}%
                            ....Points collected: ...{round(best[0], 2)}
                            ....Points possible: ....{round(best[1], 2)}"""
                            .split('\n')) # join-split needed to remove whitespace

        # ADD ALTERNATIVE SCORES, IF APPLICABLE
        alt_score_text = ""
        alt = out_score['alt_scores']
        if alt:
            alt_score_text = "\nALTERNATIVE SCORE(S):"
            percents = [self.frac_to_percent(*alt_score) for alt_score in alt]
            percents.sort(reverse=True)
            for score in percents:
                alt_score_text += f"\n....{score}%"

        # ADD THE CATEGORY BREAKDOWN
        by_category = out_score['by_category']
        category_text = '\nCATEGORY BREAKDOWN:'
        ordered_categories = list(by_category.keys())
        ordered_categories.sort()
        # align the scores to each other
        max_len = max(len(word) for word in ordered_categories)
        for category in ordered_categories:
            remaining_dots = 2 + max_len - len(category)
            score = round(100*by_category[category], 2)
            category_text += f"\n....{category}{'.'*remaining_dots}{score}%"

        return preface + alt_score_text + category_text

    def calculate_one(self, class_code: str) -> dict:
        """
        Calculates the grade for one class. 
        """
        if class_code not in ScoreCalculator.parser_index:
            raise NotImplementedError(
                    "This class doesn't have an implemented grade calculator!")
        token = self.tokens[class_code]
        raw_data = CatsoopRequests.request_data(token, class_code=class_code)
        preprocessed = CatsoopRequests.preprocess_data(raw_data.text)
        parser = ScoreCalculator.parser_index[class_code]()
        score_data = parser.parse_html(preprocessed)
        out_score = parser.calculate_score(score_data)
        return out_score
        

    def calculate_all(self) -> str:
        """
        Returns the expected overall grade.
        """
        raise NotImplementedError
        
if __name__ == "__main__":
    with open('token.txt', 'r') as f:
        circuits_token = f.readline()
    tokens = {'6.200': circuits_token}
    calc = ScoreCalculator(tokens)
    score = calc.calculate_one('6.200')
    report = calc.generate_full_report('6.200', score)
    print(report)


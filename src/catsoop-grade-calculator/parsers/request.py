"""
Requests and parses the html from CAT-SOOP.
"""

import requests
import pprint
from bs4 import BeautifulSoup
from typing import Optional
import re

# with open(token.txt, 'r') as f:
#     token = f.readline()

class CatsoopRequests():

    base_urls = {'6.101': 'https://py.mit.edu/fall24/progress',
                 '6.200': 'https://circuits.mit.edu/F24/progress'}

    default_kept_strs = ['<h', '<li>', '<tr><td', '<p>']

    @staticmethod
    def request_data(token: str, class_code: Optional[str] = None, url: Optional[str] = None):
        """
        Requests the progress page from CAT-SOOP and returns
        the Response object.
        """
        if url is None:
            url = CatsoopRequests.base_urls[class_code]
        params = {'api_token': token}
        return requests.get(url, params=params)

    @staticmethod
    def preprocess_data(inp_text: str, kept_strs: Optional[list[str]] = None) -> list[str]:
        """
        Gets rid of fluff from the start and splits into lines.
        """
        if kept_strs is None: kept_strs = CatsoopRequests.default_kept_strs
        lines = inp_text.splitlines()
        out = []
        started = False
        for line in lines:
            if not started:
                if "<h" not in line: # wait for first header
                    continue
                started = True
            for kept in kept_strs:
                if kept in line:
                    out.append(line)
                    break
        out_text = "\n".join(out)
        soup = BeautifulSoup(out_text, features="html.parser")
        for script in soup(['script', 'style']):
            script.extract() # remove html formatting things, leave text
        return soup.get_text().split('\n')

    @staticmethod
    def get_numbers(line):
        """
        Given a line of text, return only the numbers in it.
        """
        out = re.findall(r'[0-9\.]+', line)
        return [float(num) for num in out]

    @staticmethod
    def get_url(class_code):
        """
        Given a class code, returns the url. Returns None if
        the class code isn't supported.
        """
        return CatsoopRequests.base_urls.get(class_code, None)
            
if __name__ == "__main__":
    with open('token.txt', 'r') as f:
        token = f.readline()
    raw_data = CatsoopRequests.request_data(token, class_code='6.200')
    preprocessed = CatsoopRequests.preprocess_data(raw_data.text)
    pprint.pp(preprocessed)
    for line in preprocessed:
        print(CatsoopRequests.get_numbers(line))




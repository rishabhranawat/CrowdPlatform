## Generic from stack need to configure

from HTMLParser import HTMLParser
import requests

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


html = requests.get("https://en.wikipedia.org/wiki/Poisson_distribution").content
from django.utils.html import strip_tags
print(strip_tags(html))

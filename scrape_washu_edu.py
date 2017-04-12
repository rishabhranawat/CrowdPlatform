import requests
from bs4 import BeautifulSoup
import re

URL = "https://www.cs.washington.edu/education/courses"
content = requests.get(URL).content

soup = BeautifulSoup(content, 'html.parser')
spans = soup.findAll('span', attrs={'class': 'course-listing-title'})
links = set()
for span in spans:
	listings = span.findAll('a')
	url = listings[0].get('href')
	links.add(url)





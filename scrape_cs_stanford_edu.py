import requests
from bs4 import BeautifulSoup
import re

URL = "https://cs.stanford.edu/courses/schedules/2016-2017.spring.php"
content = requests.get(URL).content

soup = BeautifulSoup(content, 'html.parser')
anchors = soup.findAll('a', attrs={'href':re.compile(".Stanford\.EDU$")})
for anchor in anchors:
	print(anchor.get('href'))


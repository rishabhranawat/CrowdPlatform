# Get all Stanford Course Links -- Sum 15-16, Autumn 16-17, Winter 16-17, Spring 16-17

from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json
import time


# Gets per quarter course_links
def get_course_links(URL):
	course_pages = set()
	content = requests.get(URL).content
	soup = BeautifulSoup(content, 'html.parser')
	anchors = soup.findAll('a', attrs={'href':re.compile(".Stanford\.EDU$")})
	for anchor in anchors:
		course_pages.add(anchor.get('href'))
	return course_pages

# Gets stanford course page links
def get_stanford_course_page_links():
	urls= ["https://cs.stanford.edu/courses/schedules/2016-2017.spring.php",
	"https://cs.stanford.edu/courses/schedules/2016-2017.winter.php",
	"https://cs.stanford.edu/courses/schedules/2016-2017.spring.php",
	"https://cs.stanford.edu/courses/schedules/2015-2016.summer.php"]

	p = Pool(8)
	all_course_page_links = list(p.map(get_course_links, urls))
	course_pages = set()
	for each in all_course_page_links:
		course_pages = course_pages | each
	return course_pages



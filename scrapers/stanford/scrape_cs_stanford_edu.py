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


# Utils
def is_abs(url):
	return bool(urlparse.urlparse(url).netloc)

def check_url(url, host_url):
	if(host_url == url or url in all_course_pages):
		return ["circle", False]
	if(host_url in url and host_url != url):
		return ["abs", True]
	elif("mailto:" in url):
		return ["mail", False]
	else:
		return ["rel", not (is_abs(url))]

def get_absolute_path(host, rel):
	return urlparse.urljoin(host, rel)

def check_if_pdf(response):
	return response.headers['content-type']=='application/pdf'
		

# Getting the fro_links
def get_fro_links(course_home_page_url):
	# Soup Boiler Plate
	course_home_page_response = requests.get(course_home_page_url)	
	course_home_page = course_home_page_response.content
	course_home_page_soup = BeautifulSoup(course_home_page, 'html.parser')
	course_home_page_links = course_home_page_soup.findAll('a')
	
	# Getting the links from course_home_page
	course_home_page_fro_links = set()
	for link_fro_course_home in course_home_page_links:
		try:
			link_fro_course_home = link_fro_course_home.get("href")
			link_fro_course_home = link_fro_course_home.lstrip()

			typ, cond = check_url(link_fro_course_home, course_home_page_url)
			if(cond):
				link_to_add = link_fro_course_home
				if(typ == "rel"):
					link_to_add = get_absolute_path(course_home_page_url, 
						link_fro_course_home)
				if(course_home_page_url != link_to_add):
					course_home_page_fro_links.add(link_to_add)
		except:
			pass

	return course_home_page_fro_links

all_course_pages = list(get_stanford_course_page_links())
p = Pool(8)
all_for_links = list(p.map(get_fro_links, all_course_pages[:10]))
ll = set()
for each in all_for_links:
	ll = ll | each

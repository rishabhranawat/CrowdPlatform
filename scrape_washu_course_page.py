import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json

def is_abs(url):
	return bool(urlparse.urlparse(url).netloc)

def check_url(url):
	if("homework" in url):
		return True
	elif("hw" in url):
		return True	
	else:
		return not (is_abs(url))

def get_relative_path(host, rel):
	return urlparse.urljoin(host, rel)

def check_if_pdf(response):
	return response.headers['content-type']=='application/pdf'
		

all_course_pages = []
with open("wash_links.json") as f:
	d = json.load(f)
	for course_index, pages in d.items():
		all_course_pages.extend(pages)

all_course_pages[:10]
for course_home_page_url in all_course_pages:
	course_home_page = requests.get(course_home_page_url).content
	course_home_page_soup = BeautifulSoup(course_home_page, 'html.parser')
	course_home_page_links = course_home_page_soup.findAll('a')
	course_home_page_fro_links = set()
	for link_fro_course_home in course_home_page_links:
		try:
			if(check_url(link_fro_course_home.get("href"))):
				course_home_page_fro_links.add(link_fro_course_home.get("href"))
		except:
			pass

	for each in course_home_page_fro_links:
		print(each)
import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json

# Utils
def is_abs(url):
	return bool(urlparse.urlparse(url).netloc)

def check_url(url):
	if("homework" in url):
		return ["homework", True]
	elif("hw" in url):
		return ["hw", True]	
	else:
		return ["rel", not (is_abs(url))]

def get_absolute_path(host, rel):
	return urlparse.urljoin(host, rel)

def check_if_pdf(response):
	return response.headers['content-type']=='application/pdf'
		

# Getting all links from washu_index
all_course_pages = []
with open("wash_links.json") as f:
	d = json.load(f)
	for course_index, pages in d.items():
		all_course_pages.extend(pages)


# Getting all the course_home_page stuff
for course_home_page_url in all_course_pages[:2]:

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
			typ, cond = check_url(link_fro_course_home)
			if(cond):
				link_to_add = link_fro_course_home
				if(typ == "rel"):
					link_to_add = get_absolute_path(course_home_page_url, 
						link_fro_course_home)
				if(course_home_page_url != link_to_add):
					course_home_page_fro_links.add(link_to_add)
		except:
			print(link_fro_course_home)




import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json
import time

# TO DO: Download related files
# TO DO: MAKE THIS MULTITHREADED

# Utils
def is_abs(url):
	return bool(urlparse.urlparse(url).netloc)

def check_url(url, host_url, all_course_pages):
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
		

# Getting all link_to_addnks from washu_index
all_course_pages = []
with open("wash_links.json") as f:
	d = json.load(f)
	for course_index, pages in d.items():
		all_course_pages.extend(pages)

ts = time.time()
# Getting all the course_home_page stuff
for course_home_page_url in all_course_pages[:10]:
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

			typ, cond = check_url(link_fro_course_home, course_home_page_url, all_course_pages)
			if(cond):
				link_to_add = link_fro_course_home
				if(typ == "rel"):
					link_to_add = get_absolute_path(course_home_page_url, 
						link_fro_course_home)
				if(course_home_page_url != link_to_add):
					course_home_page_fro_links.add(link_to_add)
		except:
			pass
print(time.time() - ts)


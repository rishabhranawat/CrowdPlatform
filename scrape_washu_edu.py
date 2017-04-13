import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json

def is_abs(url):
	return bool(urlparse.urlparse(url).netloc)

def get_relative_path(host, rel):
	return urlparse.urljoin(host, rel)

def get_washu_courses_page():
	COURSES_CS_WASHU = "https://www.cs.washington.edu/education/courses"
	content = requests.get(COURSES_CS_WASHU).content
	courses_washu = BeautifulSoup(content, 'html.parser')
	spans = courses_washu.findAll('span', 
		attrs={'class': 'course-listing-title'})
	courses = set()
	for span in spans:
		listings = span.findAll('a')
		url = listings[0].get('href')
		courses.add(url)
	return courses

def get_all_courses_links(courses):
	course_past_courses = {}
	for COURSES_CS_WASHU_COURSE_INDEX in courses:
			try:
				content = requests.get(COURSES_CS_WASHU_COURSE_INDEX).content
				course_past_courses[COURSES_CS_WASHU_COURSE_INDEX] = []

				course_index = BeautifulSoup(content, 'html.parser')    
				past_course_index = course_index.find('div',
				 attrs={'id':'block-menu-menu-news-and-events'})
				past_course_links = past_course_index.findAll('a')
				for past_course_link in past_course_links:
					pcl = past_course_link.get('href')
					if(is_abs(pcl)):
						course_past_courses[COURSES_CS_WASHU_COURSE_INDEX].append(\
							get_relative_path(
								COURSES_CS_WASHU_COURSE_INDEX, pcl))
			except:
				print(COURSES_CS_WASHU_COURSE_INDEX)
	return course_past_courses

with open("wash_links.json", "w") as f:
	data = get_all_courses_links(get_washu_courses_page())
	json.dump(data, f)

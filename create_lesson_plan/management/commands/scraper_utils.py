from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import json
import time
from time import sleep
import hashlib
from create_lesson_plan.models import OfflineDocument
from django.core.files import File


FILE_TYPES = ["application/pdf", "pdf"]
WASHU_STOP_URLS = ["http://courses.cs.washington.edu/", "/", 
"http://cs.stanford.edu/academics/courses", 
"https://ocw.mit.edu/courses/", "https://ocw.mit.edu/"]


def create_offline_document_object(content_page_url, content, univeristy, subject, 
	f=None, file_name=None):
	
	off_doc = OfflineDocument(link=content_page_url, 
		source=univeristy, 
		subject=subject, 
		content=content)
	if(f): 
		off_doc.attachment.save(file_name, File(open(file_name, 'r')))
	off_doc.save()
	print(str(off_doc.pk)+" "+off_doc.link)
	return True

def download_files_load_es(all_course_pages, level, university,subject,content_page_url):
	try:
		content_page_response = requests.get(content_page_url)
		if(content_page_response != None):
			try:
				content_page = content_page_response.content
				ext_type, file_type = get_file_type(content_page_url, content_page_response)
				if(ext_type in FILE_TYPES):	
					file_name = content_page_url.split("/")[-1]
					f = download_pdf_file(content_page_url, file_name, 
						content_page_response)
					create_offline_document_object(content_page_url, 
						'pdf attached', 
						university, subject, 
						f, file_name)
					return set()
				elif(ext_type not in FILE_TYPES and level == 1):
					return get_fro_links(all_course_pages, content_page_url, content_page_response)
				elif(file_type not in FILE_TYPES 
					and ext_type not in FILE_TYPES and level == 2 and "text/html" in file_type):
					create_offline_document_object(content_page_url, content_page_response.content, 
						university, subject)
			except Exception as e:
				print(e)
				print("Error: ", content_page_url)
				return set()

		else:
			if(level == 1): return set()
			if(level == 2): pass
	except:
		if(level == 1): return set()
		if(level == 2): pass
def download_pdf_file(download_url, name, response):
	response = urllib2.urlopen(download_url)
	file = open(name, 'w')
	file.write(response.read())
	file.close()
	return file

def get_file_type(url, response):
	return url.split('.')[-1].replace(" ", ""), response.headers['content-type']

def get_sha_encoding(content):
	return 1

def get_page_content_response(url):
	counter = 0
	page_response = requests.get(url)
	# while(counter <=2 and page_response == None):
	# 	print(page_response)
	# 	counter += 1
	# 	try:
	# 		page_response = requests.get(url)
	# 	except:
	# 		sleep(1)
	# 		continue
	return page_response

def is_abs(url):
	return bool(urlparse.urlparse(url).netloc)

def check_url(url, host_url, all_course_pages):
	if(url in WASHU_STOP_URLS):
		return ["circle", False]
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
		
def get_fro_links(all_course_pages, course_home_page_url, course_home_page_response):
	# Soup Boiler Plate
		
	if(course_home_page_response != None):
		course_home_page = course_home_page_response.content
		course_home_page_soup = BeautifulSoup(course_home_page, 'html.parser')
		course_home_page_links = course_home_page_soup.findAll('a')
		
		# Getting the links from course_home_page
		course_home_page_fro_links = set()
		for link_fro_course_home in course_home_page_links:
			try:
				link_fro_course_home = link_fro_course_home.get("href")
				link_fro_course_home = link_fro_course_home.lstrip()

				typ, cond = check_url(link_fro_course_home, 
					course_home_page_url, 
					all_course_pages)
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
	else:
		return set()
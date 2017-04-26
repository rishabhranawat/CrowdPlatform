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


FILE_TYPES = ["application/pdf"]
WASHU_STOP_URLS = ["http://courses.cs.washington.edu/", "/", 
"http://cs.stanford.edu/academics/courses"]

def download_files_load_es(all_course_pages, level, university,subject,content_page_url):
	content_page_response = get_page_content_response(content_page_url)
	if(content_page_response != None):
		content_page = content_page_response.content
		content_page_soup = BeautifulSoup(content_page, 'html.parser')

		file_type = get_file_type(content_page_url, content_page_response)

		# TO:DO -- Download
		if(file_type in FILE_TYPES):
			file_name = content_page_url.split("/")[-1]
			f, response = download_pdf_file(content_page_url, file_name)
			create_offline_document_object(content_page_url, 
				response.read(), 
				university, subject, 
				f, file_name)
			print(content_page_url)
			return set()
		elif(file_type not in FILE_TYPES and level == 1):
			return get_fro_links(all_course_pages, content_page_url)
		elif(file_type not in FILE_TYPES and level == 2):
			create_offline_document_object(content_page_url, content_page_soup.content, 
				university, subject)
			print(content_page_url)
	else:
		if(level == 1): return set()
		if(level == 2): pass


def create_offline_document_object(content_page_url, content, univeristy, subject, 
	f=None, file_name=None):
	try:
		off_doc = OfflineDocument(link=content_page_url, 
			source=univeristy, 
			subject=subject, 
			content=content)
		if(f): 
			off_doc.attachment.save(file_name, File(open(file_name, 'r')))
			os.remove(file_name)		
		off_doc.save()
		print(str(off_doc.pk)+" "+off_doc.link)
		return True
	except:
		return False


def download_pdf_file(download_url, name):
    response = urllib2.urlopen(download_url)
    file = open(name, 'w')
    file.write(response.read())
    file.close()
    return file, response

def get_file_type(url, response):
	return response.headers['content-type']

def get_sha_encoding(content):
	return 1

def get_page_content_response(url):
	print(url)
	counter = 0
	page_response = None
	while(counter <=5 and page_response == None):
		print(page_response)
		counter += 1
		try:
			page_response = requests.get(url)
		except:
			sleep(1)
			continue
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
		
def get_fro_links(all_course_pages, course_home_page_url):
	# Soup Boiler Plate
	
	course_home_page_response = get_page_content_response(course_home_page_url)	
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
from django.core.management.base import BaseCommand
from django.core.files import File

from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json
import time
from functools import partial
import hashlib
import os

from scraper_utils import get_file_type, get_sha_encoding, get_fro_links, download_pdf_file
from scraper_utils import get_page_content_response, download_files_load_es

from create_lesson_plan.models import OfflineDocument


def get_sub_level(all_course_pages, level, university, subject, content_page_url):
	new_links_or_none = download_files_load_es(all_course_pages, level, university, subject, content_page_url)
	return new_links_or_none

def write_to_file(home_page_urls):
	with open('mit_ocw_links.txt', "w") as f:
		for url in home_page_urls:
			f.write('%s \n'% url)
	f.close()


def download_level_1_links(content_page_url, course_page):
	course_home_page_response = requests.get(content_page_url)
	home_page_urls = list(get_fro_links([course_page], 
		content_page_url, course_home_page_response))

	all_level_1_links = set()
	for each_url in home_page_urls:

		new_links = get_sub_level([course_page], 1, 
			"MIT", "Computer Science", each_url)
		time.sleep(2)

		if(new_links != None):
			all_level_1_links = all_level_1_links | new_links
	
	all_level_1_links = list(all_level_1_links)
	write_to_file(all_level_1_links)

def get_level_1_links():
	f = open('mit_ocw_links.txt', 'r')
	links = f.read().splitlines()
	return links

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		content_page_url = "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-828-operating-system-engineering-fall-2012/labs/"
		course_page = "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-828-operating-system-engineering-fall-2012/labs/"
		download_level_1_links(content_page_url, course_page)
		# all_level_1_links = ["https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-828-operating-system-engineering-fall-2012/lecture-notes-and-readings/"]
		# for final_depth_url in all_level_1_links:
		# 	if(not OfflineDocument.objects.filter(link=final_depth_url).exists()):
		# 		print("Request ", final_depth_url)
		# 		get_sub_level([course_page], 2, 
		# 			"MIT", "Computer Science", final_depth_url)
		# 		time.sleep(2)

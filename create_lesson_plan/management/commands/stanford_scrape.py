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


def get_all_sub_level(content_page_urls, all_course_pages, typ):
	p = Pool(8)
	func = partial(download_files_load_es, all_course_pages, typ, "Stanford University", "Computer Science")

	if(typ == 1):
		all_sub_level_1_links = list(p.map(func, content_page_urls)) 
		ll = set()
		for each in all_sub_level_1_links:
			ll = ll | each
		return ll
	else:
		p.map(func, content_page_urls)


def get_sub_level(all_course_pages, level, university, subject, content_page_url):
	new_links_or_none = download_files_load_es(all_course_pages, level, university, subject, content_page_url)
	return new_links_or_none

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		content_page_url = "http://web.stanford.edu/class/cs103/"
		course_page = "http://web.stanford.edu/class/cs103/"

		course_home_page_response = requests.get(content_page_url)
		home_page_urls = list(get_fro_links([course_page], 
			content_page_url, course_home_page_response))[:1]

		all_level_1_links = set()
		for each_url in home_page_urls:
			new_links = get_sub_level([course_page], 1, 
				"New York University", "Computer Science", each_url)
			time.sleep(2)

			if(new_links != None):
				all_level_1_links = all_level_1_links | new_links
		
		all_level_1_links = list(all_level_1_links)
		

		for final_depth_url in all_level_1_links:
			print(final_depth_url)

			get_sub_level([course_page], 2, 
				"New York University", "Computer Science", final_depth_url)
			time.sleep(2)

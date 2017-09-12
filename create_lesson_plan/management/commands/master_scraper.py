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
from Queue import Queue

from create_lesson_plan.models import OfflineDocument

from scraper_utils import get_file_type, get_sha_encoding, get_fro_links, download_pdf_file
from scraper_utils import get_page_content_response, download_files_load_es

import threading

def get_sub_level(all_course_pages, level, university, subject, content_page_url):
	new_links_or_none = download_files_load_es(all_course_pages, level, university, subject, content_page_url)
	return new_links_or_none

def download_level_1_links(url, university, subject):
	course_home_page_response = requests.get(url)
	home_page_urls = list(get_fro_links([url], 
	url, course_home_page_response))

	all_level_1_links = set()
	for each_url in home_page_urls:
		print(each_url)
		new_links = get_sub_level([url], 1, 
			university, subject, each_url)

		if(new_links != None):
			all_level_1_links = all_level_1_links | new_links
		time.sleep(2)
	
	return list(all_level_1_links)

def spawn_crawlers(dets):
	url = dets["url"]
	university = dets["university"]
	subject = dets["subject"]

	all_level_1_links = download_level_1_links(
		url, university, subject)

	for final_depth_url in all_level_1_links:
		url = final_depth_url.strip()
		print(final_depth_url)
		if(not OfflineDocument.objects.filter(link=url).exists()):
			get_sub_level([course_page], 2, university, subject, url)
			time.sleep(5)

class Command(BaseCommand):
	def __init__(self):
		self.visited = set()

	def get_sub_level(all_course_pages, level, university, subject, content_page_url):
		new_links_or_none = download_files_load_es(all_course_pages, level, university, subject, content_page_url)
		return new_links_or_none

	def add_arguments(self, parser):
		parser.add_argument('--seed', nargs='+', type=str)

	def get_seed_urls(self, seed):
		with open(seed, "r") as f:
			d = json.load(f)
		return d

	def handle(self, *args, **options):
		seed_urls = self.get_seed_urls(options['seed'][0])
		p = Pool(2)
		func = partial(spawn_crawlers)
		p.map(func, seed_urls)


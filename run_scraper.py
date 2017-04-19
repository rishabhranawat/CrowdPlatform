from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json
import time
from functools import partial
import hashlib

from scraper_utils import get_file_type, get_sha_encoding, get_fro_links
from scrape_washu_multi import get_all_content_urls
# from create_lesson_plan.models import OfflineDocument

def download_files_load_es(all_course_pages, content_page_url):
	content_page_response = requests.get(content_page_url)
	content_page = content_page_response.content
	content_page_soup = BeautifulSoup(content_page, 'html.parser')
	
	file_type = get_file_type(content_page_url, content_page_response)
	
	# TO:DO -- Download
	if(file_type == "application/pdf"):
		return set()
	else:
		return get_fro_links(all_course_pages, content_page_url)

def get_all_sub_level_1():
	content_page_urls, all_course_pages = get_all_content_urls()
	content_page_urls = list(content_page_urls)
	
	p = Pool(8)
	func = partial(download_files_load_es, all_course_pages)
	all_sub_level_1_links = list(p.map(func, content_page_urls)) 
	ll = set()
	for each in all_sub_level_1_links:
		ll = ll | each

	for each in ll:
		print(each)

get_all_sub_level_1()
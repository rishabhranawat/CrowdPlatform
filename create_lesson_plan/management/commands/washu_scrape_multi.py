from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json
import time
from scraper_utils import get_fro_links
from functools import partial

	
# Getting all link_to_addnks from washu_index
def get_all_course_pages():
	all_course_pages = []
	with open("wash_links.json") as f:
		d = json.load(f)
		for course_index, pages in d.items():
			all_course_pages.extend(pages)
	return all_course_pages

def get_all_content_urls():
	all_course_pages = get_all_course_pages()
	p = Pool(8)
	func = partial(get_fro_links, all_course_pages)
	all_for_links = list(p.map(func, all_course_pages[:1]))
	ll = set()
	for each in all_for_links:
		ll = ll | each
	return ll, all_course_pages

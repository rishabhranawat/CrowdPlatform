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

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		content_page_url = "http://www.scs.stanford.edu/17wi-cs140/"
		course_page = "http://www.scs.stanford.edu/17wi-cs140/"

		content_page_urls = get_all_sub_level([content_page_url], [course_page], 1)
		content_page_urls_2 = get_all_sub_level([content_page_urls], [course_page], 2)

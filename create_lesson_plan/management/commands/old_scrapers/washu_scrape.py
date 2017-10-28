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
from scraper_utils import get_page_content_response,create_offline_document_object
from scraper_utils import download_files_load_es

from washu_scrape_multi import get_all_content_urls
from create_lesson_plan.models import OfflineDocument


def get_all_sub_level(content_page_urls, all_course_pages, typ):
	p = Pool(8)
	func = partial(download_files_load_es, all_course_pages, typ)

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
		# Level 1
		content_page_urls, all_course_pages = get_all_content_urls()
		content_page_urls = list(content_page_urls)
		content_page_urls_2 = get_all_sub_level(content_page_urls, all_course_pages, 1)

		# Level 2s
		print(len(content_page_urls_2))
		content_page_urls_3 = get_all_sub_level(content_page_urls_2, all_course_pages, 2)
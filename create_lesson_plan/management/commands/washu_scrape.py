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

from scraper_utils import get_file_type, get_sha_encoding, get_fro_links, download_pdf_file
from washu_scrape_multi import get_all_content_urls
from create_lesson_plan.models import OfflineDocument

FILE_TYPES = ["application/pdf"]

def create_offline_document_object(content_page_url, content, f, file_name):
	off_doc = OfflineDocument(link=content_page_url, source='University of Washington', subject='Computer Science', content=content)
	if(f): off_doc.attachment.save(file_name, File(open(file_name, 'r')))
	off_doc.save()
	return True

def download_files_load_es(all_course_pages, level, content_page_url):
	content_page_response = requests.get(content_page_url)
	content_page = content_page_response.content
	content_page_soup = BeautifulSoup(content_page, 'html.parser')
	
	file_type = get_file_type(content_page_url, content_page_response)
	
	# TO:DO -- Download
	if(file_type in FILE_TYPES):
		f = download_pdf_file(content_page_url, content_page_url.split("/")[-1])

		return set()
	elif(file_type not in FILE_TYPES and level == 1):
		return get_fro_links(all_course_pages, content_page_url)
	elif(file_type not in FILE_TYPES and level == 2):
		

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
		get_all_sub_level(content_page_urls_2, all_course_pages, 2)

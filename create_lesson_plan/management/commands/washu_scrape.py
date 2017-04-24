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
from scraper_utils import get_page_content_response

from washu_scrape_multi import get_all_content_urls
from create_lesson_plan.models import OfflineDocument

FILE_TYPES = ["application/pdf"]

def create_offline_document_object(content_page_url, content, f=None, file_name=None):
	try:
		off_doc = OfflineDocument(link=content_page_url, 
			source='University of Washington', 
			subject='Computer Science', 
			content=content)
		if(f): 
			off_doc.attachment.save(file_name, File(open(file_name, 'r')))
			os.remove(file_name)		
		off_doc.save()
		print(str(off_doc.pk)+" "+off_doc.link)
		return True
	except:
		return False

def download_files_load_es(all_course_pages, level, content_page_url):

	content_page_response = get_page_content_response(content_page_url)
	if(content_page_response != None):
		content_page = content_page_response.content
		content_page_soup = BeautifulSoup(content_page, 'html.parser')

		file_type = get_file_type(content_page_url, content_page_response)

		# TO:DO -- Download
		if(file_type in FILE_TYPES):
			# file_name = content_page_url.split("/")[-1]
			# f, response = download_pdf_file(content_page_url, file_name)
			# create_offline_document_object(content_page_url, response.read(), f, file_name)
			print(content_page_url)
			return set()
		elif(file_type not in FILE_TYPES and level == 1):
			return get_fro_links(all_course_pages, content_page_url)
		elif(file_type not in FILE_TYPES and level == 2):
			# create_offline_document_object(content_page_url, content_page_soup.content)
			print(content_page_url)
	else:
		if(level == 1): return set()
		if(level == 2): pass

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
		# content_page_urls_3 = get_all_sub_level(content_page_urls_2, all_course_pages, 2)
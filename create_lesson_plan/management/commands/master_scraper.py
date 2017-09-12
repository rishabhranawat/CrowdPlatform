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

class Command(BaseCommand):
	def __init__(self):
		self.visited = set()
		self.seed_urls = set()

	def add_arguments(self, parser):
		parser.add_argument('--seed', nargs='+', type=str)

	def get_seed_urls(self, seed):
		with open(seed, 'r') as f:
			lines = f.readlines()
			self.seed_urls = set([i.replace("\n",  "") for i in lines])
		return self.seed_urls

	# def fetch_urls(self, url, q, next_level):
		


	def handle(self, *args, **options):
		self.get_seed_urls(options['seed'][0])

		queues = []
		for each in self.seed_urls:
			queues.append(Queue())

		p = Pool(8)


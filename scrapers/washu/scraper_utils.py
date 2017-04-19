from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import re
import urlparse
import json
import time
import hashlib

def get_file_type(url, response):
	print(url+" "+response.headers['content-type'])

def get_sha_encoding(content):
	return 1

def save_doc_in_els():

def download_files_load_es(content_page_url):
	content_page_response = requests.get(content_page_url)
	content_page = content_page_response.content
	content_page_soup = BeautifulSoup(content_page, 'html.parser')

	file_type = get_file_type(content_page_url, content_page_response)

	if(file_type == "application/pdf"):







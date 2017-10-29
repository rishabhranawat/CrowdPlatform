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

Command(BaseCommand):
	def __init__(self):
		self.visited = set()
	
	def handle(self, *args, **options):
		pass


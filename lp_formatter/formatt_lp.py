import urllib2
import xml.etree.cElementTree as ET
import logging

from bs4 import BeautifulSoup
from xml.dom import minidom


from create_lesson_plan.models import *
from django.db.models import Q

def format_lesson(root, lesson):
	engage_urls = Engage_Urls.objects.filter(lesson_fk = lesson)
	
	doc = ET.SubElement(root, "lesson")

	for url in engage_urls:
		try: 
			
			title = url.title
			link = url.display_url

			ET.SubElement(doc, "url", name="url").text = str(link).encode("utf-8")
			ET.SubElement(doc, "title", name="title").text = str(title).encode("utf-8")
		except:
			continue

	evaluate_urls = Evaluate_Urls.objects.filter(lesson_fk=lesson)
	for url in evaluate_urls:
		try:
			title = url.title
			link = url.display_url

			ET.SubElement(doc, "url", name="url").text = str(link).encode("utf-8")
			ET.SubElement(doc, "title", name="title").text = str(title).encode("utf-8")
		except:
			continue
	

l = lesson.objects.filter(Q(stage = 1)).reverse()

logging.info('Formatting %d lesson plans', l.count())

root = ET.Element("root")
for each in l:
	format_lesson(root, each)

tree = ET.ElementTree(root)
tree.write("gauiss_formatted_lesson_plan.xml")
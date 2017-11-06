from django.core.management.base import BaseCommand

from create_lesson_plan.models import OfflineDocument

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	
	def handle_data(self, d):
		self.fed.append(d)
	
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

class Command(BaseCommand):
	def __init__(self):
		pass

	def get_es_docs_dump(self):
		client = Elasticsearch()
		page = client.search(index="offline_content", doc_type="offline_document",
                        scroll="2m", size=50, body={})
                sid = page['_scroll_id']
                scroll_size = page['hits']['total']
	    	f = open("text_corpus/data.txt", "a")
                tots = 50
                while(scroll_size > 0 and tots < 2000):
                    hits = page['hits']['hits']
                    for each_hit in hits:
                        source_data = each_hit['_source']
                        content = source_data['content'].encode('utf-8')
                        if(content == 'pdf attached' or content=='doc attached'):
                            print(source_data['attachment'].keys())
                            if("content" in source_data['attachment']):
                                content = source_data['attachment']['content'].encode('utf-8')
                        f.write(content)
                    page = client.scroll(scroll_id=sid, scroll="2m")
                    sid = page["_scroll_id"]
                    scroll_size = len(page['hits']['hits'])
                    tots += 50
                    print("scroll size" + str(scroll_size))

                f.close()

	def handle(self, *args, **options):
		self.get_es_docs_dump()

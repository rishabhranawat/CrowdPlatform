import scrapy
from scrapy.item import Item, Field

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from django.utils.html import strip_tags
from create_lesson_plan.models import OfflineDocument
from django.core.management.base import BaseCommand


# LinkObject just to store the link temporarily
class LinkObject(Item):
    link = Field()

link_objs = [] # global variable that stores all links to be crawld
INDEX = "nicaragua_wiki_3"

# Initial Starter Spider
class WikipediaSpider(scrapy.Spider):
	name = 'wikipediaspider'
	start_urls = ['https://es.wikipedia.org/wiki/Ingenier%C3%ADa_de_sistemas']
	def parse(self, response):
		print("\n \n here \n \n"+response.css('title').extract()[0])
		if(len(OfflineDocument.objects.filter(link=response.url, , index_name=INDEX)) == 0):
			off_doc = OfflineDocument(link=response.url,\
				content=strip_tags(response.text),\
				title=response.css('title').extract()[0],\
				source='wikipedia', index_name=INDEX)
			off_doc.save()
		for url in response.css('a'):
			new_link = response.urljoin(url.xpath('@href').extract_first())
			if(len(OfflineDocument.objects.filter(link=new_link, , index_name=INDEX)) == 0):
				link_obj = LinkObject()
				link_obj['link'] = new_link
				link_objs.append(link_obj)
		return link_objs

# Level 1 Spider
class Level1Spider(scrapy.Spider):
	name = "level1spider"
	start_urls = []

	def __init__(self):
		global link_objs
		for link_obj in link_objs:
			url = link_obj['link']
			if(url is not None):
				self.start_urls.append(link_obj['link'])
		link_objs = []

	def parse(self, response):
		if(len(OfflineDocument.objects.filter(link=response.url, index_name=INDEX)) == 0):
			off_doc = OfflineDocument(link=response.url,\
				content=strip_tags(response.text),\
				title=response.css('title').extract()[0],\
				source='wikipedia', index_name=INDEX)
			off_doc.save()

		for url in response.css('a'):
			new_link = response.urljoin(url.xpath('@href').extract_first())
			if(len(OfflineDocument.objects.filter(link=new_link, , index_name=INDEX)) == 0):
				link_obj = LinkObject()
				link_obj['link'] = new_link
				link_objs.append(link_obj)
		return link_objs

# Level 2 Spider
class Level2Spider(scrapy.Spider):
	name = "level2spider"
	start_urls = []

	def __init__(self):
		global link_objs
		for link_obj in link_objs:
			url = link_obj['link']
			if(url is not None):
				self.start_urls.append(link_obj['link'])
		link_objs = []

	def parse(self, response):
		if(len(OfflineDocument.objects.filter(link=response.url, index_name=INDEX)) == 0):
			off_doc = OfflineDocument(link=url,\
				content=strip_tags(response.text),\
				title=response.css('title').extract()[0],\
				source='wikipedia', index_name=INDEX)
			off_doc.save()
		return link_objs


class Command(BaseCommand, scrapy.Spider):
	runner = CrawlerRunner()
	def handle(self, *args, **options):
		configure_logging()
		self.crawl()
		reactor.run()

	@defer.inlineCallbacks
	def crawl(self):
		yield self.runner.crawl(WikipediaSpider)
		yield self.runner.crawl(Level1Spider)
		yield self.runner.crawl(Level2Spider)
		reactor.stop()



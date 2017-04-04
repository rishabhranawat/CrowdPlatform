import scrapy
from scrapy.item import Item, Field

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from django.utils.html import strip_tags
from create_lesson_plan.models import OfflineDocument
from django.core.management.base import BaseCommand

class LinkObject(Item):
    link = Field()

link_objs = []
class WikipediaSpider(scrapy.Spider):
	name = 'wikipediaspider'
	start_urls = ['https://en.wikipedia.org/wiki/Portal:Computer_science']
	count = 0
	def parse(self, response):
		off_doc = OfflineDocument(link=response.url,\
			content=strip_tags(response.text),\
			source='wikipedia')
		off_doc.save()
		for url in response.css('a'):
			self.count +=1 
			link_obj = LinkObject()
			link_obj['link'] = response.urljoin(url.xpath('@href').extract_first())
			link_objs.append(link_obj)
		return link_objs

class Level1Spider(scrapy.Spider):
	name = "level1spider"
	start_urls = []

	def __init__(self, higher_link_objs):
		for link_obj in higher_link_objs:
			url = link_obj['link']
			if(url is not None):
				self.start_urls.append(link_obj['link'])

	def parse(self, response):
		off_doc = OfflineDocument(link=response.url,\
			content=strip_tags(response.text),\
			source='wikipedia')
		off_doc.save()
		for url in response.css('a'):
			link_obj = LinkObject()
			link_obj['link'] = url.xpath('@href').extract_first()
			link_objs.append(link_obj)
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
		reactor.stop()



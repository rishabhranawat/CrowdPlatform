import scrapy
from scrapy.item import Item, Field

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


class LinkObject(Item):
    link = Field()
    content = Field()

link_objs = []
class WikipediaSpider(scrapy.Spider):
	name = 'wikipediaspider'
	start_urls = ['https://en.wikipedia.org/wiki/Portal:Computer_science']
	def parse(self, response):
		for url in response.css('a'):
			link_obj = LinkObject()
			link_obj['link'] = response.urljoin(url.xpath('@href').extract_first())
			link_obj['content'] = response.text
			link_objs.append(link_obj)

class Level1Spider(scrapy.Spider):
	name = "level1spider"
	start_urls = []

	def __init__(self):
		for link_obj in link_objs:
			url = link_obj['link']
			if(url is not None):
				self.start_urls.append(link_obj['link'])

	def parse(self, response):
		for url in response.css('a'):
			link_obj = LinkObject()
			link_obj['link'] = url.xpath('@href').extract_first()
			link_obj['content'] = response.text
			link_objs.append(link_obj)


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(WikipediaSpider)
    yield runner.crawl(Level1Spider)
    reactor.stop()

crawl()
reactor.run() 
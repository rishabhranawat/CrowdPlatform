import scrapy
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess


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
			link_obj['link'] = url.xpath('@href').extract_first()
			link_obj['content'] = response.text
			link_objs.append(link_obj)


class Level1Spider(scrapy)
	name = "level1spider"
	start_urls =[]

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(WikipediaSpider)
process.start()
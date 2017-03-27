import scrapy

class WikipediaSpider(scrapy.Spider):
	name = 'wikipediaspider'
	start_urls = ['https://en.wikipedia.org/wiki/Portal:Computer_science']
	
	def parse(self, response):
		links = response.css('a')
		links_urls = []
		for each in links:
			print(each)
			links_urls.append(each.xpath('@href').extract_first())
		print("\n \n \n")
		next_page = "https://en.wikipedia.org/wiki/Poisson_distribution"
		if next_page is not None:
			yield scrapy.Request(next_page, callback=self.parse)

# import scrapy


# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'http://quotes.toscrape.com/page/1/',
#     ]

#     def parse(self, response):
#         # for quote in response.css('div.quote'):
#         #     yield {
#         #         'text': quote.css('span.text::text').extract_first(),
#         #         'author': quote.css('small.author::text').extract_first(),
#         #         'tags': quote.css('div.tags a.tag::text').extract(),
#         #     }

#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)
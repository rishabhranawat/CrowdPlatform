from django.core.management.base import BaseCommand

from general_scraper import GeneralSeedScraper

class Command(BaseCommand):
	def __init__(self):
		self.visited = set()
	
	def handle(self, *args, **options):
		gss = GeneralSeedScraper()
		gss.initialize_scraper('seeds_generator/seeds.txt')


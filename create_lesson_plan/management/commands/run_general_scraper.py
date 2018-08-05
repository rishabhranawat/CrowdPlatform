from django.core.management.base import BaseCommand

from multiprocessing import Pool
from functools import partial
from create_lesson_plan.models import OfflineDocument, IndexDocument
from general_scraper import GeneralSeedScraper

def spawn_tasks(link):
	gss = GeneralSeedScraper()
	gss.run_scraper(link)


class Command(BaseCommand):
	def __init__(self):
		self.visited = set()
	
    def get_seed_links(self, file_name):
        	f = open(file_name, 'r')
        	lines = f.readlines()
        	seed_links = [x.strip() for x in lines]
       	 	f.close()
        	return seed_links

	
	def handle(self, *args, **options):
		seeds = self.get_seed_links('seeds_generator/seeds_os_feb.txt')
                res_seeds = []
                for each_link in seeds:
                    num = len(IndexDocument.objects.filter(link=each_link))
                    if(num == 0): 
                        res_seeds.append(each_link)
                final_seeds = res_seeds
                p = Pool(2)
                func = partial(spawn_tasks)
                p.map(func, final_seeds)

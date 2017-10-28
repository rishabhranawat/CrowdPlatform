from django.core.management.base import BaseCommand

from multiprocessing import Pool
from functools import partial
from Queue import Queue

import threading

from create_lesson_plan.models import OfflineDocument
from create_lesson_plan.graph_query.query_formulator_poc import GraphQueryFormulator
from create_lesson_plan.pyms_cog import *

class Command(BaseCommand):
	def __init__(self):
	    self.links = set()
            
        def get_graph_nodes(self):
            gqf = GraphQueryFormulator()
            nodes = gqf.kg.nodes
            l = [str(x) for x in nodes]
            return l

        def get_links_query(self, query):
            query_links = set()
            results = bing_search(query, 2)
            for each_link in results:
                query_links.add(each_link['display_url'])
            return query_links
  
        def dump_links_file(self):
            with open('my_new_seeds.txt', 'w') as f:
                for link in self.links:
                    f.write("%s \n", link)
            return

	def handle(self, *args, **options): 
            queries = self.get_graph_nodes()[:2]
            p = Pool(4)
            func = partial(get_links_query)
            results = p.map(func, queries)
            for each in results:
                self.links |= results
                


from django.core.management.base import BaseCommand

from multiprocessing import Pool
from functools import partial
from Queue import Queue
import requests

import threading

from create_lesson_plan.models import OfflineDocument
from create_lesson_plan.graph_query.query_formulator_poc import GraphQueryFormulator
from create_lesson_plan.pyms_cog import *



class Command(BaseCommand):
	def __init__(self):
	    self.links = set()

	def get_existing(self, file_name):
		l = []
		with open(file_name, 'r') as f:
			l = f.readlines()
		res = [x.strip() for x in l]
		return res

	def dump_visited_queries(self, nodes):
		with open('seeds_generator/visited_queries.txt', 'a') as f:
			for each_node in nodes:
				f.write(each_node)
				f.write("\n")
		return

	def get_graph_nodes(self):
		visited_queries = self.get_existing('seeds_generator/visited_queries.txt')
		gqf = GraphQueryFormulator()
		nodes = gqf.kg.nodes
		l = []
		for x in nodes:
			if(str(x) not in visited_queries):
				l.append(str(x))
		return l

	def get_links_query(self, query, f):
		results = bing_search(query, 10)
		for each_link in results:
			try:
				resp = requests.get(each_link['Url'])
				f.write(resp.url.encode('utf-8'))
				f.write("\n")
			except Exception, e:
				print("random error", e)
				continue
		return

	def handle(self, *args, **options): 
		# get query nodes
		queries = self.get_graph_nodes()
		
		f = open('seeds_generator/seeds_os.txt', 'a')
		
		for query in queries:
			self.get_links_query(query, f)

		f.close()

		self.dump_visited_queries(queries)
		return
                


import sys
import logging
import random

from comprehension_burden import *


logging.basicConfig(level=logging.DEBUG)

class GSS:

	def __init__(self):
		pass


	def generate_greedy_sequence(self, lesson_plan):

		comprehension_burden = CB(lesson_plan)

		url_to_content = lesson_plan.content
		number_of_documents = lesson_plan.number_of_docs
		all_docs = url_to_content.keys()

		doc_to_concepts, doc_to_keys, related_concepts = comprehension_burden_calculator.get_doc_to_keys(1)

		greedy_sequence = []

		while(len(greedy_sequence) < len(all_docs)):

			# calculate comprehension burden looking backwards
			# sequence the one that reduces the burden the least
			

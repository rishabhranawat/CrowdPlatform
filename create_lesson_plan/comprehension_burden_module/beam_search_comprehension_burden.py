import sys
import random
import logging

from comprehension_burden import *


logging.basicConfig(level=logging.INFO)


'''
Beam Search Sequencer - Explore graph based 
on a beam_width number of possibilities
at each time step choosing the document 
that increases the comprehension burden the least.
'''
class BSS:
	
	def __init__(self, beam_width):
		self.beam_width = beam_width

	def generate_beam_sequence(self, lesson_plan):
		comprehension_burden_calculator = CB(lesson_plan)

		url_to_content = lesson_plan.content
		number_of_documents = lesson_plan.number_of_docs

		doc_to_concepts, doc_to_keys, related_concepts = comprehension_burden_calculator.get_doc_to_key_concepts(3)
		concept_to_score = comprehension_burden_calculator.get_concept_to_global_score(related_concepts, doc_to_keys)

		beamed_sequence = []

		docs_tried = []
		min_marginal_cb = 0

		random_docs_to_try = set()
		keys = url_to_content.keys()

		while(len(random_docs_to_try) < self.beam_width):
			random_docs_to_try.add(keys[random.randint(0, number_of_documents-1)])

		intermediate_cb = 0.0
		for doc_to_try in random_docs_to_try:
			beamed_sequence.append(doc_to_try)

			intermediate_cb = comprehension_burden_calculator.lp_cb(beamed_sequence, doc_to_concepts, doc_to_keys)
			logging.info("Document: %s, with related keys: %s, has a comprehension burden of %d", 
				doc_to_try, doc_to_keys[doc_to_try], intermediate_cb)
			beamed_sequence.pop()


'''
Greedy Search Sequencer - Always pick the document
with the least delta. 
'''
class greedy_search_sequencer:

	def __init__(self):
		pass

	def generate_greedy_sequence(self, lesson_plan):
		comprehension_burden_calculator = CB(lesson_plan)


'''
Hypothesis here is that there is some notion of 
reinforcement that would help improve the quality of a lesson plan.
'''
class beam_search_sequencer_with_reinforcement:

	def __init__(self, beam_width):
		self.beam_width = beam_width
		pass

	def generate_beam_search_sequencer_with_reinforcement(self, lesson_plan):
		pass

def run_experiments_generate_report():
	pass

def runner():
	arguments = sys.argv[1:]


	filepath = arguments[0]
	sequencer_type = arguments[1]
	if(sequencer_type == 'bss'):
		beam_width = int(arguments[2])

	# TODO: clean up, so as to take generic arguments and not just
	# specific to beam search
	bss = BSS(beam_width)
	lesson_plan = LP(filepath)

	bss.generate_beam_sequence(lesson_plan)


if __name__ == "__main__":
	runner()




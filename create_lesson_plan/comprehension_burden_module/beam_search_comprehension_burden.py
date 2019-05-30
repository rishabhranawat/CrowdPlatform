import sys
import random
import logging

from comprehension_burden import *


logging.basicConfig(level=logging.DEBUG)


def write_to_file(filepath, sequence, cb):
	beamed_filepath = filepath.replace(".txt", "_beamed.txt")

	with open(beamed_filepath, "w") as beamed_file:
		for each_doc in sequence:
			beamed_file.write(each_doc+"\n")

		beamed_file.write("Sequence has a comprehension burden of: %d" % (cb))



'''
Beam Search Sequencer - Explore graph based 
on a beam_width number of possibilities
at each time step choosing the document 
that increases the comprehension burden the least.
'''
class BSS:
	
	def __init__(self, beam_width):
		self.beam_width = beam_width


	def generate_choices(self, docs):
		random_docs_to_try = set()
		number_of_docs_remaining = len(docs)

		potential_candidates = self.beam_width if(self.beam_width <= len(docs)) else len(docs)
		while(len(random_docs_to_try) < potential_candidates):
			random_docs_to_try.add(docs[random.randint(0, number_of_docs_remaining-1)])

		return random_docs_to_try

	def pretty_print_doc_concepts(self, doc, concepts):
		print("Url: " + doc)
		cs = ""
		for x in concepts:
			cs = cs +" ,"+x.label
		print("Concepts: " + cs)
		print("\n")

	def generate_beam_sequence(self, lesson_plan):
		comprehension_burden_calculator = CB(lesson_plan)

		url_to_content = lesson_plan.content
		number_of_documents = lesson_plan.number_of_docs
		all_docs = url_to_content.keys()

		doc_to_concepts, doc_to_keys, related_concepts = comprehension_burden_calculator.get_doc_to_key_concepts(3)
		for doc, concepts in doc_to_concepts.items():
			self.pretty_print_doc_concepts(doc, concepts)

		for doc, key_concepts in doc_to_keys.items():
			print("Url: " + doc)
			print("Concepts: ", key_concepts)
			print("\n")

		concept_to_score = comprehension_burden_calculator.get_concept_to_global_score(related_concepts, doc_to_keys)

		beamed_sequence = []
		cb = 0.0

		logging.debug("Number of Documents: %d", number_of_documents)
		while(len(beamed_sequence) < number_of_documents):
			
			doc_to_append = None
			intermediate_cb = None

			random_docs_to_try = self.generate_choices(all_docs)
			for doc_to_try in random_docs_to_try:
				
				# generate potential sequence
				beamed_sequence.append(doc_to_try)

				# compute comprehension burden for that particular option
				cb_current_seq = comprehension_burden_calculator.lp_cb(beamed_sequence, doc_to_concepts, doc_to_keys)
				logging.debug("Document: %s, with related keys: %s, has a comprehension burden of %d", 
					doc_to_try, doc_to_keys[doc_to_try], cb_current_seq)

				# pick the one that reduces the comprehension burden of the overall doc the least
				if(intermediate_cb == None or cb_current_seq + cb < intermediate_cb):
					intermediate_cb = cb_current_seq + cb
					doc_to_append = doc_to_try

				# revert it to the original sequence
				beamed_sequence.pop()

			# set sequence and corresponding cb
			logging.debug("Comprehension Burden: %d and number of documents in sequence: %d", cb, len(beamed_sequence))
			cb = intermediate_cb
			beamed_sequence.append(doc_to_append)

			# remove appended doc from chocies
			all_docs.remove(doc_to_append)

		for each in beamed_sequence:
			logging.debug(each)
		logging.debug("Comprehension Burden of the lesson plan: %d", cb)
		return beamed_sequence, cb


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

	sequence, cb = bss.generate_beam_sequence(lesson_plan)
	write_to_file(filepath, sequence, cb)


if __name__ == "__main__":
	runner()




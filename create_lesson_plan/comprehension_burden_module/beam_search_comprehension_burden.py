import sys
import random
import logging
import json
import time

from os import listdir
from os.path import isfile, join

from comprehension_burden import *


logging.basicConfig(level=logging.DEBUG)


format = ["Schedule for the lesson plan", "Summary of key-concept(s)","Explains key-concept(s)", "Applications of key-concept(s)","Related to key-concept(s)", "Other"]


def write_to_file(filepath, sequence, cb):
	beamed_filepath = filepath.replace(".txt", "_beamed.txt")

	beamed_filepath = filepath.replace(".json", "_beamed_json.txt")
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

def group_urls(docs):
	grouped = {}
	for d in docs:
		typ = d["content_type"]
		if(typ in grouped):
			grouped[typ].append(d["url"])
		else:
			grouped[typ] = [d["url"]]
	return grouped

def all_urls(docs):
	urls = []
	for each in docs:
		urls.append(each["url"])
	return urls

def get_burden_for_sequence(sequence):
	au = sequence
	lesson_plan_Td = LP(au)
	cb = CB(lesson_plan_Td)
	tdfsw = cb.get_cb_for_sequence_provided(2, sequence)
	return tdfsw


def runner_grouped():
	arguments = sys.argv[1:]

	bss = BSS(5)
	grouped_lesson_plans = []

	latest_files = ["lesson" + str(count) + ".json" for count in xrange(int(arguments[0]), int(arguments[1]))]
	onlyfiles = ["lps/crowd_sourced_data/"+f for f in listdir("lps/crowd_sourced_data") if f in latest_files]

	lesson_plans = []

	for eachfile in onlyfiles:
		with open(eachfile, 'r') as data:
			json_data = json.load(data)
			lesson_plans.append(json_data)

	burdens = []
	for each_lesson_plan_json_data in lesson_plans:
		
		# calculating topic DFS weighted
		# tdfsw_time = time.time()
		# au = all_urls(each_lesson_plan_json_data["docs"])
		# lesson_plan_Td = LP(au)
		# cb = CB(lesson_plan_Td)
		# tdfsw = cb.get_cb(2, "random", "random")
		# tdfsw_time = time.time() - tdfsw_time

		bss_sequence, bss_cb = bss.generate_beam_sequence(LP(all_urls(each_lesson_plan_json_data["docs"])))

		grouped_urls = group_urls(each_lesson_plan_json_data["docs"])

		# print("RANDOM GROUPED")
		# total_random = 0
		# for k, v in grouped_urls.items():
		# 	lesson_plan_a = LP(v)
		# 	cb = CB(lesson_plan_a)
		# 	total_random += cb.get_cb(2, "random", "random")

		# calculating beamed, crowd sourced
		print("BEAM")
		typ_to_sequence = {}
		total_comprehension_burden = 0
		for k, v in grouped_urls.items():
			lesson_plan = LP(v)
			sequence, cb = bss.generate_beam_sequence(lesson_plan)
			typ_to_sequence[k] = sequence
			total_comprehension_burden += cb
		
		final_sequence = []
		for each in format:
			if(each in typ_to_sequence):
				final_sequence.extend(typ_to_sequence[each])


		actual_burden = get_burden_for_sequence(final_sequence)


		# print("TDFSW GROUPED")
		# grouped_tdfs_time = time.time()
		# total_tdfs_weighted_grouped = 0
		# for k, v in grouped_urls.items():
		# 	lesson_plan_a = LP(v)
		# 	cb = CB(lesson_plan_a)
		# 	total_tdfs_weighted_grouped += cb.get_cb(2, "linearWeighted", "random")
		# grouped_tdfs_time = time.time() - grouped_tdfs_time

		# burdens.append(
			
		# 	# ['Random: ' + str(tdfsw/total_comprehension_burden) + 
		# 	[' Crowd Sourced Beam Search: ' + str(total_comprehension_burden/total_comprehension_burden) + 
		# 	' TDFS-Grouped: ' + str(total_tdfs_weighted_grouped/total_comprehension_burden) + 
		# 	' Random-Grouped: ' + str(total_random/total_comprehension_burden)
		# 	]
		
		# )
	
		print('BSS')
		for each in bss_sequence:
			print(each)

		print('Crowd BSS')
		for each in final_sequence:
			print(each)


		burdens.append(
			['BSS: ' + str(bss_cb/actual_burden), ' Crowd BSS: ' + str(actual_burden/actual_burden)]
		)

	for each in burdens:
		print(each)


	# final_sequence = []
	# for each in format:
	# 	if(each in typ_to_sequence):
	# 		final_sequence.append(each)
	# 		final_sequence.extend(typ_to_sequence[each])
	# 		final_sequence.append("\n")
	# write_to_file(filepath, final_sequence, total_comprehension_burden)


if __name__ == "__main__":
	runner_grouped()




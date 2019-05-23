import sys

from comprehension_burden import *

'''
Beam Search Sequencer - Explore graph based 
on a beam_width number of possibilities
at each time step choosing the document 
that increases the comprehension burden the least.
'''
class beam_search_sequencer:
	
	def __init__(self, beam_width):
		self.beam_width = beam_width
		pass

	def generate_beam_sequence(self, lesson_plan):
		comprehension_burden_calculator = CB(sample_lp)

'''
Greedy Search Sequencer - Always pick the document
with the least delta. 
'''
class greedy_search_sequencer:

	def __init__(self):
		pass

	def generate_greedy_sequence(self, lesson_plan):
		comprehension_burden_calculator = CB(sample_lp)


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
	print(arguments)

if __name__ == "__main__":
	runner()




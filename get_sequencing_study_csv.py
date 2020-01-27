from create_lesson_plan.models import *

import csv

def get_engage_links(lesson_plan):
	engage_objs = Engage_Urls.objects.filter(lesson_fk=lesson_plan)

	urls = []
	for engage_link in engage_objs:
		urls.append(engage_link.display_url)

	return urls

def construct_sequence_study_lp(lesson_plan):
	urls = get_engage_links(lesson_plan)

	print(lesson_plan.bullets_as_list())
	lesson_plan_key_concepts = ",".join(lesson_plan.bullets_as_list()).replace("\n", "").replace("\r", "")
	print(lesson_plan_key_concepts)
	lesson_title = lesson_plan.lesson_title

	rows_by_url = []
	for each in urls:
		rows_by_url.append([lesson_title, lesson_plan_key_concepts, each])
	return rows_by_url


def write_sequence_study_to_csv(lesson_plans):

	rows = []
	for lesson_plan in lesson_plans:
		row = construct_sequence_study_lp(lesson_plan)
		rows.extend(row)

	with open('sequence_study_input_data.csv', mode='w') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerows(rows)

def get_relevant_lesson_plans(course_title):
	
	l = lesson.objects.filter(course_name=course_title[0], 
		lesson_title=course_title[1])
	if(len(l) == 0):
		return
	else:
		return l[0]

def get_lps():
	course_title = [
		("Algorithms - User Study 2", "Graph Theory"),
		("Algorithms - User Study 2", "Greedy Algorithms"),
		("Machine Learning - User Study 2", "Clustering"),
		("User Study - Operating Systems 2", "Memory Management"),
		("User Study - Machine Learning", "Logistic Regression"),
		
		("User Study - Operating Systems", "Processes"),
		("User Study - Algorithms", "Sorting Algorithms"),
		("User Study - Machine Learning", "Supervised Learning"),
		("User Study - Operating Systems", "Scheduling algorithms"),
		("User Study - Algorithms", "Divide and Conquer")

	]
	lps = []
	for ct in course_title:
		lp = get_relevant_lesson_plans(ct)
		if(lp):
			lps.append(lp)
	print(lps)
	return lps

l = get_lps()
write_sequence_study_to_csv(l)
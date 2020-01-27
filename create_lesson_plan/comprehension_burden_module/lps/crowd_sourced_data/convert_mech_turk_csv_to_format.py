import csv
from collections import Counter
import json

LESSON_PLAN_TITLE = 27
URL = 29
CATEGORY = 30

categories = ["Schedule for the lesson plan", "Summary of key-concept(s)","Explains key-concept(s)", "Applications of key-concept(s)","Related to key-concept(s)", "Other"]

def group_urls_by_lesson_plan(rows):
	lp_to_rows = {}
	for row in rows:
		title = row[LESSON_PLAN_TITLE]

		if(title not in lp_to_rows):
			lp_to_rows[title] = []
		lp_to_rows[title].append(row)

	return lp_to_rows

def get_url_to_cateogry(lp_rows):

	url_to_category_map = {}

	for each in lp_rows:
		url = each[URL]
		category = each[CATEGORY]
		if(url not in url_to_category_map):
			url_to_category_map[url] = []

		url_to_category_map[url].append(category)

	url_to_category = {}

	for k, cc in url_to_category_map.items():

		highest_count = 0
		highest_category = ""
		for each in categories:
			c = cc.count(each)
			if(highest_count != 0 and highest_count == c):
				# break tie
				print(k, cc)
				highest_category = cc[int(raw_input())]
				print("choosing: ", highest_category)
				break

			elif(highest_count < c):
				highest_category = each
				highest_count = c
		url_to_category[k] = highest_category

	print(url_to_category)
	return url_to_category


def get_data(rows):
	lp_to_rows = group_urls_by_lesson_plan(rows)

	lp_data = []
	for k, v in lp_to_rows.items():
		url_to_category = get_url_to_cateogry(v)
		lp_data.append((k, url_to_category))

	return lp_data
	
def format(title, data):
	docs = []
	for url, category in data.items():
		docs.append({"url": url, "content_type" : category})
	return {"docs" : docs, "lesson_title": title}


with open("mech_data_csv.csv", "r") as f:
	reader = csv.reader(f)
	go = True
	rows = []
	for r in reader:
		rows.append(r)
	
	data = get_data(rows[1:])

count = 20
for lesson_plan, each_lp in data:
	with open("lesson"+str(count)+".json", "w") as d:
		json.dump(format(lesson_plan, each_lp), d)
	count += 1

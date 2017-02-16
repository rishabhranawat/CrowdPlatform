import sys
from py_ms_cognitive import PyMsCognitiveWebSearch

import json
 
def description_filters(bing_obj):
	if("wikipedia" in bing_obj.display_url):
		return bing_obj.snippet
	else:
		return None

def bing_search(query, collected, limit):
	API_KEY = '1e67699387e54366b30695c9bcd68b58'
	print("here!3")
	goal_urls = len(collected)+limit
	urls_collected = []
	iterations = 0
	while(len(collected) < goal_urls and iterations < 2):
		search_service = PyMsCognitiveWebSearch(API_KEY, query)
		bing_data = search_service.search(limit=limit, format='json')

		for bing_obj in bing_data:
			display_url = bing_obj.display_url
			if(display_url not in collected):
				collected[display_url] = description_filters(bing_obj)
				urls_collected.append(display_url)
		iterations += 1
	return (urls_collected, collected)
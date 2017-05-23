from py_ms_cognitive import PyMsCognitiveWebSearch

def bing_search(query, limit):
	all_links = []
	try:
		API_KEY ='8d06ebb959e54714bb2b5a8089704244'
		search_service = PyMsCognitiveWebSearch(API_KEY, 
			query, 
			custom_params='&mkt=en-US')
		response = search_service.search(
			limit=limit, 
			format='json')

		for link in response:
			details = link.json
			link_details = {
				'title': details['name'],
				'Url': details['url'],
				'Description': details['snippet'],
				'display_url': details['displayUrl']
			}
			all_links.append(link_details)
		return all_links
	except:
		print "Error when querying bing"
		return all_links
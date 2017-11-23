def run_topic_search(request, duplicate_dict, query_set, type1, input_title, input_grade):
    new_link_list = []
    es_links = get_index_results(input_title, query_set)

    valid_result, duplicate_dict, new_link_list = \
        generateDictAndLinksList(es_links, duplicate_dict, new_link_list)
   # type2_range = [6, 6]
   # for query in query_set:
   #     for type2 in range(1, type2_range[type1 - 1]):
   #         processed_query, limit = processed(query, type1, type2, \
   #             len(query_set), input_title, input_grade)
   #         query2 = query
   #         results = bing_search(processed_query, limit)
   #         valid_result, duplicate_dict, new_link_list = \
   #             generateDictAndLinksList(results, duplicate_dict, new_link_list)

    output = {'dups': duplicate_dict, 'links': new_link_list}
    print(output)
    return output

def get_index_results(input_title, lesson_outline):
    es = ElasticsearchOfflineDocuments()
    hits = es.generate_search_urls(input_title, lesson_outline)
    links = []
    # for hit in hits:
    #    if(hit.meta.score > 20):
    #        print(hit.attachment)
    #        link_dets = {'Url': hit.link, 'display_url': hit.link, 'Description': '',
    #        'title': hit.link}
    #        links.append(link_dets)
    # return links
    links = []
    for hit in hits:
        link_dets = {'Url':hit, 'display_url':hit, 'Description':'', 'title':hit}
        links.append(link_dets)
    return links



'''
DEPRECATE -- shifting to ES
'''
def processed_undergrad(query, type1, type2, bullets, input_title):
        # engage phase
    limit=2
    if type1 == 1:
        if type2 == 1:
            query += " "+input_title+" +site:wikipedia.org"
            if bullets == 3: limit = 2
            elif bullets == 2: limit = 2
            else: limit = 2

        elif type2 == 2:
            query += " "+input_title+" notes site:mit.edu "
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3

        elif type2 == 3:
            query += " "+input_title+" notes site:cmu.edu "
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3
            
        elif type2 == 4:
            query += " "+input_title+" notes site:stanford.edu "
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3

        elif type2 == 5:
            query += " "+input_title+" notes site:edu "
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3

        elif type2 == 6:
            query += " "+input_title+" applications examples"
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3
    
    # evaluate phase
    elif type1 == 2:
        if type2 == 1:
            query += " "+input_title+" homeworks site:mit.edu"
            if bullets == 3: limit = 1
            if bullets == 2: limit = 1
            else: limit = 4
        elif type2 == 2:
            query += " "+input_title+" homeworks site:cmu.edu"

            if bullets == 3: limit = 1
            if bullets == 2: limit = 1
            else: limit = 4

        elif type2 == 3:
            query += " "+input_title+" homeworks site:stanford.edu"
            if bullets == 3: limit = 1
            if bullets == 2: limit = 1
            else: limit = 4

        if type2 == 4:
            query += " "+input_title+" homeworks filetype:pdf"
            if bullets == 3: limit = 2
            if bullets == 2: limit = 3
            else: limit = 4

        elif type2 == 5:
            query += " "+input_title+" midterm+final+practice filetype:pdf"
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 1
            else: limit = 4

    return query, limit


'''
DEPRECATE -- shifting to ES
'''
def processed(query, type1, type2, bullets, input_title, input_grade):
    if input_grade == "Undergraduate":
        return processed_undergrad(query, type1, type2, bullets, input_title)


'''
DEPRECATE -- shifting to ES
'''
def getProcessedQuery(query, type1,unType):
    if(type1 == 1): query = query.replace("site:edu", universities[unType])
    elif(type1 == 2): query = query+(" "+universities[unType])
    return query
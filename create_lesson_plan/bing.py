# -*- coding: utf-8 -*-
import sys
import urllib
import urllib2
import json
import summsrch
 
def bing_search(query, search_type, limit, query_original):
    key= 'U2Tlenujx3Z8Y3nxPiTkfirOrhfXtrcUk2jMz3xgGXA'
    query = urllib.quote_plus(query,safe='+') # cleaning up the query
    print("bing "+query)
    # create credential for authentication
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    credentials = (':%s' % key).encode('base64')[:-1]
    auth = 'Basic %s' % credentials
    #url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=10&$format=json'
    
   
    url = 'https://api.datamarket.azure.com/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top='+str(limit)+'&$format=json'
    try:
      #proxy settings for IITD network
     #proxy = urllib2.ProxyHandler({'https': 'https://tt1140924:decode#thecode@proxy22.iitd.ernet.in:3128'})
     #opener = urllib2.build_opener(proxy)
     #--
     #urllib2.install_opener(opener)
     request = urllib2.Request(url)
     request.add_header('Authorization', auth)
     request.add_header('Options', 'DisableLocationDetection')
     request.add_header('User-Agent', user_agent)
     request_opener = urllib2.build_opener()
     #request_opener = urllib2.build_opener(proxy)
     response = request_opener.open(request) 
     response_data = response.read()
     json_result = json.loads(response_data)
     print(json_result)
     #summsrch.summ_search(query_original,json_result)
     result_list = []
     for result in json_result['d']['results']:
      if search_type == 'Web':
       result_list.append({'title': result['Title'], 'Url': result['Url'], 'Description': result['Description']})
      else:
       result_list.append({'title': result['Title'], 'Url': result['MediaUrl'], 'Description': "No description"})
     print 'Number of results fetched: %d' %len(result_list)
     #if len(result_list)>0:
        #if __name__ == '__main__':
      #summsrch.summ_search(query_original,json_result) 
     return result_list
    except urllib2.URLError, e:
     print "Error when querying the Bing API", e   

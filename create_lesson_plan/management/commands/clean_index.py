from django.core.management.base import BaseCommand

from elasticsearch import Elasticsearch
from create_lesson_plan.models import IndexDocument

class Command(BaseCommand):
	def get_body(self, pk):
		query_body ={
			  "query": {
				"bool": {
				  "must": [
					{"match": {
						"pk": pk
					}}
				  ]
				}
			  },
			  "_source": ["link", "pk"]
			}
		return query_body

	def handle(self, *args, **options):
		all_index = IndexDocument.objects.all()
		es = Elasticsearch()
                
                counter = 0
		for each in all_index.iterator():
			query_body = self.get_body(each.pk)
			results = es.search(index="offline_content", body=query_body)
			if(len(results["hits"]["hits"]) > 0):
                            res = results["hits"]["hits"][0]["_source"]
                            if(res["link"] != each.link): 
		                counter += 1
                print(counter)


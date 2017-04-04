from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

client = Elasticsearch()

s = Search(using=client, index="create_lesson_plan").query("match", content="community")
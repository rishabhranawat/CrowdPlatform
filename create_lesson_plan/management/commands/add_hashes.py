from django.core.management.base import BaseCommand

from create_lesson_plan.models import OfflineDocument, IndexDocument

import hashlib
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


class Command(BaseCommand):

    def __init__(self):
        self.client = Elasticsearch()
        #self.f = open("text_corpus/delete_es_docs.txt", "a")

    def delete_es_document(self, pk):
        # get doc by pk, and delete. Possibility of error but minor docs.
        #s = Search(using=self.client, index="offline_content")
        #sq = s.query("match", pk=pk)
        #res = sq.delete()
        self.f.write(""+str(pk)+"\n")

    def check_exists_delete_create(self, link, content_hash, pk):
        # Both the link and content have the be unique. If either exists, delete
        link_exists = IndexDocument.objects.filter(link = link)
        content_exists = IndexDocument.objects.filter(content_hash=content_hash)
        if(len(link_exists)>0  or len(content_exists)>0):
            self.delete_es_document(pk)
            return False
        else:
            i = IndexDocument.objects.create(link=link, content_hash=content_hash)
            i.save()
            return True

    def create_index_documents(self):
        # gets scroll
        page = self.client.search(index="offline_content", doc_type="offline_document",
                scroll="2m", size=50, body={})
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']
        tots = 50

        # loops untill all docs covered
        while(scroll_size > 0):
            hits = page['hits']['hits']
            for each_hit in hits:

                # source_data has the data that was ingested
                source_data = each_hit['_source']
                
                # content either the raw content or the attachment that was ingested
                content = source_data['content'].encode('utf-8')
                if('content' in source_data['attachment']):
                    content = source_data['attachment']['content'].encode('utf-8')
                
                # link, get sha256 hash --> create index document or delete this doc from es
                link = source_data['link']
                m = hashlib.sha256(content).hexdigest().encode('utf-8')
                self.check_exists_delete_create(link, m, source_data['pk'])
                
            # continue scrolling
            page = self.client.scroll(scroll_id = sid, scroll="2m")
            sid = page['_scroll_id']
            scroll_size = len(page['hits']['hits'])
            tots += 50
            print(sid, tots)
        self.f.close()

    def delete_duplicate_es_docs(self):
        f = open("text_corpus/delete_es_docs.txt", "r")
        l = f.readlines()

        nums = set([int(x.strip()) for x in l])
        
        for pk in nums:
            body = {"query":{"match":{"pk": pk}}}
            self.client.delete_by_query(index="offline_content", 
                    doc_type="offline_document", body=body, conflicts="proceed")
            print(pk)

    def handle(self, *args, **options):
        #self.create_index_documents()
        self.delete_duplicate_es_docs()

from django.core.management.base import BaseCommand

from create_lesson_plan.models import OfflineDocument, IndexDocument

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from scraper_utils import download_pdf_file, get_domain_from_url, get_file_type
from scraper_utils import EsIndexer, get_page_content_response

import requests
import time


class Command(BaseCommand):
    def __init__(self):
        self.es_indexer = EsIndexer()
        self.es = Elasticsearch()


    def check_if_doc_exists(self, d):
        if(IndexDocument.objects.filter(link=d.link) == 0): return False
        return True
    
    '''
    This is a one time thing where we are trying to migrate 
    from OfflineDocument to IndexDocument
    '''
    def get_offline_document_index(self):
        counter = -1
        docs = OfflineDocument.objects.all()
        while(counter < 29000):
            counter += 1
            print(counter)
            d = docs[counter]
            if(not self.check_if_doc_exists(d)):
                try:
                    response = requests.get(d.link)
                    if(response.status_code != 200): continue
                    else:
                        file_type = get_file_type(d.link, response)[1]
                        if("text/html" in file_type):
                            content = response.content
                            self.es_indexer_index_document(d.link, d.source, 
                                    d.subject, 'engage/evaluate', content, '','')
                        else:
                            file_name = link.split("/")[-1]
                            data = download_pdf_file(link, file_name, response)
                            self.es_indexer.index_document(d.link, d.source, 
                                    d.subject, 'engage/evaluate', '', '', data)
                except Exception as e:
                    print(e)
                    continue
            else:
                continue
    
    def check_if_in_es(self, doc):
      s = Search(using=self.es, index="offline_content")
      sq = s.query("match", pk=doc.pk)
      hits = sq.execute()
      print(len(hits), doc.pk)
      return (len(hits) > 0)

    def index_index_documents(self):
        docs = IndexDocument.objects.filter(pk=26070)
        es_indexer = EsIndexer()
        for doc in docs:
            if(not self.check_if_in_es(doc)):
                time.sleep(2)
                try:
                    link = doc.link
                    source = get_domain_from_url(link)
                    response = get_page_content_response(link)
                    if(response == None): continue
                    else:
                        file_type = get_file_type(doc.link, response)[1]
                        if("text/html" in file_type):
                            content = response.content
                            es_indexer.create_mapping_index(link, source, 'Computer Science',
                                    'engage/evaluate', content, '', '', doc.pk)
                        else:
                            file_name = link.split("/")[-1]
                            data = download_pdf_file(link, file_name, response)
                            es_indexer.create_mapping_index(link, source, 'Computer Science',
                                    'enggage/evaluate', '', '', data, doc.pk)
                except Exception as e:
                    print(e)
                    continue
            else:
                continue

    '''
    '''                
    def delete_extra_index_docs(self):
        pass

    def handle(self, *args, **options):
        #self.get_offline_document_index()
        self.index_index_documents()

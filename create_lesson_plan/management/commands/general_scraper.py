from multiprocessing import Pool
import requests
import time
import base64

from scraper_utils import get_page_content_response, download_pdf_file
from scraper_utils import download_files_load_es, create_offline_document_object, get_fro_links
from scraper_utils import get_domain_from_url, get_file_type, EsIndexer

class GeneralSeedScraper:
    
    def __init__(self):
        self.es_indexer = EsIndexer()
    
    def load_doc(self, link, response, source, subject, level):
        file_type = get_file_type(link, response)[1]
        try:
            if("text/html" in file_type):
                if(level == 2 or level == 1):
                    content = response.content
                    self.es_indexer.index_document(link, source, subject, 'engage/evaluate', content, '', '')
                return True
            else:
                file_name = link.split("/")[-1]
                data = download_pdf_file(link, file_name, response)
                r = self.es_indexer.index_document(link, source, subject, 'engage/evaluate', '', '', data)
        except Exception as e:
            print(e)
            return False

    def level_depth_b(self, links):
        for link in links:
            source = get_domain_from_url(link)
            response = get_page_content_response(link)
            if(response == None): continue
            else: self.load_doc(link, response, source, "Computer Science", 2)
            time.sleep(2)
        return

    def level_depth_a(self, link):
        source = get_domain_from_url(link)
        response = get_page_content_response(link)
        if(response == None): return []
        loaded = self.load_doc(link, response, source, "Computer Science", 1)
        if(loaded): 
            links = get_fro_links([], link, response)
            return links
        else: return []

    def run_scraper(self, link):
        links = self.level_depth_a(link)
        self.level_depth_b(links)
        return
        




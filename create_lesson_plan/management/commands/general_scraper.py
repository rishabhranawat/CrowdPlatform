from multiprocessing import Pool
import requests

from scraper_utils import get_page_content_response, download_pdf_file
from scraper_utils import download_files_load_es, create_offline_document_object, get_fro_links
from scraper_utils import get_domain_from_url, get_file_type

class GeneralSeedScraper:
    
    def __init__(self):
        pass

    def get_seed_links(self, file_name):
        f = open(file_name, 'r')
        lines = f.readlines()
        seed_links = [x.strip() for x in lines]
        f.close()
        return seed_links

    def load_doc(self, link, response, source, subject):
        file_type = get_file_type(link, response)[1]
        if("text/html" in file_type):
            print('html',link)
            create_offline_document_object(link, response.content, source, 
                subject)
            return
        else:
            print(file_type, link)
            file_name = link.split("/")[-1]
            f = download_pdf_file(link, file_name, response)
            create_offline_document_object(link, 'doc attached', source, 
                subject, f, file_name)
            return

    def level_depth_b(self, links):
        for link in links:
            source = get_domain_from_url(link)
            response = get_page_content_response(link)
            self.load_doc(link, response, source, "Computer Science")
        return

    def level_depth_a(self, link):
        source = get_domain_from_url(link)
        response = get_page_content_response(link)
        self.load_doc(link, response, source, "Computer Science")
        links = get_fro_links([], link, response)
        return links

    def run_scraper(self, link):
        links = self.level_depth_a(link)
        self.level_depth_b(links)
        return
        
    def initialize_scraper(self, file_name):
        seeds = self.get_seed_links(file_name)
        self.run_scraper(seeds[0])



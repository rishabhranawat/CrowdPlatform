from multiprocessing import Pool
import requests

from scraper_utils import get_page_content_response, download_pdf_file
from scraper_utils import download_files_load_es, create_offline_document_object, get_fro_links


class GeneralSeedScraper:
    
    def __init__(self):
        pass

    def get_seed_links(self, file_name):
        f = open(file_name, 'r')
        lines = f.readlines()
        seed_links = [x.strip() for x in lines]
        f.close()
        return seed_links
    
    def level_depth_a(self, link):
        download_files_load_es(link)
        fro_links = get_fro_links(None, link, get_page_content_response(link))

    def run_scraper(self, file_name):
        seeds = self.get_seed_links(file_name)

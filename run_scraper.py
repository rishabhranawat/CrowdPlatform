from scrapers.washu.scraper_utils import get_file_type, get_sha_encoding, get_fro_links
from scrapers.washu.scraper_washu_multi import get_all_content_urls
from create_lesson_plan.models import OfflineDocument


def download_files_load_es(all_course_pages, content_page_url):
	content_page_response = requests.get(content_page_url)
	content_page = content_page_response.content
	content_page_soup = BeautifulSoup(content_page, 'html.parser')
	
	file_type = get_file_type(content_page_url, content_page_response)
	
	# TO:DO -- Download
	if(file_type == "application/pdf"):
		return None
	else:
		return get_fro_links(all_course_pages, content_page_url)


def get_all_sub_level_1():
	content_page_urls, all_course_pages = get_fro_links()
	p = Pool(8)
	func = partial(download_files_load_es, content_page_urls)
	all_sub_level_1_links = list(p.map(func, all_course_pages[:1])) 
	ll = set()
	for each in all_sub_level_1_links:
		ll = ll | each
	for a in ll:
		print(a)

get_all_sub_level_1()

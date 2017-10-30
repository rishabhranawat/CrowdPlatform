from create_lesson_plan.search_elastic import ElasticsearchOfflineDocuments
import sys

e = ElasticsearchOfflineDocuments()
print(sys.argv[1], sys.argv[2])
urls = e.generate_search_urls(sys.argv[1], [sys.argv[2]])
for each in urls:
    print(each)

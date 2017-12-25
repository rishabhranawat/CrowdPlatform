from django.core.management.base import BaseCommand



import simhash
from create_lesson_plan.models import lesson, Engage_Urls, Evaluate_Urls
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):

        hashes = []

        # Number of blocks to use (more in the next section)
        blocks = 4
        # Number of bits that may differ in matching pairs
        distance = 3

        l = lesson.objects.get(course_name='Machine Learning 3', lesson_title='Mixture Models')

        eng_urls = Engage_Urls.objects.filter(lesson_fk=l)
        eva_urls = Evaluate_Urls.objects.filter(lesson_fk=l)

        for u in eng_urls:
            resp = requests.get(u.url)
            h = simhash.shingle(resp.content)
            print(h)
            hashes.append(simhash.compute(h))

        matches = simhash.find_all(hashes, blocks, distance)
        print(matches)

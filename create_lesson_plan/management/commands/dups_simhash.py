from django.core.management.base import BaseCommand

from create_lesson_plan.models import lesson, Engage_Urls, Evaluate_Urls
import requests
import time

class Command(BaseCommand):

    def get_shingles(self, f, size):
        shingles = set()
        buf = f
        for i in range(0, len(buf)-size+1):
            yield buf[i:i+size]

    def jaccard(self, set1, set2):
        x = len(set1.intersection(set2))
        y = len(set1.union(set2))

        return x/float(y)

    def handle(self, *args, **options):
        SHINGLE_SIZE = 5

        l = lesson.objects.get(course_name='Machine Learning 3', lesson_title='Mixture Models')

        eng_url = Engage_Urls.objects.filter(lesson_fk=l)[0]
        eva_url = Evaluate_Urls.objects.filter(lesson_fk=l)[0]

        eng_u = "https://en.wikipedia.org/wiki/Mixture_model"
        eva_u = "https://en.wikipedia.org/wiki/Mixture_models"


        f1 = requests.get(eng_u).content
        f2 = requests.get(eva_u).content

        start = time.time()
        shingles1 = set(self.get_shingles(f1, size=SHINGLE_SIZE))
        shingles2 = set(self.get_shingles(f2, size=SHINGLE_SIZE))
        print("shingles", time.time()-start)
        print(shingles1)
        print(type(shingles1))
        start = time.time()
        print(self.jaccard(shingles1, shingles2), eng_url.url, eva_url.url)
        print(time.time()-start)

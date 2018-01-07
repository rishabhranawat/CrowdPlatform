from django.core.management.base import BaseCommand

from create_lesson_plan.models import lesson, Engage_Urls, Evaluate_Urls
import requests

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

        eng_u = "https://www.edureka.co/blog/k-means-clustering-algorithm/"
        eva_u = "https://www.edureka.co/blog/k-means-clustering-algorithm/#SignUp"


        f1 = requests.get(eng_u).content
        f2 = requests.get(eva_u).content

        shingles1 = set(self.get_shingles(f1, size=SHINGLE_SIZE))
        shingles2 = set(self.get_shingles(f2, size=SHINGLE_SIZE))

        print(self.jaccard(shingles1, shingles2), eng_url.url, eva_url.url)

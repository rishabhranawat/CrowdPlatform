from django.core.management.base import BaseCommand

from create_lesson_plan.models import lesson

import requests

class Command(BaseCommand):

	HTTP = "http"
	hostname = "ec2-54-201-126-67.us-west-2.compute.amazonaws.com:8000/create_lesson_plan"
	endpoint = "user_lesson_plan/1"


	def handle(self, *args, **options):
		all_lesson_plans_staged = lesson.objects.filter(stage=1)[:1]

		for each_lesson_plan in all_lesson_plans_staged:
			url = "%s://%s/%s/%s" % (self.HTTP, self.hostname, str(375), self.endpoint)
			print(url)
			response = requests.get(url)

			if(response.status_code == 200):
				f = open("lesson_plans/lesson_plan_%s_%s.html"%
					(each_lesson_plan.course_name.replace(" ", "_"), each_lesson_plan.lesson_title.replace(" ", "_")), 
					"w")
				f.write(response.content)
				f.close()
			else:
				print("failed to download %s"%(each_lesson_plan.pk))
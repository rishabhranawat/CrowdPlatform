from elasticsearch.client import IndicesClient
from django.conf import settings
from django.core.management.base import BaseCommand
from create_lesson_plan.models import lesson

class Command(BaseCommand):
	def handle(self, *args, **options):
		self.recreate_index()

	def recreate_index(self):
		
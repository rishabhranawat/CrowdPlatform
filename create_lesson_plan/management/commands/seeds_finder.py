from django.core.management.base import BaseCommand

from create_lesson_plan.models import OfflineDocument
from create_lesson_plan.graph_query.query_formulator_poc import GraphQueryFormulator
from create_lesson_plan.pyms_cog import *

class Command(BaseCommand):
	def __init__(self):
		pass
	
	def handle(self, *args, **options):
		print('here!')

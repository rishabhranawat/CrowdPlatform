from django.db import models

from vote.managers import VotableManager
from vote.models import VoteModel

import django.db.models.options as options


options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
	'es_index_name', 'es_type_name', 'es_mapping'
)
# Create your models here.
class lesson(VoteModel, models.Model):
	user_name = models.CharField(max_length=400)
	subject = models.CharField(max_length=400)
	course_name = models.CharField(max_length=400)
	lesson_title = models.CharField(max_length=400)
	grade = models.CharField(max_length=100)
	bullets = models.CharField(max_length=1200)
	stage = models.IntegerField(default=0)
	score = models.IntegerField(default=0)

	class Meta:
		es_index_name = 'create_lesson_plan'
		es_type_name = 'lesson'
		es_mapping = {
			'properties': {
				'user_name' : {'type': 'string', 'index':'not_analyzed'},
			},
		}
	

class lesson_plan(models.Model):
	lesson_fk = models.ForeignKey(lesson)
	lesson_title = models.CharField(max_length=400)
	engage_url1 = models.CharField(max_length=600)
	engage_url2 = models.CharField(max_length=600)
	engage_img1 = models.CharField(max_length=600)
	engage_img2 = models.CharField(max_length=600)
	explain_url1 = models.CharField(max_length=600)
	explain_url2 = models.CharField(max_length=600)
	explain_url3 = models.CharField(max_length=600)
	explain_img1 = models.CharField(max_length=600)
	evaluate_url1 = models.CharField(max_length=600)
	evaluate_url2 = models.CharField(max_length=600)
	evaluate_url3 = models.CharField(max_length=600)
	evaluate_img1 = models.CharField(max_length=600)

class Engage_Urls(models.Model):
	title = models.CharField(max_length=600, blank=True)
	lesson_fk = models.ForeignKey(lesson)
	item_id = models.IntegerField()
	url = models.CharField(max_length=600)
	desc = models.CharField(max_length=600)

class Explain_Urls(models.Model):
	title = models.CharField(max_length=600, blank=True)
	lesson_fk = models.ForeignKey(lesson)
	item_id = models.IntegerField()
	url = models.CharField(max_length=600)
	desc = models.CharField(max_length=600)

class Evaluate_Urls(models.Model):
	title = models.CharField(max_length=600, blank=True)
	lesson_fk = models.ForeignKey(lesson)
	item_id = models.IntegerField()
	url = models.CharField(max_length=600)
	desc = models.CharField(max_length=600)

class Engage_Images(models.Model):
	lesson_fk = models.ForeignKey(lesson)
	url = models.CharField(max_length=600)

class Explain_Images(models.Model):
	lesson_fk = models.ForeignKey(lesson)
	url = models.CharField(max_length=600)

class Evaluate_Images(models.Model):
	lesson_fk = models.ForeignKey(lesson)
	url = models.CharField(max_length=600)

# Multiple Choice Questions
class MCQ(models.Model):
	course_name = models.CharField(max_length=400)
	lesson_title = models.CharField(max_length=400)
	grade = models.CharField(max_length=100)
	question = models.CharField(max_length=1600)
	optiona = models.CharField(max_length=600)
	optionb = models.CharField(max_length=600)
	optionc = models.CharField(max_length=600)
	optiond = models.CharField(max_length=600)
	correct_answer = models.CharField(max_length=2)

# Fill in the Blank Questions
class FITB(models.Model):
	course_name = models.CharField(max_length=400)
	lesson_title = models.CharField(max_length=400)
	grade = models.CharField(max_length=100)
	question = models.CharField(max_length=1600)
	answer = models.CharField(max_length=400)
	
class Document(models.Model):
	lesson_fk=models.ForeignKey(lesson)
	docfile=models.FileField(upload_to='documents')

class Image(models.Model):
	lesson_fk=models.ForeignKey(lesson)
	docfile=models.FileField(upload_to='images')

class OfflineDocument(models.Model):
	link = models.CharField(max_length=600)
	content = models.TextField()
	date_scraped = models.DateTimeField()
	source = models.TextField()

# class OfflineDocumentMapping(MappingType, Indexable):
# 	@classmethod
# 	def get_model(cls):
# 		return OfflineDocument
	
# 	@classmethod
# 	def get_mapping(cls):
# 		return {
# 			'properties': {
# 				'id': {'type':'integer'},
# 				'link' : {'type':'string', 'index': 'not_analyzed'},
# 				'content': {'type':'string', 'analyzer': 'snowball'},
# 				'date_scraped': {'type':'date', 'analyzer':'not_analyzed'},
# 				'source': {'type':'text', 'analyzer': 'not_analyzed'}
# 			}
# 		}
	
# 	@classmethod
# 	def extract_document(cls, obj_id, obj=None):
# 		if obj is None:
# 			obj = cls.get_model().objects.get(pk=obj_id)
# 		return {
# 			'id': obj.id,
# 			'link': obj.link,
# 			'content': obj.content,
# 			'date_scraped': obj.date_scraped,
# 			'source': obj.source
# 		}


	

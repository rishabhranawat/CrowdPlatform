from django.db import models
import django.db.models.options as options
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone

from vote.managers import VotableManager
from vote.models import VoteModel

from search import OfflineDocumentIndex as OfflineDoc



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
	url = models.TextField()
	display_url = models.TextField(default="blank")
	title = models.CharField(max_length=600, blank=True)
	lesson_fk = models.ForeignKey(lesson)
	item_id = models.IntegerField()
	url = models.CharField(max_length=600)
	desc = models.CharField(max_length=600)

class Explain_Urls(models.Model):
	url = models.TextField()
	display_url = models.TextField(default="blank")
	title = models.CharField(max_length=600, blank=True)
	lesson_fk = models.ForeignKey(lesson)
	item_id = models.IntegerField()
	desc = models.CharField(max_length=600)

class Evaluate_Urls(models.Model):
	url = models.TextField()
	display_url = models.TextField(default="blank")
	title = models.CharField(max_length=600, blank=True)
	lesson_fk = models.ForeignKey(lesson)
	item_id = models.IntegerField()
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
	lesson = models.ForeignKey(lesson, null=True)
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

class TestScore(models.Model):
	test_score = models.IntegerField(default=0, null=False, blank=False)
	lesson = models.ForeignKey(lesson)

##############################################
#		Offline Database Models 			 #
#		Todo - create mappings structure	 #
#		and then put to the index instead 	 #
#		instead of randomly putting it 		 #
##############################################
from elasticsearch.client import IndicesClient, IngestClient
from django.conf import settings
from elasticsearch import Elasticsearch
from datetime import datetime
import base64
import json
import uuid


class OfflineDocument(models.Model):
	PHASE_CHOICES = (
			('EN', 'Engage'),
			('EV', 'Evaluate'),
	)

	link = models.CharField(max_length=600, unique=True, default=uuid.uuid1)
	source = models.TextField()
	title = models.TextField(null=True, blank=True)

	content = models.TextField()

	subject = models.TextField(null=True, blank=True)
	phase = models.CharField(max_length=2, choices=PHASE_CHOICES)

	summary = models.TextField(null=True, blank=True)
	meta_tags = models.TextField(null=True, blank=True)

	date_scraped = models.DateTimeField(default=timezone.now, blank=True)
	attachment = models.FileField(blank=True, null=True,upload_to='documents')

	def indexing(self):
		obj = OfflineDoc(
				meta={'id':self.pk},
				link=self.link,
				source=self.source,
				title=self.title,
				subject=self.subject,
				phase=self.phase,
				pk=self.pk,
				content=self.content,
				summary=self.summary
			)
		obj.save()
		return obj.to_dict(include_meta=True)

# 	def to_search(self):
# 		es = Elasticsearch()
# 		if(self.attachment != None):
# 			data = base64.b64encode(self.attachment.file.read())
# 		else:
# 			data = ''
# 		body = {
# 			'link' : self.link,
# 			'source': self.source,
# 			'subject' : self.subject,
# 			'phase': self.phase,
# 			'pk': self.pk,
# 			'content': self.content,
# 			'summary': self.summary,
# 			'data': data
# 		}
# 		body = json.dumps(body)
# 		es.index(index='offline_content', 
# 			doc_type="offline_document", 
# 			pipeline="attachment",
# 			body=body)

# 	def to_delete():
# 		es = Elasticsearch()
# 		body = {
# 		  "query": { 
# 		    "match": {
# 		      "pk": 42
# 		    }
# 		  }
# 		}
# 		body = json.dumps(body)
# 		es.delete_by_query(index='offline_content', 
# 			doc_type='offline_document',
# 			body=body)
		
# def add_to_search(instance, **kwargs):
# 	instance.to_search()

# def remove_fro_search(instance, **kwargs):
# 	instance.to_delete()

# post_save.connect(add_to_search, sender=OfflineDocument)
# pre_delete.connect(remove_fro_search, sender=OfflineDocument)
	

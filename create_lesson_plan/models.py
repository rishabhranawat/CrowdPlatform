from django.db import models
import django.db.models.options as options
from django.db.models.signals import post_save, pre_delete

from vote.managers import VotableManager
from vote.models import VoteModel

from search import OfflineDocument as OfflineDoc



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

##############################################
#		Offline Database Models 			 #
#		Todo - create mappings structure	 #
#		and then put to the index instead 	 #
#		instead of randomly putting it 		 #
##############################################
from elasticsearch.client import IndicesClient
from django.conf import settings
from elasticsearch import Elasticsearch
from datetime import datetime


class OfflineDocument(models.Model):
	
    link = models.CharField(max_length=600)
    content = models.TextField()
    source = models.TextField()
    title = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    meta_tags = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    date_scraped = models.DateTimeField(default=datetime.now(), blank=True)

    class Meta:
		es_index_name = 'create_lesson_plan'
		es_type_name = 'offline_doc'
    
    def to_search(self):
    	es = Elasticsearch()
    	doc = {
    		'link':self.link,
    		'content':self.content
    	}
    	res = es.index(index=self._meta.es_index_name, \
    		doc_type=self._meta.es_type_name, id=self.id, body=doc)

def update_search(instance, **kwargs):
	instance.to_search()

post_save.connect(update_search, sender=OfflineDocument)
	

from django.db import models

from vote.managers import VotableManager
from vote.models import VoteModel
# Create your models here.
class lesson(VoteModel, models.Model):
	user_name = models.CharField(max_length=400)
	subject = models.CharField(max_length=400)
	course_name = models.CharField(max_length=400)
	lesson_title = models.CharField(max_length=400)
	grade = models.CharField(max_length=100)
	bullets = models.CharField(max_length=1200)
	stage = models.IntegerField(default=0)

	def indexing(self):
		obj = lessonIndex(
			meta = {'id': self.id},
			user_name = self.user_name,
			subject = self.subject,
			course_name = self.course_name,
			lesson_title = self.lesson_title,
			grade = self.grade,
			bullets = self.bullets,
			stage = self.stage
		)
		obj.save(index='lesson')
		return obj.to_dict(include_meta=True)


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

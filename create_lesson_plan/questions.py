import json
import string
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core import serializers
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core import serializers


from create_lesson_plan.models import lesson, lesson_plan, Engage_Urls, TestScore
from create_lesson_plan.models import Explain_Urls, Evaluate_Urls, MCQ
from create_lesson_plan.models import FITB, Engage_Images, Explain_Images
from create_lesson_plan.models import Evaluate_Images, Document, Image
from create_lesson_plan.forms import *

from create_lesson_plan.pyms_cog import bing_search 



class AddQuestions(View):
    def get(self, request, pk, *args, **kwargs):
    	questions = MCQ.objects.filter(lesson=lesson.objects.get(pk=pk))
    	l = lesson.objects.get(pk=pk)
    	f = AddMCQQuestions()
        return render(request, 'question_entry.html', {'lesson':l, 'form':f, 'questions':questions})

    def post(self, request, pk, *args, **kwargs):
    	if('submit' in request.POST):
    		option_a = request.POST['option_a']
    		option_b = request.POST['option_b']
    		option_c = request.POST['option_c']
    		option_d = request.POST['option_d']
    		answer = request.POST['answer']
    		question = request.POST['question']

    		mcq = MCQ(lesson=lesson.objects.get(pk=pk), question=question,correct_answer=answer,
    			optiona=option_a, optionb=option_b, optionc=option_c, optiond=option_d)
    		mcq.save()
    		return redirect('/create_lesson_plan/'+pk+'/add_questions/')

class AnswerQuestions(View):
	
	def get(self, request, pk, *args, **kwargs):
		l = lesson.objects.get(pk=pk)
		questions = MCQ.objects.filter(lesson=l)
		forms = []
		for each in questions:
			initial = {
				'question':each.question, 
				'question_pk':each.pk,
				'option_a':each.optiona,
				'option_b':each.optionb,
				'option_c':each.optionc,
				'option_d':each.optiond
				}
			forms.append(AnswerQuestionsForm(initial=initial))
		return render(request, 'answer_questions.html', {'forms':forms, 'lesson':l})

	def post(self, request, pk, *args, **kwargs):
		pks = request.POST['question_pk']
		answers = request.POST['answer']

		score = 0
		for i in range(0, len(pks), 1):
			q = MCQ.objects.get(pk=int(pks[i]))
			if(answers[i]==q.correct_answer): score += 1

		ts = TestScore(lesson=lesson.objects.get(pk=pk), test_score=score)
		ts.save()
		return redirect('/create_lesson_plan/'+pk+'/display_search_lesson_plan/')



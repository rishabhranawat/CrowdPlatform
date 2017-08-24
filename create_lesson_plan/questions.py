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


from create_lesson_plan.models import lesson, lesson_plan, Engage_Urls
from create_lesson_plan.models import Explain_Urls, Evaluate_Urls, MCQ
from create_lesson_plan.models import FITB, Engage_Images, Explain_Images
from create_lesson_plan.models import Evaluate_Images, Document, Image
from create_lesson_plan.forms import *

from create_lesson_plan.pyms_cog import bing_search 

class AddQuestions(View):
    def get(self, request, pk, *args, **kwargs):
    	print(pk)
        return render(request, 'question_entry.html', {})

    def post(self, request, pk, *args, **kwargs):
        return render(request, 'question_entry.html', {})


# =================================================
# FUNCTIONS FOR HANDLING QUESTIONS, NO LONGER USED
# =================================================


# def search_q_results(request):
#     if 'quest' in request.POST:
#         query = request.POST['quest']
#         # find mcq questions
#         m = MCQ.objects.filter(Q(lesson_title__icontains=query))
#         # find fill in the blank questions
#         f = FITB.objects.filter(Q(lesson_title__icontains=query))
#         return render(request, 'search_q_results.html', {'m': m, 'f': f, 'quest': query})
#     else:
#         return HttpResponse('query not found')


# def generate_qp_results(request):
#     if 'quest' in request.POST:
#         query = request.POST['quest']
#         # find mcq questions
#         m = MCQ.objects.filter(Q(course_name__icontains=query))
#         # find fill in the blank questions
#         f = FITB.objects.filter(Q(course_name__icontains=query))
#         return render(request, 'generate_qp_results.html', {'m': m, 'f': f, 'quest': query})
#     else:
#         return HttpResponse('query not found')

# # Search for questions


# def search_que(request):
#     return render(request, 'search_questions.html')


# def generate_q_paper(request):
#     return render(request, 'generate_q_paper.html')


# def submit_question(request):
#     return render(request, 'question_entry.html')


# def search_results(request):
#     if 'query' in request.POST:
#         query = request.POST['query']
#         l = lesson.objects.filter(Q(lesson_title__icontains=query))
#         en = Engage_Urls.objects.filter(lesson_fk=l[0])
#         ex = Explain_Urls.objects.filter(lesson_fk=l[0])
#         ev = Evaluate_Urls.objects.filter(lesson_fk=l[0])
#         doc = Document.objects.filter(lesson_fk=l[0])
#         pic = Image.objects.filter(lesson_fk=l[0])
#         return render(request, 'search_results.html', {'lesson_title': l[0].lesson_title, 'en': en, 'ex': ex, 'ev': ev, 'doc': doc, 'pic': pic})
#     else:
#         return HttpResponse('query not found')


# def show_temp_lesson_plan(request):
#     return render(request, 'index.html')
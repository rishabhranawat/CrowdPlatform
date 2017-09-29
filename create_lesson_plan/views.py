import json
import string
import time

from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Queue

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
from create_lesson_plan.search_elastic import ElasticsearchOfflineDocuments

from create_lesson_plan.pyms_cog import bing_search 

# list of subjects
subjects = ['Computer Science']
# list of education levels
grades = ['Undergraduate', 'Graduate']
# filters used in web search results
filters = ['blogspot', 'syllabus', 'curriculum', 'syllabi', 'catalog',\
            'course-outline', 'course structure', 'schedule', 'outline', \
            'course page', 'course description', 'basic information', \
            'course outcomes']
# list of type of uploads
types = ['Document', 'Image']
# list of universities
universities = ['ocw.mit:edu', 'stanford:edu', 'cmu:edu']

class Links(object):

    def __init__(self, url, display_url, desc, value, title):
        self.url = url
        self.desc = desc
        self.value = value
        self.title = title
        self.display_url = display_url

# determine if a search result is to be filtered, just based on its URL


def isToBeFiltered(url, description, title):
    for temp in filters:
        if temp in url.lower() or temp in description.lower()\
            or temp in title.lower():
            return True
    return False

# determine wether URL contains specific keywords


def contains(url, course_list, input_bullets, input_title, subject_list):
    for course_sub in course_list:
        if (course_sub in url.url) or (course_sub in url.desc):
            return True
    for bullet in input_bullets:
        if (bullet in url.url) or (bullet in url.desc):
            return True
    for subject in subject_list:
        if (subject in url.url) or (subject in url.desc):
            return True
    if (input_title in url.url) or (input_title in url.desc):
        return True
    return False

# ===============================================================================
# FUNCTIONS FOR TRANSLATING USER KEYWORDS INTO SEARCH QUERIES AND FETCHING RESULTS
# ================================================================================
# create search query based on type1 and type2
def processed_undergrad(query, type1, type2, bullets, input_title):
        # engage phase
    limit=2
    if type1 == 1:
        if type2 == 1:
            query += " "+input_title+" +site:wikipedia.org"
            if bullets == 3: limit = 2
            elif bullets == 2: limit = 2
            else: limit = 2

        elif type2 == 2:
            query += " "+input_title+" notes site:mit.edu "
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3

        elif type2 == 3:
            query += " "+input_title+" notes site:cmu.edu "
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3
            
        elif type2 == 4:
            query += " "+input_title+" notes site:stanford.edu "
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3

        elif type2 == 5:
            query += " "+input_title+" notes site:edu "
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3

        elif type2 == 6:
            query += " "+input_title+" applications examples"
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 2
            else: limit = 3
    
    # evaluate phase
    elif type1 == 2:
        if type2 == 1:
            query += " "+input_title+" homeworks site:mit.edu"
            if bullets == 3: limit = 1
            if bullets == 2: limit = 1
            else: limit = 4
        elif type2 == 2:
            query += " "+input_title+" homeworks site:cmu.edu"

            if bullets == 3: limit = 1
            if bullets == 2: limit = 1
            else: limit = 4

        elif type2 == 3:
            query += " "+input_title+" homeworks site:stanford.edu"
            if bullets == 3: limit = 1
            if bullets == 2: limit = 1
            else: limit = 4

        if type2 == 4:
            query += " "+input_title+" homeworks filetype:pdf"
            if bullets == 3: limit = 2
            if bullets == 2: limit = 3
            else: limit = 4

        elif type2 == 5:
            query += " "+input_title+" midterm+final+practice filetype:pdf"
            if bullets == 3: limit = 1
            elif bullets == 2: limit = 1
            else: limit = 4

    return query, limit


def processed(query, type1, type2, bullets, input_title, input_grade):
    if input_grade == "Undergraduate":
        return processed_undergrad(query, type1, type2, bullets, input_title)



def getProcessedQuery(query, type1,unType):
    if(type1 == 1): query = query.replace("site:edu", universities[unType])
    elif(type1 == 2): query = query+(" "+universities[unType])
    return query

def generateDictAndLinksList(results, duplicate_dict, new_link_list):
    valid_result = []
    print(results)
    for r in results:
        if r['Url'] not in duplicate_dict and \
            not isToBeFiltered(r['Url'], r['Description'], r['title']):
            valid_result.append(r)
        duplicate_dict[r['Url']] = 1

    if len(valid_result) == 0:
        return valid_result, duplicate_dict, new_link_list
    
    for each_result in valid_result:
        l = Links(each_result['Url'], each_result['display_url'], each_result['Description'], -1,
         each_result['title'])
        new_link_list.append(l)

    return valid_result, duplicate_dict, new_link_list

def get_index_results(input_title, lesson_outline):
    es = ElasticsearchOfflineDocuments()
    hits = es.generate_search_urls(input_title, lesson_outline)
    links = []
    for hit in hits:
        if(hit.meta.score > 20):
            print(hit.attachment)
            link_dets = {'Url': hit.link, 'display_url': hit.link, 'Description': '',
            'title': hit.link}
            links.append(link_dets)
    return links


def run_topic_search(duplicate_dict, query_set, type1, input_title, input_grade):
    
    new_link_list = []

    es_links = get_index_results(input_title, query_set)

    valid_result, duplicate_dict, new_link_list = \
        generateDictAndLinksList(es_links, duplicate_dict, new_link_list)
    type2_range = [6, 6]
    for query in query_set:
        for type2 in range(1, type2_range[type1 - 1]):
            processed_query, limit = processed(query, type1, type2, \
                len(query_set), input_title, input_grade)
            query2 = query
            results = bing_search(processed_query, limit)
            valid_result, duplicate_dict, new_link_list = \
                generateDictAndLinksList(results, duplicate_dict, new_link_list)

    output = {'dups': duplicate_dict, 'links': new_link_list}
    print(output)
    return output


def get_relevant_links(query, results, query_type, output):
    result_filtered = summsrch.summ_search(query, results, query_type)
    link_list = []
    for r in result_filtered:
        link = Links(r['Url'], each_result['display_url'],r['Description'], r['Value'], r['title'])
        link_list.append(link)
    output.put(link_list)

# use this to create a new lesson plan
def create_lesson_plan(request):
    dropdown_options = {'subjects': subjects, 'grades': grades}
    return render(request, 'form.html', dropdown_options)

# displays the lesson plan created based on web search results using user
# keywords

class GenerateLessonPlan(View):
    form = GenerateLessonPlanForm()

    def get(self, request, *args, **kwargs):
        return render(request, 'generate.html', {'form':self.form})

    def post(self, request, todo, *args, **kwargs):
        if(todo == '1'):
          if 'input_title' in request.POST:
            subject_name = request.POST['subject_name']
            course_name = request.POST['course_name']
            input_title = request.POST['input_title']
            input_grade = request.POST['input_grade']
            input_bullets = request.POST['lesson_outline']
            
            # Create new lesson object
            l = lesson(user_name=request.user.username, 
              subject=subject_name, 
              course_name=course_name, 
              lesson_title=input_title, 
              grade=input_grade, 
              bullets=input_bullets)
            l.save()
            
            # get course outline bullets, build query from each bullet
            input_bullets = input_bullets.lower()
            input_bullets = input_bullets.split('\n')
            query_set = []
            for bullet in input_bullets:
                bullet = bullet.strip()
                query_set.append(bullet)
            
            dups = {}
            outputs = run_topic_search(dups, query_set, 1, input_title, input_grade)
            
            engage_urls = []
            engage_urls_length = []
            dups = outputs['dups']
            item_id = 0
            for url in outputs['links']:
                e = Engage_Urls(lesson_fk=l, item_id=item_id, url=url.url,
                                desc=url.desc, title=url.title, display_url=url.display_url)
                e.save()
                engage_urls.append(e)
                item_id += 1
                print(url.url)
            
            # for evalaute phase, run query set (explain type1 = 3)
            outputs = run_topic_search(dups, query_set, 2, input_title, input_grade)
            evaluate_urls = []
            dups = outputs['dups']
            # print "evaluate %d"%len(outputs['links'])
            item_id = 0
            for url in outputs['links']:
                e = Evaluate_Urls(lesson_fk=l, item_id=item_id,
                                  url=url.url, desc=url.desc, title=url.title, display_url=url.display_url)
                e.save()
                evaluate_urls.append(e)
                item_id += 1
                print(url.url)
            lesson_pk = l.pk
            return redirect('/create_lesson_plan/'+str(lesson_pk)+'/user_lesson_plan/1')
          else:
              return HttpResponse('input_title not found')



# remove an item from the lesson plan
def remove_from_lp(request):
    if request.POST:
        l = lesson.objects.get(id=request.POST.get('lessonId'))
        itemId = request.POST.get('itemId')
        # URL or image
        itemType = request.POST.get('itemType')
        # the stage which the item belongs to
        itemGroup = request.POST.get('itemGroup')
        # if itemType == 'url':
        if itemGroup == "engage":
            e = Engage_Urls.objects.filter(
                lesson_fk=l, item_id=itemId).delete()
        elif itemGroup == "evaluate":
            e = Evaluate_Urls.objects.filter(
                lesson_fk=l, item_id=itemId).delete()
        elif itemGroup == "explain":
            e = Explain_Urls.objects.filter(
                lesson_fk=l, item_id=itemId).delete()
        return HttpResponse('Deleted')
    else:
        return HttpResponse('Expecting POST request.')



class upload_lesson_plan(FormView):

  def get(self, request, *args, **kwargs):
    form = UploadLessonPlanForm()
    return render(request, 'upload.html', {'form': form})

  def post(self, request, *args, **kwargs):
    if request.method == 'POST':
      subject_name = request.POST['subject_name']
      course_name = request.POST['course_name']
      title = request.POST['input_title'].lower().replace('+', ' ')
      grade = request.POST['input_grade']
      bullets = request.POST['lesson_outline']
      files = request.FILES.getlist('myfiles[]')
      print(files)

      l = lesson(user_name=request.user.username,
        subject=subject_name, course_name=course_name,
        lesson_title=title, grade=grade, bullets=bullets, stage=1)
      l.save()

      for f in files:
        d = Document(lesson_fk=l, docfile=f)
        d.save()

      return redirect('/create_lesson_plan/profile')


class user_profile(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        # user = User.objects.get(username=user)
        lesson_plans = list(lesson.objects.filter(user_name=user, stage=1).order_by('course_name'))
        print(user, lesson_plans)
        plans = []
        if(len(lesson_plans) > 0):
            c = lesson_plans[0].course_name
            cl = []

            for lp in lesson_plans:
                if(lp.course_name == c): 
                    cl.append(lp)
                else: 
                    plans.append(cl)
                    cl = []
                    c = lp.course_name
                    cl.append(lp)
            if(len(plans) == 0): plans.append(cl)
        print(plans)
        context = {
            'user':user, 
            'lesson_plans':plans}
        return render(request, 'profile.html', context)


class UserLessonPlan(View):
    def get_details(self, pk):
        l = lesson.objects.get(pk=pk)
        engage_urls = Engage_Urls.objects.filter(lesson_fk=l).order_by('item_id')
        evaluate_urls = Evaluate_Urls.objects.filter(lesson_fk=l).order_by('item_id')
        return l, engage_urls, evaluate_urls

   
    def get(self, request, pk, todo, *args, **kwargs):
        if(todo == '1'):
            l, engage_urls, evaluate_urls = self.get_details(pk)
            form = ManualLinkAddition()
            return render(request, 'user_lesson_plan.html', {'l':l, 
                'engage_urls':engage_urls, 'evaluate_urls':evaluate_urls, 'form':form})

    def post(self, request, pk, todo, *args, **kwargs):
        if(todo == '1'):
            return self.get(request, pk, todo)
        if(todo=='2'):
            return self.delete_link(request, pk)
        elif(todo=='3'):
            return self.reorder_links(request, pk)
        elif(todo == '4'):
            l = lesson.objects.get(pk = pk)
            l.stage = 1
            l.save()
            return HttpResponse("saved")
        elif(todo == '5'):
            return self.move_link_phase(request, pk)
        elif(todo == '6'):
            return self.save_new_link(request, pk)

    def move_link_phase(self, request, pk):
        link_id = request.POST['id']
        print(link_id)
        typ = request.POST['type']
        change_to = request.POST['change_to']
        l = lesson.objects.get(pk=int(request.POST['pk']))
        if(typ == 'engage'):
            i = Engage_Urls.objects.latest('item_id').item_id
            url = Engage_Urls.objects.get(pk=int(link_id))
            e = Evaluate_Urls(lesson_fk=l, item_id=i+1,
                                  url=url.url, desc=url.desc, title=url.title)
            e.save()
            url.delete()           
            return HttpResponse("place holder")
        elif(typ == 'evaluate'):
            i = Evaluate_Urls.objects.latest('item_id').item_id
            url = Evaluate_Urls.objects.get(pk=int(link_id))
            e = Engage_Urls(lesson_fk=l, item_id=i+1,
                                  url=url.url, desc=url.desc, title=url.title)
            e.save()  
            url.delete()         
            return HttpResponse("place holder")
        return HttpResponse("Error")


    def save_new_link(self, request, pk):
        print(request.POST)
        link = request.POST["fd[link]"]
        desc = request.POST["fd[link_desc]"]
        title = request.POST["fd[link_title]"]
        typ = request.POST["fd[link_type]"]
        l = lesson.objects.get(pk=pk)
        if(typ == 'Evaluate'):  
            i = Evaluate_Urls.objects.latest('item_id').item_id + 1
            e = Evaluate_Urls(lesson_fk=l, item_id=i,
                                  url=link, desc=desc, title=title)
            e.save()
        else:
            i = Engage_Urls.objects.latest('item_id').item_id + 1
            e = Engage_Urls(lesson_fk=l, item_id=i,
                                  url=link, desc=desc, title=title)
            e.save()
        return HttpResponse("Okay!")

    def delete_link(self, request, pk):
        l, engage_urls, evaluate_urls = self.get_details(pk)
        url_type = request.POST["type"]
        item_id = int(request.POST['id'])

        if(url_type=="engage"): 
            engage_urls = engage_urls.filter(item_id=item_id).delete()
        elif(url_type=="evaluate"):
            evaluate_urls = evaluate_urls.filter(item_id=item_id).delete()
        return HttpResponse("deleted")

    def get_link_with_item_id(self, urls, item_id):
        for each in urls:
            if(each.item_id == item_id):
                return each
        return None

    def get_next_lowest_id(self, urls, item_id):
        next_min = None
        for i in range(len(urls)-1, -1, -1):
            each = urls[i]
            if(each.item_id != item_id and each.item_id < item_id):
                return each
        return None

    def get_next_highest_id(self, urls, item_id):
        for each in urls:
            print(each.item_id, item_id)
        for i in range(0, len(urls), 1):
            each = urls[i]
            if(each.item_id != item_id and each.item_id > item_id):
                return each
        return None


    def reorder_links(self, request, pk):
        l, engage_urls, evaluate_urls = self.get_details(pk)
        url_type = request.POST["type"]
        item_id = int(request.POST['id'])
        up_down = request.POST["up_down"]

        if(url_type=="engage"):
            urls = engage_urls
        elif(url_type=="evaluate"):
            urls = evaluate_urls
        
        if(up_down == "up"):
            move_link_up = self.get_link_with_item_id(urls, item_id)
            move_link_down = self.get_next_lowest_id(urls, item_id)

            if(move_link_down != None):
                move_link_up.item_id=move_link_down.item_id
                move_link_up.save()

                move_link_down.item_id=item_id
                move_link_down.save()
                return HttpResponse("Okay")
            else:
                return HttpResponse("Okay at top")
        else:
            move_link_down = self.get_link_with_item_id(urls, item_id)
            move_link_up = self.get_next_highest_id(urls, item_id)

            if(move_link_up != None):
                move_link_down.item_id = move_link_up.item_id
                move_link_down.save()

                move_link_up.item_id = item_id
                move_link_up.save()

                return HttpResponse("Okay")
            else:
                return HttpResponse("At the Bottom anyway")

# Landing page for search lesson plan, i.e. the html page shown when user
# clicks on the "Search Lesson plan"


def search_lp(request):
    return render(request, 'search.html', {'subjects': subjects, 'grades': grades})

# save lesson plan


def save_lesson_plan(request):
    if 'input_title' in request.POST:
                # print 'yes'
                # print request.POST['input_title']
                #l = lesson()
                #l= request.POST['lesson']
                # l = lesson.objects.filter(Q(subject= subject,course_name__icontains=course, lesson_title__icontains=title, grade=input_grade))  #user_name==request.user.username and
                # receive search parameters
        subject_name = request.POST['subject']
        course_name = request.POST['course_name']
        input_title = request.POST['input_title']

        input_title = input_title.lower()
        input_title = string.replace(input_title, '+', ' ')
        # print input_title
        input_grade = request.POST['grade']
        input_bullets = request.POST['bullets']
        user_name = request.POST['user_name']
        # print user_name
        # print 'hello'
        # print request.user.username
        # exist = False
        # l_list = lesson.objects.filter(Q(user_name=request.user.username, subject=subject_name,
        #                                  course_name__icontains=course_name, 
        #                                  lesson_title__icontains=input_title, 
        #                                  grade=input_grade))
        #l_list_exist = lesson.objects.filter(Q(user_name = user_name, subject= subject_name,course_name__icontains=course_name, lesson_title__icontains=input_title, grade=input_grade))
    # Create new lesson object
        print(input_bullets)
        l = lesson(user_name=request.user.username, subject=subject_name, course_name=course_name,
                   lesson_title=input_title, grade=input_grade, bullets=input_bullets)
        l.save()

    # Lesson plan being saved already exists in database
        if len(l_list) > 0:
                    # print 'length = ',len(l_list)
            exist = True
            l = l_list[0]
            if user_name == request.user.username:
                # print "delete"
                e = Engage_Urls.objects.filter(lesson_fk=l)
                if len(e) > 0:
                    e.delete()
                e = Explain_Urls.objects.filter(lesson_fk=l)
                if len(e) > 0:
                    e.delete()
                e = Evaluate_Urls.objects.filter(lesson_fk=l)
                if len(e) > 0:
                    e.delete()
                e = Document.objects.filter(lesson_fk=l)
                if len(e) > 0:
                    e.delete()
                e = Image.objects.filter(lesson_fk=l)
                if len(e) > 0:
                    e.delete()
            # engage_urls_exist.extend(Engage_Urls.objects.filter(lesson_fk=l))
            # explain_urls_exist.extend(Explain_Urls.objects.filter(lesson_fk=l))
            # evaluate_urls_exist.extend(Evaluate_Urls.objects.filter(lesson_fk=l))
        else:
            # print 'length not > 0'
            #l = lesson(user_name = request.user.username, subject=subject_name,course_name = course_name, lesson_title = input_title, grade = input_grade, bullets = input_bullets)
            l.save()

    else:
        print 'input_title not found'
    engage_urls = []
    explain_urls = []
    evaluate_urls = []
    doc = []
    pic = []
    j = 0
    i = 0
    length = len(Engage_Urls.objects.filter(lesson_fk=l))
    # for i in range(0,10):
    try:
        while (True):

            item = "engageurl_" + str(i)
            # print item
            # print request.POST[item]
        # try:
            if request.POST[item] != "none":
                itemdesc = "engagedesc_" + str(i)
                itemtitle = "engagetitle_" + str(i)
                e1 = Engage_Urls(lesson_fk=l, item_id=j, url=request.POST[
                                 item], desc=request.POST[itemdesc], 
                                 title=request.POST[itemtitle])
                # print e1.url
                e_exist = Engage_Urls.objects.filter(
                    lesson_fk=l, url=request.POST[item])
                if len(e_exist) == 0:
                    #   print "Exist"
                    if user_name != request.user.username:
                        #length = len(Engage_Urls.objects.filter(lesson_fk=l))
                        e1.item_id = length
                #       print length
                    e1.save()
                    length = length + 1
                # e1.save()
                engage_urls.append(e1)
                j = j + 1
            i = i + 1
            #engage = Engage_Urls.objects.filter
    except Exception as e:
        random = "exceeded"

    j = 0
    i = 0
    length = len(Explain_Urls.objects.filter(lesson_fk=l))
    # for i in range(0,10):
    try:
        while(True):
            item = "explainurl_" + str(i)
        #   print item
        # try:
            if request.POST[item] != "none":
                itemdesc = "explaindesc_" + str(i)

                e1 = Explain_Urls(lesson_fk=l, item_id=j, url=request.POST[
                                  item], desc=request.POST[itemdesc])
        #       print e1.url
                explain_urls.append(e1)
                e_exist = Explain_Urls.objects.filter(
                    lesson_fk=l, url=request.POST[item])
                if len(e_exist) == 0:
                    #           print "Exist"
                    if user_name != request.user.username:
                        #length = len(Explain_Urls.objects.filter(lesson_fk=l))
                        e1.item_id = length
        #               print length
                    e1.save()
                    length = length + 1
                # e1.save()
        #       print len(explain_urls)
                j = j + 1
            i = i + 1
    except Exception as e:
        random = "exceeded"

    j = 0
    i = 0
    length = len(Evaluate_Urls.objects.filter(lesson_fk=l))
    # for i in range(0,10):
    try:
        while (True):
            # pass
            item = "evaluateurl_" + str(i)
        #   print item
        # try:
            if request.POST[item] != "none":
                itemdesc = "evaluatedesc_" + str(i)
                itemtitle = "evaluatetitle_" + str(i)
                e1 = Evaluate_Urls(lesson_fk=l, item_id=j, url=request.POST[
                                   item], desc=request.POST[itemdesc], 
                                   title=request.POST[itemtitle])
        #       print e1.url
                evaluate_urls.append(e1)
                e_exist = Evaluate_Urls.objects.filter(
                    lesson_fk=l, url=request.POST[item])
                if len(e_exist) == 0:
                    #           print "Exist"
                    if user_name != request.user.username:
                        #length = len(Engage_Urls.objects.filter(lesson_fk=l))
                        e1.item_id = length
        #               print length
                    e1.save()
                    length = length + 1
                # e1.save()
        #       print len(evaluate_urls)
                j = j + 1
            i = i + 1
    except Exception as e:
        random = "exceeded"
    # print len(evaluate_urls)
    j = 0
    i = 1
    length = len(Document.objects.filter(lesson_fk=l))
    # for i in range(1,10):
    try:
        while(True):
            # pass
            item = "document_" + str(i)
        #   print item
        # try:
            if request.POST[item] != "none":
                print "Hey %d" % i
                e1 = Document(lesson_fk=l, docfile=request.POST[item])
        #       print e1.docfile.name
                e_exist = Document.objects.filter(
                    lesson_fk=l, docfile=request.POST[item])
                if len(e_exist) == 0:
                    #           print "Exist"
                    # if user_name != request.user.username:
                        #length = len(Engage_Urls.objects.filter(lesson_fk=l))
                    #   e1.item_id= length
                    #               print length
                    e1.save()
                    #length = length+1
                # e1.save()
                doc.append(e1)
                j = j + 1
            i = i + 1
    except Exception as e:
        random = "exceeded"

    j = 0
    i = 1
    length = len(Image.objects.filter(lesson_fk=l))
    # for i in range(1,10):
    try:
        while(True):

            item = "Image_" + str(i)
        #   print item
        # try:
            if request.POST[item] != "none":
                #itemdesc = "evaluatedesc_" + str(i)
                e1 = Image(lesson_fk=l, docfile=request.POST[item])
        #       print e1.docfile.name
                e_exist = Image.objects.filter(
                    lesson_fk=l, docfile=request.POST[item])
                if len(e_exist) == 0:
                    # if user_name != request.user.username:
                        #length = len(Engage_Urls.objects.filter(lesson_fk=l))
                        #e1.item_id= length
                    #               print length
                    e1.save()
                    #length = length+1
                # e1.save()
                pic.append(e1)
                j = j + 1
            i = i + 1
    except Exception as e:
        random = "exceeded"
    
    return redirect('/create_lesson_plan/profile/')

class SearchLessonPlans(View):
    form = SearchResultsForm()

    def get(self, request, *args, **kwargs):
        return render(request, 'search.html', {'form':self.form})

    def post(self, request, *args, **kwargs):
        if(request.method == 'POST'):
            subject = request.POST['subject_name']
            course_name = request.POST['course_name']
            input_grade = request.POST['input_grade']
            input_title = request.POST['input_title']

            lessons = lesson.objects.filter(Q(subject = subject, 
                course_name__icontains=course_name,
                lesson_title__icontains=input_title,
                grade=input_grade, stage=1)).order_by('-score')
            
            return render(request, 'search_results_terse.html', 
                {'lessons':lessons})


class DisplaySearchLessonPlan(View):
    def get(self, request, pk, *args, **kwargs):
        l = lesson.objects.get(pk=pk)
        input_title = l.lesson_title
        engage_urls = Engage_Urls.objects.filter(lesson_fk=l)
        evaluate_urls = Evaluate_Urls.objects.filter(lesson_fk=l)

        documents = Document.objects.filter(lesson_fk=l)

        return render(request, 'display_search_lesson_plan.html', {'l':l, 
            'engage_urls':engage_urls, 'evaluate_urls':evaluate_urls,
             'documents':documents, 'count': l.votes.count()})
    def post(self, request, pk, *args, **kwargs):
      
        typ = request.POST['type']
        l = lesson.objects.get(pk=pk)\

        if(l.user_name == request.user.username):
            return HttpResponse("OKay!")

        if(typ == '1'):
            voted = l.votes.up(request.user.id)
            if(voted):
                l.score += 1
            l.save()
        else:
            voted = l.votes.down(request.user.id)
            if(voted):
                l.score -=1
            l.save()

        return HttpResponse("OKay!")
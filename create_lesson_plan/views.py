import json
import string
import time
import hashlib
import requests

from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Queue
from multiprocessing import Lock
from subprocess import Popen, PIPE

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
from django.core.cache import cache


from create_lesson_plan.models import lesson, lesson_plan, Engage_Urls
from create_lesson_plan.models import Explain_Urls, Evaluate_Urls, MCQ
from create_lesson_plan.models import FITB, Engage_Images, Explain_Images
from create_lesson_plan.models import Evaluate_Images, Document, Image
from create_lesson_plan.forms import *
from create_lesson_plan.search_elastic import ElasticsearchOfflineDocuments
from create_lesson_plan.pyms_cog import bing_search 
from create_lesson_plan.graph_query.query_formulator_poc import GraphQueryFormulator
from create_lesson_plan.es_search_module.es_search import SearchES

from simhash import fingerprint, simpair_indices
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

sent2Vec_process_key = 'sent2Vec_process'
sent2Vec_mutex_key = 'sent2Vec_mutex'
gqf_key = 'gqf'

collective_cache = {sent2Vec_process_key:None, sent2Vec_mutex_key:None,gqf_key:GraphQueryFormulator()}

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

'''
Quries es using the search_elastic module.
'''
def get_index_results(input_title, lesson_outline, phase):
    es = SearchES()
    hits = es.generate_search_urls(lesson_outline, phase)
    links = []
    for hit in hits:
        link_dets = {'Url':hit, 'display_url':hit, 'Description':'', 'title':hit}
        links.append(link_dets)
    return links



'''
Gets the closest node label and passes it to 
GQF which in turn returns related queries.
'''
def get_queries_knowledge_graph(query):
    gqf = collective_cache[gqf_key]
    query = query.replace("\n", "")
    if(not gqf.kg.has_node(query)):
        query_node = get_relevant_queries_sent2vec(query).replace("\n", "").strip()
    else:
        query_node = query
    queries = gqf.get_queries(query, query_node)
    return queries

'''
Runs Topic wise search.
Flow: input -> get closest node -> generate contextual queries graph -> es
'''
def run_topic_search(duplicate_dict, query_set, type1, input_title, input_grade):
    new_link_list = []
    
    for query in query_set:
        queries = get_queries_knowledge_graph(query)
        es_links = get_index_results(input_title, queries, type1)
        valid_result, duplicate_dict, new_link_list = \
            generateDictAndLinksList(es_links, duplicate_dict, new_link_list)
    output = {'dups': duplicate_dict, 'links': new_link_list}
    return output


# use this to create a new lesson plan
def create_lesson_plan(request):
    dropdown_options = {'subjects': subjects, 'grades': grades}
    return render(request, 'form.html', dropdown_options)

'''
Uses the running subprocess to stdin and read stdout.
TODO: Wrap start_subprocess_sent2vec and get_sent2vec_relevant_queries
into a sentnn module.
'''
def get_relevant_queries_sent2vec(query):
    process = collective_cache[sent2Vec_process_key]
    mutex = collective_cache[sent2Vec_mutex_key]
    query = query.title()
    with mutex:
        process.stdin.write(str(query)+"\n")
        time.sleep(0.5)
        l = []
        for i in range(0, 11, 1):
            dets = process.stdout.readline().split(" ")
            val = " ".join(dets[2:])
            if(len(val) > 1 and val != " "):
                l.append((float(dets[0]), val))
        if(l[0][0] > 0.7):
            return l[0][1]
        else:
            gqf = collective_cache[gqf_key]
            new_label = query.replace("\n", "").strip()
            closest_label = l[0][1].replace("\n", "").strip()
            gqf.add_to_kg(closest_label, new_label) 
            return query

'''
Starts a subprocess that runs the sent2Vec c++ implementation.
TODO: A gensim wrapper.
'''
def start_subprocess_sent2vec():
    if(collective_cache[sent2Vec_process_key] == None):
        c = "/home/ec2-user/collective_store_one/researchModels/sent2vec/fasttext nnSent /home/ec2-user/collective_store_one/researchModels/models/model_31k.bin seeds_generator/kg_nodes.txt"

        process = Popen(c.split(), stdin=PIPE, stdout=PIPE, universal_newlines=True)
        time.sleep(3)

        process.stdout.readline()

        collective_cache[sent2Vec_process_key] = process
        collective_cache[sent2Vec_mutex_key] = Lock()
        return True
    else:
        collective_cache[sent2Vec_process_key].kill()
        collective_cache[sent2Vec_process_key] = None
        return start_subprocess_sent2vec()

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_hash(content):
    h = hashlib.sha256()
    h.update(content)
    val_bytes = bytearray(h.digest())
    n = 0
    for byte in val_bytes:
         n = n<<8 | byte
    return n

def get_content(link): 
    return requests.get(link.display_url).content
'''
Responsible for generation of lesson plans -- integrates
the entire search engine cycle.

TODO: Need to clean up the garbage code from the ancient past.
'''
from create_lesson_plan.dups_detector import DuplicateDetector

class GenerateLessonPlan(View):
    form = GenerateLessonPlanForm()
    def __init__(self):		
        self.dups_detector = DuplicateDetector()   
 
    def remove_url_anchor(self, url):
        return url[:url.index('#')] if '#' in url else url
   
    def clean_wikipedia(self, link):
        wiki_stops = ["edit", "oldid", "action=info", "printable=yes",
                   "Special:", "action=" ]
        for each in wiki_stops:
            if each in link: return None
        return link

    def clean_anchors(self, links):
        l = set()
        f = []
        for link in links:
            if("wikipedia" in link.display_url):
                r = self.clean_wikipedia(link.display_url)
                if(r == None): continue
            
            clean_url = self.remove_url_anchor(link.display_url)
            if(clean_url not in l):
                link.display_url = clean_url
                link.url = clean_url
                link.title = clean_url
                l.add(clean_url)
                f.append(link)
        return f


    def detect_dups(self, links):
        start = time.time()
        content = []
        
        p = Pool(8)
        content = list(p.map(get_content, links))
        p.close()
        p.join()

        # for link in links:
        #     content.append(requests.get(link).content)

        dup_sets = []
        visited = set()
        for i in range(0, len(links), 1):
            per_dup_set = [links[i]]
            if(i in visited): continue
            visited.add(i)
            for j in range(0, len(links), 1):
                if(i == j or j in visited): continue
                if(self.dups_detector.detect(content[i], content[j]) > 0.7):
                    per_dup_set.append(links[j])
                    visited.add(j)
            dup_sets.append(per_dup_set)
        
        absolute_unique_links = set()
        for per in dup_sets:
            print([p.display_url for p in per])
            absolute_unique_links.add(per[0])
        print("time taken for duplicate", time.time()-start)
        return absolute_unique_links
        

    def get(self, request, *args, **kwargs):
        return render(request, 'generate.html', {'form':self.form})

    def post(self, request, todo, *args, **kwargs):
        if(collective_cache[sent2Vec_process_key] == None):
            start_subprocess_sent2vec()

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
            output_links_f = self.clean_anchors(outputs['links'])
            output_links = self.detect_dups(output_links_f)
            for url in output_links:
                e = Engage_Urls(lesson_fk=l, item_id=item_id, url=self.remove_url_anchor(url.url),
                                desc=url.desc, title=url.title, 
                                display_url=self.remove_url_anchor(url.display_url))
                e.save()
                engage_urls.append(e)
                item_id += 1
            
            outputs = run_topic_search(dups, query_set, 2, input_title, input_grade)
            evaluate_urls = []
            dups = outputs['dups']
            item_id = 0
            output_links = self.clean_anchors(outputs['links'])
            for url in output_links:
                e = Evaluate_Urls(lesson_fk=l, item_id=item_id,
                                  url=url.url, desc=url.desc, title=url.title, 
                                  display_url=url.display_url)
                e.save()
                evaluate_urls.append(e)
                item_id += 1
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
        plans = {}
        
        for each_lesson_plan in lesson_plans:
            lesson_plan_name = each_lesson_plan.course_name
            if(lesson_plan_name in plans):
                plans[lesson_plan_name].append(each_lesson_plan)
            else:
                plans[lesson_plan_name] = [each_lesson_plan]

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
        subject_name = request.POST['subject']
        course_name = request.POST['course_name']
        input_title = request.POST['input_title']

        input_title = input_title.lower()
        input_title = string.replace(input_title, '+', ' ')
        input_grade = request.POST['grade']
        input_bullets = request.POST['bullets']
        user_name = request.POST['user_name']
        # Create new lesson object
        l = lesson(user_name=request.user.username, subject=subject_name, course_name=course_name,
                   lesson_title=input_title, grade=input_grade, bullets=input_bullets)
        l.save()

    # Lesson plan being saved already exists in database
        if len(l_list) > 0:
            exist = True
            l = l_list[0]
            if user_name == request.user.username:
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
        else:
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

from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from create_lesson_plan.models import lesson, lesson_plan, Engage_Urls, Explain_Urls, Evaluate_Urls, MCQ, FITB, Engage_Images, Explain_Images, Evaluate_Images, Document, Image
from create_lesson_plan.forms import DocumentForm 
import bing
import summsrch
import json
import string
from django.db.models import Q
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Manager
from multiprocessing import Queue
#from operator import itemgetter
import summsrch

# list of subjects
subjects = ['Math', 'Computer Science']
# list of education levels
grades = [ 'High School', 'Undergraduate']
# filters used in web search results
filters = ['blogspot', 'syllabus', 'curriculum', 'syllabi', 'catalog']
#list of type of uploads
types=['Document', 'Image']

class Links(object):
	def __init__(self,url,desc,value):
		self.url = url
		self.desc = desc
		self.value = value

# determine if a search result is to be filtered, just based on its URL
def isToBeFiltered(url):
    if len(url) > 100:
        return True
    for temp in filters:
        if temp in url.lower():
            return True 
    return False

# determine wether URL contains specific keywords
def contains(url,course_list, input_bullets, input_title, subject_list):
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
def processed(query,type1,type2):
    # engage phase
    if type1 == 1:
        if type2 == 1:
            query+="+site:wikipedia.org"
            #print "Created query " + query
        elif type2 == 2:
            query+="+examples"
        elif type2 == 3:
            query+="+applications"
    
    # explain phase
    elif type1 == 2:
        if type2 == 1:
            query+=" filetype:ppt site:edu "
        elif type2 == 2:
            query+=" concepts filetype:pdf site:edu "
    
    # evaluate phase
    elif type1 == 3:
        if type2 == 1:
            query+="+homeworks+site:edu"
        elif type2 == 2:
            query+=" midterm+solutions site:edu"
    
    return query

# Input: a list of links already returned, a set of queries to be run
# ouput: a dictionary of {'Duplicates':dup[], 'Links':links[]}
def run_topic_search(duplicate_dict, query_set, type1):
    link_list = []

 # run the search once for each query in the set
 # for now the search queries are manually defined
 # type2 specifies what is appended to the main query before sending to bing
 # look at the function processed for the different values
    
    for query in query_set:
        query_results ={} 
        output_links = Queue()	
        for type2 in range(1,4):
            # process and run each query
            processed_query = processed(query, type1, type2)
            query2 = query
            query2 = query2.replace("+Math","")
            query2 = query2.replace("+Computer Science","")
            if type1 == 1:
              query2+="+Engage"
            elif type1 ==2:
              query2+="+Explain"
            elif type1 ==3:
              query2+="+Evaluate"

            results = bing.bing_search(processed_query, 'Web', query2)
            #print len(results)

            valid_result=[]
            for r in results:
            	if r['Url'] not in duplicate_dict and not isToBeFiltered(r['Url']):
            		valid_result.append(r)
            	duplicate_dict[r['Url']]=1	

            #print "number of links %d"%len(valid_result)
            if len(valid_result)==0:
              continue
            query_results[processed_query] = valid_result

        query_threads =[]   
        index =0 
        for key, value in query_results.iteritems():
            query_threads.append(Process(target= get_relevant_links,args=(key,value,index,output_links)))
            index+=1
            query_threads[-1].start()

        for i in range(len(query_threads)):
          query_threads[i].join()

        #print "Reached here"

        for i in range(len(query_threads)):
          link_list+=output_links.get()

        #print "Hey ya"

           # result_filtered = summsrch.summ_search(processed_query,valid_result)
            
            
            # for r in result_filtered:
            #     link = Links(r['Url'], r['Description'], r['Value'])
            #     link_list.append(link)
            #     count = count + 1

   	        
    #print "Number of final limks %d and type %d" %(type1,len(link_list))
    #new_link_list = sorted(link_list, key=lambda x: x.value, reverse=True)
    # ASHWIN: I removed reverse=True because I changed the scoring in summsearch.py so that lower
    # values of 'value' are better
    new_link_list = sorted(link_list, key=lambda x: x.value)
    if len(link_list) >= 10:
     count=10
    else:
     count = len(link_list)     
    # return the duplicates list and the list of link objects
    output = {'dups':duplicate_dict, 'links':new_link_list[0:count]}
    return output

def get_relevant_links(query,results,query_type,output):
  result_filtered = summsrch.summ_search(query,results,query_type)
  link_list =[]
  for r in result_filtered:
    link = Links(r['Url'], r['Description'], r['Value'])
    link_list.append(link)

  output.put(link_list)
  #print "Done"
  


# use this to create a new lesson plan
def create_lesson_plan(request):
    dropdown_options = {'subjects':subjects, 'grades':grades}
    return render(request, 'form.html', dropdown_options)

# use this to display a lesson plan
def display_lesson_plan(request, lesson_plan_id = ""):
    # get all the objects required to display complete lesson plan
    l = lesson.objects.get(id=lesson_plan_id)
    print "found lesson with id: %d" % l.id
    engage_urls = Engage_Urls.objects.filter(lesson_fk=l)
    #engage_img1 = Engage_Images.objects.filter(lesson_fk=l)
    explain_urls = Explain_Urls.objects.filter(lesson_fk=l)
    #explain_img1 = Explain_Images.objects.filter(lesson_fk=l)
    evaluate_urls = Evaluate_Urls.objects.filter(lesson_fk=l)
    #evaluate_img1 = Evaluate_Images.objects.filter(lesson_fk=l)
    doc=Document.objects.filter(lesson_fk=l)
    pic = Image.objects.filter(lesson_fk=l)
    # add to the context
    c = {}
    c['lesson_plan'] = l
    c['input_title'] = l.lesson_title
    c['engage_urls'] = engage_urls
    c['explain_urls'] = explain_urls
    c['evaluate_urls'] = evaluate_urls
    c['doc'] = doc
    c['pic'] = pic
    #if engage_img1:
     #   c['engage_img1'] = engage_img1[0]
    #if explain_img1:
     #   c['explain_img1'] = explain_img1[0]
    #if evaluate_img1:
     #   c['evaluate_img1'] = evaluate_img1[0]

    # render
    #if request.user.username == l.user_name:
    return render(request, 'index.html', c)
    #return render(request,'index_display_2.html',c)

# displays the lesson plan created based on web search results using user keywords
def show_lesson_plan(request):
  if 'input_title' in request.POST:
   # receive search parameters
   subject_name = request.POST['subject_name']
   course_name = request.POST['course_name']
   input_title = request.POST['input_title']
   input_grade = request.POST['input_grade']
   input_bullets = request.POST['input_bullets']
   #print subject_name
   #print course_name
   dups = {}
   img_dups = {}

   # Create new lesson object
   l = lesson(user_name = request.user.username, subject=subject_name,course_name = course_name, lesson_title = input_title, grade = input_grade, bullets = input_bullets)
   #l.save()

   # get course outline bullets, build query from each bullet
   input_bullets = input_bullets.lower()
   input_bullets = input_bullets.split('\n')
   query_set = []
   subject_name = string.replace(subject_name, ' ', '+')
   subject_name = subject_name.lower()
   subject_list = subject_name.split('+')
   course_name = string.replace(course_name,' ','+')
   course_name = course_name.lower()
   course_list = course_name.split('+')
   input_title = string.replace(input_title,' ','+')
   input_title = input_title.lower()
   input_list = input_title.split('+')
   #print course_name
   for bullet in input_bullets:
    bullet = bullet.strip()
    bullet = string.replace(bullet, ' ', '+')
    #query_set.append(bullet + "+" + input_title + "+" + course_name+"+"+subject_name)
    query_set.append(bullet + "+" + input_title)
    #query_set.append(bullet + "+" + course_name+"+"+subject_name)

   # for engage phase, run query set (engage type1 = 1)
   outputs = run_topic_search(dups, query_set, 1)
   # list of urls for the engage phase
   engage_urls = []
   engage_urls_length =[]
   dups = outputs['dups']
   #print "Number of Engage URLS fetched: %d" % len(engage_urls)
   #print "engage %d"%len(outputs['links'])
   i=0
   for url in outputs['links']:
   	#print url
    #if contains(url,course_list,input_bullets,input_title,subject_list):
    	e = Engage_Urls(lesson_fk = l,item_id=i, url = url.url, desc = url.desc)
    	#e.save()
    	#print e.url
    	engage_urls.append(e)
    	#engage_urls_length.append(i)
    	i = i+1

   # find an engage img, add it to the duplicate list
   #engage_img1 = ""
   #engage_img = bing.bing_search(query_set[0],'Image')
   #if engage_img:
    #engage_img1 = engage_img[0]['Url']
    #img_dups[engage_img1] = 1
   #else:
    #engage_img1 = ""
   #enga_img = Engage_Images(lesson_fk = l, url = engage_img1)
   #enga_img.save()

   # for explain phase, run query set (explain type1 = 2)
   outputs = run_topic_search(dups, query_set, 2)
   #print "Explain %d"%len(outputs['links'])
   # list of urls for the explain phase
   explain_urls = []
   explain_urls_length = []
   dups = outputs['dups']
   #print "explain %d"%len(outputs['links'])
   i=0
   for url in outputs['links']:
   	#print url
   	#if contains(url,course_list,input_bullets,input_title,subject_list):
   		e = Explain_Urls(lesson_fk = l,item_id=i, url = url.url, desc = url.desc)
   		#e.save()
   		explain_urls.append(e)
   		i=i+1

   # find an explain image
   #explain_img1 = ""
   #explain_img = bing.bing_search(query_set[0],'Image')
   #if explain_img:
    #for img in explain_img:
     #if img['Url'] not in img_dups:
      #explain_img1 = img['Url']
      #img_dups[explain_img1] = 1
      #break
   #else: 
    #explain_img1 = ""
   #expl_img = Explain_Images(lesson_fk = l, url = explain_img1)
   #expl_img.save()

   # for evalaute phase, run query set (explain type1 = 3)
   outputs = run_topic_search(dups, query_set, 3)
   #print "Evaluate %d"%len(outputs['links'])
   # list of urls for the evaluate phase
   evaluate_urls = []
   dups = outputs['dups']
   #print "evaluate %d"%len(outputs['links'])
   i=0
   for url in outputs['links']:
   	#print url
   	#if contains(url,course_list,input_bullets,input_title,subject_list):
   		e = Evaluate_Urls(lesson_fk = l,item_id=i, url = url.url, desc = url.desc)
   		#e.save()
   		evaluate_urls.append(e)
   		i=i+1

    # get an img for evaluate phase
   #evaluate_img1 = ""
   #evaluate_img = bing.bing_search(query_set[0],'Image')
   #if evaluate_img:
    #for img in explain_img:
     #if img['Url'] not in img_dups:
      #evaluate_img1 = img['Url']
      #img_dups[explain_img1] = 1
      #break
   #else:
    #evaluate_img1 = ""
   #eval_img = Evaluate_Images(lesson_fk = l, url = evaluate_img1)
   #eval_img.save()

   return render(request, 'index.html', {'lesson_plan':l, 'input_title' : input_title, 'engage_urls': engage_urls, 'explain_urls' : explain_urls, 'evaluate_urls' : evaluate_urls})
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
    #if itemType == 'url':
    if itemGroup == "engage":
      e = Engage_Urls.objects.filter(lesson_fk=l,item_id=itemId).delete()
    elif itemGroup == "evaluate":
      e = Evaluate_Urls.objects.filter(lesson_fk=l,item_id=itemId).delete()
    elif itemGroup == "explain":
      e = Explain_Urls.objects.filter(lesson_fk=l,item_id=itemId).delete()
    #elif itemType == 'img':
    #if itemGroup == 'engage':
     # e = Engage_Images.objects.get(item_id=itemId).delete()
    #elif itemGroup == 'evaluate':
     # e = Evaluate_Images.objects.get(item_id=itemId).delete()
    #elif itemGroup == 'explain':
     # e = Explain_Images.objects.get(item_id=itemId).delete()
    return HttpResponse('Deleted')
  else:
    return HttpResponse('Expecting POST request.')


# upload lesson plan
def upload(request):
  return render(request,'upload.html', {'subjects':subjects, 'grades':grades})

def upload_lp(request):
  if request.method=='POST':
   subject_name = request.POST['subject_name']
   course_name = request.POST['course_name']
   input_title = request.POST['input_title']
   input_title = input_title.lower()
   input_title = string.replace(input_title,'+',' ')
   input_grade = request.POST['input_grade']
   input_bullets = request.POST['input_bullets']
   l_list = lesson.objects.filter(Q(user_name = request.user.username,subject= subject_name,course_name__icontains=course_name, lesson_title__icontains=input_title, grade=input_grade))
   l = lesson(user_name = request.user.username, subject=subject_name,course_name = course_name, lesson_title = input_title, grade = input_grade, bullets = input_bullets)
   if len(l_list) > 0:
    l=l_list[0]
   else:
    #print 'length not > 0'
    l.save()
   return render(request,
        'list.html',
        {'types':types,'form': DocumentForm(),'lesson_plan':l, 'doc': Document.objects.filter(lesson_fk=l), 'pic': Image.objects.filter(lesson_fk=l)},
    )
  else:
   return HttpResponse('query not found')

def list(request):
    # Handle file upload
    docs =[]
    images =[]
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        subject_name = request.POST['subject']
        course_name = request.POST['course_name']
        input_title = request.POST['lesson_title']
        input_title = input_title.lower()
        input_title = string.replace(input_title,'+',' ')
        input_grade = request.POST['grade']
        input_bullets = request.POST['bullets']
        l_list = lesson.objects.filter(Q(subject= subject_name,course_name__icontains=course_name, lesson_title__icontains=input_title, grade=input_grade))
        #l = lesson(user_name = request.user.username, subject=subject_name,course_name = course_name, lesson_title = input_title, grade = input_grade, bullets = input_bullets)
        #l=lesson(user_name="",subject="",course_name="",lesson_title="",grade="",bullets="")
        #print l_list[0].subject
        if form.is_valid():
            #print request.POST['upload_type']
            if request.POST['upload_type']=='Document':
                newdoc = Document(lesson_fk=l_list[0], docfile = request.FILES['docfile'])
            else:
                newdoc = Image(lesson_fk=l_list[0], docfile=request.FILES['docfile'])

            newdoc.save()

            # Redirect to the document list after POST
            #return HttpResponseRedirect('/list/')
        docs = Document.objects.filter(lesson_fk=l_list[0])
        #print len(docs)
        images = Image.objects.filter(lesson_fk=l_list[0])

    else:
        form = DocumentForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render(request,
        'list.html',
        {'types':types,'form': form,'lesson_plan':l_list[0], 'doc': docs , 'pic': images},
    )

# Landing page for search lesson plan, i.e. the html page shown when user clicks on the "Search Lesson plan"
def search_lp(request):
	return render(request,'search.html', {'subjects':subjects, 'grades':grades})

#save lesson plan
def save_lesson_plan(request):
	if 'input_title' in request.POST:
		#print 'yes'
		#print request.POST['input_title']
		#l = lesson()
		#l= request.POST['lesson']
		#l = lesson.objects.filter(Q(subject= subject,course_name__icontains=course, lesson_title__icontains=title, grade=input_grade))  #user_name==request.user.username and  
		# receive search parameters
		subject_name = request.POST['subject']
		course_name = request.POST['course_name']
		input_title = request.POST['input_title']
		
		input_title = input_title.lower()
		input_title = string.replace(input_title,'+',' ')
		#print input_title
		input_grade = request.POST['grade']
		input_bullets = request.POST['bullets']
		user_name = request.POST['user_name']
		# print user_name
		# print 'hello'
		# print request.user.username
		exist = False
		l_list = lesson.objects.filter(Q(user_name = request.user.username, subject= subject_name,course_name__icontains=course_name, lesson_title__icontains=input_title, grade=input_grade))
		#l_list_exist = lesson.objects.filter(Q(user_name = user_name, subject= subject_name,course_name__icontains=course_name, lesson_title__icontains=input_title, grade=input_grade))
        # Create new lesson object
		l = lesson(user_name = request.user.username, subject=subject_name,course_name = course_name, lesson_title = input_title, grade = input_grade, bullets = input_bullets)
		
        # Lesson plan being saved already exists in database
		if len(l_list) > 0:
			#print 'length = ',len(l_list)
			exist=True
			l=l_list[0]
			if user_name == request.user.username:
				#print "delete"
				e = Engage_Urls.objects.filter(lesson_fk=l)
				if len(e)>0:
					e.delete()
				e = Explain_Urls.objects.filter(lesson_fk=l)
				if len(e)>0:
					e.delete()
				e = Evaluate_Urls.objects.filter(lesson_fk=l)
				if len(e)>0:
					e.delete()
				e = Document.objects.filter(lesson_fk=l)
				if len(e)>0:
					e.delete()
				e = Image.objects.filter(lesson_fk=l)
				if len(e)>0:
					e.delete()
      #engage_urls_exist.extend(Engage_Urls.objects.filter(lesson_fk=l))
      #explain_urls_exist.extend(Explain_Urls.objects.filter(lesson_fk=l))
      #evaluate_urls_exist.extend(Evaluate_Urls.objects.filter(lesson_fk=l))
		else:
			#print 'length not > 0'
			#l = lesson(user_name = request.user.username, subject=subject_name,course_name = course_name, lesson_title = input_title, grade = input_grade, bullets = input_bullets)
			l.save()
	 
	else:
		print 'input_title not found'
	engage_urls=[]
	explain_urls=[]
	evaluate_urls =[]
	doc= []
	pic = []
	j=0	
	i=0
	length = len(Engage_Urls.objects.filter(lesson_fk=l)) 
	#for i in range(0,10):
	try:
		while (True):
		
			item = "engageurl_" + str(i)
			#print item
			#print request.POST[item]
		#try:
			if request.POST[item] != "none":
				itemdesc = "engagedesc_" + str(i)
				e1 = Engage_Urls(lesson_fk = l,item_id=j, url = request.POST[item], desc = request.POST[itemdesc])
				#print e1.url
				e_exist = Engage_Urls.objects.filter(lesson_fk=l, url= request.POST[item])
				if len(e_exist)==0:
				#	print "Exist"
					if user_name != request.user.username:
						#length = len(Engage_Urls.objects.filter(lesson_fk=l)) 
						e1.item_id= length
				#		print length
					e1.save()
					length=length+1
				#e1.save()
				engage_urls.append(e1)
				j=j+1
			i=i+1
				#engage = Engage_Urls.objects.filter
	except Exception as e:
		random= "exceeded"

	j=0
	i=0
	length = len(Explain_Urls.objects.filter(lesson_fk=l))
	#for i in range(0,10):
	try:
		while(True):
			item = "explainurl_" + str(i)
		#	print item
		#try:
			if request.POST[item] != "none":
				itemdesc = "explaindesc_" + str(i)
				e1 = Explain_Urls(lesson_fk = l,item_id=j, url = request.POST[item], desc = request.POST[itemdesc])
		#		print e1.url
				explain_urls.append(e1)
				e_exist = Explain_Urls.objects.filter(lesson_fk=l, url= request.POST[item])
				if len(e_exist)==0:
		#			print "Exist"
					if user_name != request.user.username:
						#length = len(Explain_Urls.objects.filter(lesson_fk=l)) 
						e1.item_id= length
		#				print length
					e1.save()
					length=length+1
				#e1.save()
		#		print len(explain_urls)
				j=j+1
			i=i+1
	except Exception as e:
		random= "exceeded"

	j=0	
	i=0
	length= len(Evaluate_Urls.objects.filter(lesson_fk=l))
	#for i in range(0,10):
	try:
		while (True):
    #pass
			item = "evaluateurl_" + str(i)
		#	print item
		#try:
			if request.POST[item] != "none":
				itemdesc = "evaluatedesc_" + str(i)
				e1 = Evaluate_Urls(lesson_fk = l,item_id=j, url = request.POST[item], desc = request.POST[itemdesc])
		#		print e1.url
				evaluate_urls.append(e1)
				e_exist = Evaluate_Urls.objects.filter(lesson_fk=l, url= request.POST[item])
				if len(e_exist)==0:
		#			print "Exist"
					if user_name != request.user.username:
						#length = len(Engage_Urls.objects.filter(lesson_fk=l)) 
						e1.item_id= length
		#				print length
					e1.save()
					length = length+1
				#e1.save()
		#		print len(evaluate_urls)
				j=j+1
			i=i+1
	except Exception as e:
		random= "exceeded"
	#print len(evaluate_urls)
	j=0	
	i=1
	length = len(Document.objects.filter(lesson_fk=l))
	#for i in range(1,10):
	try:
		while(True):
			#pass
			item = "document_" + str(i)
		#	print item
		#try:
			if request.POST[item] != "none":
				print "Hey %d" %i
				e1 = Document(lesson_fk = l,docfile=request.POST[item])
		#		print e1.docfile.name
				e_exist = Document.objects.filter(lesson_fk=l, docfile= request.POST[item])
				if len(e_exist)==0:
		#			print "Exist"
					#if user_name != request.user.username:
						#length = len(Engage_Urls.objects.filter(lesson_fk=l)) 
					#	e1.item_id= length
		#				print length
					e1.save()
					#length = length+1
				#e1.save()
				doc.append(e1)
				j=j+1
			i=i+1
	except Exception as e:
		random = "exceeded"

	j=0
	i=1
	length = len(Image.objects.filter(lesson_fk=l))
	#for i in range(1,10):
	try:
		while(True):
		
			item = "Image_" + str(i)
		#	print item
		#try:
			if request.POST[item] != "none":
				#itemdesc = "evaluatedesc_" + str(i)
				e1 = Image(lesson_fk = l,docfile= request.POST[item])
		#		print e1.docfile.name
				e_exist = Image.objects.filter(lesson_fk=l, docfile= request.POST[item])
				if len(e_exist)==0:
					#if user_name != request.user.username:
						#length = len(Engage_Urls.objects.filter(lesson_fk=l)) 
						#e1.item_id= length
		#				print length
					e1.save()
					#length = length+1
				#e1.save()
				pic.append(e1)
				j=j+1
			i=i+1
	except Exception as e:
			random = "exceeded"		
	#save_new_lp(l,'engage',engage_urls,exist)
	#save_new_lp(l,'explain',explain_urls,exist)
	#save_new_lp(l,'evaluate',evaluate_urls,exist)
	#engage_urls = Engage_Urls.objects.filter(lesson_fk=l)
	#engage_img1 = Engage_Images.objects.filter(lesson_fk=l)
	#explain_urls = Explain_Urls.objects.filter(lesson_fk=l)
	#explain_img1 = Explain_Images.objects.filter(lesson_fk=l)
	#evaluate_urls = Evaluate_Urls.objects.filter(lesson_fk=l)
	#evaluate_img1 = Evaluate_Images.objects.filter(lesson_fk=l)
	#doc=Document.objects.filter(lesson_fk=l)
	#pic = Image.objects.filter(lesson_fk=l)
	#if 'engageurl_1' in request.POST:
	#	print request.POST['engageurl_1']
	return render(request, 'index.html', {'lesson_plan':l, 'input_title' : input_title, 'engage_urls': engage_urls, 'explain_urls' : explain_urls, 'evaluate_urls' : evaluate_urls,'doc':doc,'pic':pic})
	#return HttpResponse('engage_url1 found!!!')
	#else:
	#	return HttpResponse('engage_url1 not found')

#search existing lesson plans from the database based on user's request
def search_results_terse(request):
	if 'subject_name' in request.POST:
	 subject = request.POST['subject_name']
	 course=''
	 grade = ''
	 title = ''
	 if 'course' in request.POST:
	 	course = request.POST['course']
	 if 'grade' in request.POST:
	  grade = request.POST['grade']
	 if 'title' in request.POST:
	  title = request.POST['title']

	 l = []
	 if len(title) and grade and course and subject:
	  l = lesson.objects.filter(Q(subject= subject,course_name__icontains=course, lesson_title__icontains=title, grade=grade))
	 elif len(title) and course and subject:
	  l = lesson.objects.filter(Q(subject=subject,course_name__icontains=course, lesson_title__icontains=title))
	 elif grade and course and subject:
	  l = lesson.objects.filter(Q(subject=subject,course_name__icontains=course, grade=grade))
	 elif grade and len(title) and subject:
	 	l = lesson.objects.filter(Q(subject=subject,lesson_title__icontains=title, grade=grade))
	 elif grade and subject:
	 	l = lesson.objects.filter(Q(subject=subject, grade=grade))
	 elif len(title) and subject:
	 	l = l = lesson.objects.filter(Q(subject=subject, lesson_title__icontains=title))
	 elif course and subject:
	 	l = l = lesson.objects.filter(Q(subject=subject, course_name__icontains=course))
	 else:
	  l = lesson.objects.filter(Q(subject__icontains=subject))
	 return render(request,'search_results_terse.html', {'lessons': l})
	else:
	 return HttpResponse('Could not find any lesson plans, please enter the Subject Name')

# =================================================
# FUNCTIONS FOR HANDLING QUESTIONS, NO LONGER USED
# =================================================

def search_q_results(request):
	if 'quest' in request.POST:
		query = request.POST['quest']
		# find mcq questions
                m = MCQ.objects.filter(Q(lesson_title__icontains=query))
		# find fill in the blank questions
                f = FITB.objects.filter(Q(lesson_title__icontains=query))
		return render(request,'search_q_results.html',{'m': m, 'f': f, 'quest': query})
	else:
		return HttpResponse('query not found')

def generate_qp_results(request):
	if 'quest' in request.POST:
		query = request.POST['quest']
		# find mcq questions
		m = MCQ.objects.filter(Q(course_name__icontains=query))
		# find fill in the blank questions
		f = FITB.objects.filter(Q(course_name__icontains=query))
		return render(request,'generate_qp_results.html',{'m': m, 'f': f, 'quest': query})
	else:
		return HttpResponse('query not found')

# Search for questions
def search_que(request):
    return render(request,'search_questions.html')

def generate_q_paper(request):
    return render(request,'generate_q_paper.html')

def submit_question(request):
    return render(request,'question_entry.html')

#def submitted_question(request):
#    if 'lesson_title' in request.POST:
#        if request.POST['type'] == "mcq":
#            course_name = request.POST['course_name']
#            input_title = request.POST['lesson_title']
#            input_grade = request.POST['grade']
#                question = request.POST['question']
#                    optiona = request.POST['optA']
#                        optionb = request.POST['optB']
#                        optionc = request.POST['optC']
#                        optiond= request.POST['optD']
#                        correct_answer = request.POST['correct']
#                        q = MCQ(course_name = course_name, lesson_title = input_title, grade = input_grade, question = question, optiona = optiona, optionb = optionb, optionc = optionc, optiond = optiond, correct_answer = correct_answer)
#                        q.save()
#                        return render(request,'question_entry.html')
#                elif request.POST['type'] == "fitb":
#                    course_name = request.POST['course_name']
#                        lesson_title = request.POST['lesson_title']
#                        input_grade = request.POST['grade']
#                        if 'question1' in request.POST:
#                            question = request.POST['question1']
#                        else:
#                            print "question1 not in POST request"
#                        answer = request.POST['answer1']
#                        q = FITB(course_name = course_name, lesson_title = lesson_title, grade = input_grade, question = question, answer = answer)
#                        q.save()
#                    return render(request,'question_entry.html')
#        else:
#            HttpResponse('type not found')
#    else:
#        return HttpResponse('lesson_title not found')

# ==============================================================
# THESE FUNCTIONS ARE NOT BEING USED, CAN BE DELETED EVENTUALLY
# ==============================================================

#display uploaded search results
#def uploaded_search_results(request):
#  if 'query' in request.POST:
#   query = request.POST['query']
#   l = lesson.objects.filter(Q(lesson_title__icontains=query))
#   en = Engage_Urls.objects.filter(lesson_fk=l[0])
#   ex = Explain_Urls.objects.filter(lesson_fk=l[0])
#   ev = Evaluate_Urls.objects.filter(lesson_fk=l[0])
#   return render(request,'search_results.html',{'lesson_title': l[0].lesson_title, 'en': en, 'ex': ex, 'ev': ev})
#  else:
#   return HttpResponse('query not found')

#def save_new_lp(l,itemGroup,new_url_list,exist):
#    if exist:
#    #s_new = set(new_url_list)
#    #s = set(url_list)
#    #for x in url_list:
#    # if x not in s_new
#    #  remove_from_lp(l,itemGroup,x.item_id)
#    if itemGroup == 'engage':
#        e = Engage_Urls.objects.filter(lesson_fk=l).delete()
#    elif itemGroup == "evaluate":
#        e = Evaluate_Urls.objects.filter(lesson_fk=l).delete()
#    elif itemGroup == "explain":
#        e = Explain_Urls.objects.filter(lesson_fk=l).delete()
#        for x in new_url_list:
#        x.save()
#
#display searched lesson plan
def search_results(request):
    if 'query' in request.POST:
        query = request.POST['query']
        l = lesson.objects.filter(Q(lesson_title__icontains=query))
        en = Engage_Urls.objects.filter(lesson_fk=l[0])
        ex = Explain_Urls.objects.filter(lesson_fk=l[0])
        ev = Evaluate_Urls.objects.filter(lesson_fk=l[0])
        doc=Document.objects.filter(lesson_fk=l[0])
        pic = Image.objects.filter(lesson_fk=l[0])
        return render(request,'search_results.html',{'lesson_title': l[0].lesson_title, 'en': en, 'ex': ex, 'ev': ev,'doc':doc,'pic':pic})
    else:
        return HttpResponse('query not found')

def show_temp_lesson_plan(request):
    return render(request,'index.html')


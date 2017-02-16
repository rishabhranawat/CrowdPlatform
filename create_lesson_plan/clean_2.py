def show_lesson_plan(request):
  if 'input_title' in request.POST:
   # receive search parameters
   subject_name = request.POST['subject_name']
   course_name = request.POST['course_name']
   input_title = request.POST['input_title']
   input_grade = request.POST['input_grade']
   input_bullets = request.POST['input_bullets']

   dups = {}

   # Create new lesson object
   l = lesson(user_name = request.user.username, 
      subject=subject_name,
      course_name = course_name, 
      lesson_title = input_title, 
      grade = input_grade, 
      bullets = input_bullets)

   query_set = [input_grade+"+"+subject_name+"+"+course_name+"+"+\
   input_bullets.replace("\n", "+").replace(" ", "+")
   outputs = run_topic_search(dups, query_set, 1)
   
   dups = outputs['dups']
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

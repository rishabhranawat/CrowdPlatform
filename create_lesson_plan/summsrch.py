#!/usr/bin/python

import cgi
import urllib
import urllib2 
from urllib2 import Request
import simplejson
import json
import sys
import cPickle as cp
import os.path as pt
import numpy as np
from scipy import stats
import nltk
from googleapiclient.discovery import build
import lxml
from lxml import html
from gensim import corpora,models
#from nltk.corpus import stopwords as sw
import stop_words as sw
import re
import itertools
import math
from multiprocessing import Pool
from multiprocessing import Process
import time
from multiprocessing import Manager

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter # , XMLConverter, HTMLConverter
import wikipedia

#print "Content-Type: text/html; image/jpeg"

#stops = sw.getStopWords()
stops = sw.get_stop_words('en')
alpha = re.compile('[A-Za-z0-9]')
extras = ["forgot","email","edit","login"]
#print stops
#dict = corpora.Dictionary.load('dictionary')
avg = [[] for x in range(3)]
var = [[] for x in range(3)]
page_p = [[] for x in range(3)]
#qry = ''
form = cgi.FieldStorage()

#if form.has_key( "q" ):
 #   qry = form['q'].value.strip()

qry = 'sample space definition probability math'
#wr = open('logs/qry.txt','a')
#wr.write(str(dt.datetime.now())+'\t'+qry+'\n')
#wr.close()

manager = Manager()

resultpages = [manager.dict({}) for x in range(3)]

def accept(x):
    if x in stops:
        return  False
    if x.lower() in extras:
        return False
    if len(x) <= 2 and x.isalpha():
        return False
    if len(alpha.findall(x)) != len(x):
        return False

    return True

#extract text from a url
def extractParagraphsFromWebpages(url):
  p=[]
  #print url
  if "en.wikipedia.org/wiki/" in url:
    return parsewiki(url)
  elif ".pdf" in url:
    return parsePDF(url)
  #p=[]
  for i in range(1,6):
    para= extractText(url,i)
    if len(para)>0:
      p+=para

  return p
  #return parseHtml(url)

def clean_html(html):
    
    #print "Hey clean"
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    #print "Bye clean"
    return cleaned.strip()   

def parseHtml(url):
  try:
    #print "html"
    html =  urllib2.urlopen(Request(url)).read()
    cleanhtml = clean_html(html)
    #print "cleanhtml"
    return cleanhtml.encode("utf-8").replace("\r\n","\n").split("\n\n")

  except Exception:
    #print "cleanhtml exception"
    return []

def extractText(url,n):
    #print "No Error"
  try: 
    path='//'
    if n==1:
      path+='div/text()'
    elif n==2:
      path+='p/text()'
    elif n==3:
      path+='td/text()'
    elif n==4:
      path+='span/text()'
    elif n==5:
      path+='a/text()'

    p = lxml.html.parse(url).xpath(path)
    #print "Para"
    return p
  except Exception:
    #print "Exception Error"
    return []

#define a wikipedia page parser function
def parsewiki(url):
  
  try:
    #print "Hello"
    url= url.split("/")[-1]
    #print "URL %s"%url
    url = url.replace("_"," ")
    # regex = re.compile('[^a-zA-Z ]')
    # url = regex.sub("",url)
    #print url
    x = wikipedia.page(url).content.split("\n\n")
    return x
    
  except Exception:
    #print "Exception wiki"
    return []

#define a pdf parser function
def parsePDF(url):
  #url= "http://math.buffalostate.edu/%7Eit/projects/Gallagher.pdf"
  # Open the url provided as an argument to the function and read the content
  try:
    #print "pdf"
    f = urllib2.urlopen(Request(url)).read()
    #print "read"
    # Cast to StringIO object
    from StringIO import StringIO
    memory_file = StringIO(f)
    # Create a PDF parser object associated with the StringIO object
    parser = PDFParser(memory_file)

        # Create a PDF document object that stores the document structure
    document = PDFDocument(parser)
    #print "parser"

        # Define parameters to the PDF device objet 
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    codec = 'utf-8'

        # Create a PDF device object
    device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
    #print "laparams"

        # Create a PDF interpreter object
    interpreter = PDFPageInterpreter(rsrcmgr, device)

        # Process each page contained in the document
    for page in PDFPage.create_pages(document):
      interpreter.process_page(page)
      #data =  retstr.getvalue()
    #print "done"
    #print data.encode(utf-8).split("\n\n")
    #return retstr.getvalue().encode("utf-8").split("\n\n")
    return retstr.getvalue().split("\n\n")
  except Exception:
    return []

#downloads all the pages
def pages(results,index):
  docs = []
  titles = []
  urls = []
  
  threads = []
  sq=0
  #print "Hello World"
  print "number of links summ_search %d"%len(results)
  for r in results:
    threads.append(Process(target=download,args=(r,sq,index)))
    #print "Hello 1"
    threads[-1].start()
    #print "Hello 2"
    sq+=1
    
  for i in range(len(threads)):
      threads[i].join()

  
  return docs,titles,urls


def download(r,seqno,i):
    #print "download %d"%seqno
    try:
        global resultpages

        # print "World 1"
        # print r['Url']
        paragraphs = extractParagraphsFromWebpages(r['Url'])
        #print r['Url']
        if paragraphs==None or len(paragraphs)==0:
          paragraphs = [r['Description'].encode("utf-8","ignore")]

        docs = [k.strip() for k in paragraphs if len(k.split())>2]
        #if len(docs)==0:
        titles =  r['title']
        urls = r['Url']
        #temp = (docs,titles,urls,seqno)
        temp = (docs,r,seqno)
        resultpages[i][seqno] = temp
    except AttributeError:
      errmssg= 'couldn\'t load'+ r['Url']
      print errmssg
      


def textconv(docs): ## converts docs (list of paras) into  a  combined list of paras
  paragraphs = []

  for paras in docs:
    for para in paras:
      temp = [w for w in para if  accept(w)]
      #print temp
      paragraphs.append(temp)

  
  return paragraphs

def d2v(query, paras): ##extract new features and computes the text model
    paras = textconv(paras)
    kws = [q.lower() for q in query.split() if accept(q.lower())]
    #print "Query"
    #print kws
    paras_kws = []
    for k in paras: ### addding the query terms in the model to avoid crashing due to unimportant word in the query
      paras_kws.append(k)
    paras_kws.append(kws)
    #print "Vocabulary"
    #print paras_kws
    model = models.Word2Vec(paras_kws, size=100, window=8, min_count=0, workers=4)
    kws = list(set(similar_terms(model,paras,kws)))
  
    return model,kws



def similar_terms(model,text,kws):
  #return [k for k,v in model.most_similar(kws)]
  merged = list(itertools.chain(*text))
  #kws += [w[0] for w in nltk.FreqDist(merged).most_common(10)]
  return kws

# calculate similarity score of each page
def getRelevantParas(model,kws,paras,index):
  rel_paras = []
  global avg, var, page_p
  for i,para in enumerate(paras):
    #print para
    temp = [w for w in para if accept(w)]
    if len(temp) == 0:
      continue
    try:
        #print "Try catch"
        simil_score = model.n_similarity(kws,temp)
        if not np.isnan(simil_score):
          rel_paras.append(simil_score)
          
    except:
      continue
  if len(rel_paras) == 0:
    return np.inf
  page_avg = np.average(rel_paras)
  if page_avg == 0:
    return np.inf
  
  # ASHWIN: I changed the formula here..
  page_sem = stats.sem(rel_paras, nan_policy='omit')
  #page_var = np.var(rel_paras)
  avg[index].append(page_avg)
  var[index].append(page_sem)
  ## similarity score of the page calaculated from average and variance of all the paragraphs
  #p = abs(page_avg-10*page_var)
  p = page_sem/page_avg
  page_p[index].append(p)
  # print "Average %f"%page_avg
  # print "Variance %f"%page_var
  # print "Prob %f"%p
  #print len(avg)
  return p

# Define a PDF parser function

def summ_search(qry,results,index):
    global resultpages
    resultpages[index].clear()
    global avg, var, page_p
    avg[index] =[]
    var[index] = []
    page_p[index] =[]

    #print "Search"
    #print qry
    qry = qry.replace("+"," ")

    rawdocs,titles,urls = pages(results,index)
    #print "Result Pages %d"%len(resultpages)
    #mid = dt.datetime.now()
    rawdocs =[]
    titles=[]
    urls=[]
    result_sorted = []
    for iter in sorted(resultpages[index].keys()):
      rawdocs.append(resultpages[index][iter][0])
      #titles.append(resultpages[iter][1])
      result_sorted.append(resultpages[index][iter][1])
    
    docs = []
    for paragraphs in rawdocs:
        #print "Para %d"%len(paragraphs)
        docs.append([nltk.wordpunct_tokenize(para.lower()) for para in paragraphs if len(para.split())>2])
  
    model,kws = d2v(qry,docs)
    result_list =[]
    for i,doc in enumerate(docs):
        #print urls[i]
        print result_sorted[i]['Url']
        p = getRelevantParas(model,kws,doc,index)
        result_list.append({'title': result_sorted[i]['title'], 'Url': result_sorted[i]['Url'], 'Description': result_sorted[i]['Description'], 'Value': p})
        #print p
        #similscores+=p
    #print "Constant c"
    #print len(avg)
    #comparator = (0.5*np.percentile(avg,90)+0.5*np.percentile(var,75))
    comparator = np.nanpercentile(page_p[index],50)
    print 'Values: %s and Comparator value: %.4f' % (page_p[index], comparator)
    result_list_filtered =[]
    for r in result_list:
      if r['Value'] < comparator:
        result_list_filtered.append(r)

    return result_list_filtered

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Find connections between german wiki articles
# Copyright 2007, Andreas Maier

from pyparsing import Literal,Suppress,CharsNotIn,CaselessLiteral,\
        Word,dblQuotedString,alphanums,SkipTo,makeHTMLTags,NotAny

import time

import pprint
import urllib2
import string
import sys
reload(sys)
sys.setdefaultencoding("utf_8")

import cgi, cgitb
cgitb.enable()

from threading import Thread

class wikireader(Thread):
	def __init__ (self,keyword):
		Thread.__init__(self)
		self.keyword = keyword
		self.links = set()
		self.articlename = ""
	
	def run(self):
		page=self.get_wiki_page(self.keyword)
		(self.links, self.articlename) = self.get_linked_articles(page)
		
	def getname(self):
		return self.articlename
		
	def getlinks(self):
		return self.links

	def get_wiki_page(self,keyword):
	
		headers = { 
			'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3',
			'Accept-Encoding': 'deflate',
			'Accept-Charset': 'utf-8',
			'Referer': 'http://de.wikipedia.org/wiki/Hauptseite',
		}
		
		url = 'http://de.wikipedia.org/wiki/%s' % keyword
	
		try:
			request = urllib2.Request(url, None, headers)
			response = urllib2.urlopen(request)
			content = response.read()
			response.close()
			
			return content
			
		except urllib2.HTTPError:
			print "HTTPError: %s" % url
		  
	def get_linked_articles(self,wikipage):
		
		# Define the pyparsing grammar for a URL, that is:
		#    URLlink ::= <a href= URL>linkText</a>
		#    URL ::= doubleQuotedString | alphanumericWordPath
		# Note that whitespace may appear just about anywhere in the link.  Note also
		# that it is not necessary to explicitly show this in the pyparsing grammar; by default,
		# pyparsing skips over whitespace between tokens.
		
		
		linkOpenTag, linkCloseTag = makeHTMLTags("a")
		link = linkOpenTag + SkipTo(linkCloseTag).setResultsName("body") + linkCloseTag.suppress()
		
		
		# Go get some HTML with some links in it.
		# serverListPage = urllib.urlopen( "http://de.wikipedia.org/w/index.php?title=Hauptseite&redirect=no" )
		# htmlText = serverListPage.read()
		# serverListPage.close()
		# 	
		# print htmlText
		# 
		# scanString is a generator that loops through the input htmlText, and for each
		# match yields the tokens and start and end locations (for this application, we are
		# not interested in the start and end values).
		
		articles = set()
		
		for toks,strt,end in link.scanString(wikipage):
			if(len(toks.startA.href) != 0 and                    #remove empty links
			toks.startA.href.find('#')==-1 and                   #remove anchors
			toks.startA.href.find(':')==-1 and                   #remove wikipedia special links
			toks.startA.href.find('?')==-1 and                   #remove wikipedia special links
			toks.startA.href.find('Hauptseite')==-1):            #remove link to main page
				if(toks.body=="Artikel"):
					articlename=toks.startA.href.lstrip('/wiki/')  #save real(!) article name, so we don't get confused by redirects
				else:		
					articles.add(toks.startA.href.lstrip('/wiki/'))
				#print toks.startA.href,"->",toks.body
		
		return (articles,articlename)
	
class UnbufferedStdout:
	def __init__(self, stdout):
		self.stdout = stdout
	def write(self, arg):
		self.stdout.write(arg)
		self.stdout.flush()

sys.stdout = UnbufferedStdout(sys.stdout)	


arguments=set()
connections=set()				
firsttime=True

form=cgi.FieldStorage()
input=form.getvalue("search_terms")

terms=input.split()

print "Content-type: text/html\n"

print """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

<title>Wiki Connector 2.0!</title>
</head>"""	

print "<body>"

print "<p> Searching for connections ...</p>"

print time.ctime()

listofreaders=[]
for argument in terms:
	reader=wikireader(argument)
	listofreaders.append(reader)
	reader.start()

for reader in listofreaders:
	reader.join()
	if(firsttime):
		connections=reader.getlinks()
		firsttime=False
	else:
		connections=reader.getlinks()&connections
	
	arguments.add(reader.getname())
	


# for argument in terms:
# 	htmlsource=get_wiki_page(argument)
# 	links=get_linked_articles(htmlsource)
# 	if(firsttime):
# 		connections=links[0]
# 	else:
# 		connections=links[0]&connections
# 	firsttime=False
# 	arguments.add(links[1])
	


print "<p>"
print "The real(!) article names are:"	
print arguments
print "</p><p>"
print "All indirect connections between these articles are:"
print connections
print len(connections)

print "</p><p>"

nontrivial=set()

listofreaders=[]
for element in connections:
	reader=wikireader(element)
	listofreaders.append(reader)
	reader.start()
	
for reader in listofreaders:
	reader.join()
	links=reader.getlinks()
	if(arguments.issubset(links)):
 		print reader.getname() + " is a trivial link"
	else:
 		nontrivial.add(reader.getname())	
	
# nontrivial=set()		
# for element in connections:
# 	htmlsource=get_wiki_page(element)
# 	links=get_linked_articles(htmlsource)
# 	
# 	if(arguments.issubset(links[0])):
# 		print element + " is a trivial link"
# 	else:
# 		nontrivial.add(element)	
# 

print "</p><p>"	

print "All non-trivial connections between these articles are:"
print nontrivial
print len(nontrivial)

print "</p><p>"	

# 
# 
# if(len(connections)!=0 or len(terms)!=2):
# 	sys.exit(0)
# else:
# 	print "Starting recursive search! (Only possible for two articles)"
# 	
# 	
# 
# 	htmlsource=get_wiki_page(terms[0])
# 	links1a=get_linked_articles(htmlsource)
# 	
# 	htmlsource=get_wiki_page(terms[1])
# 	links1b=get_linked_articles(htmlsource)
# 	
# 	level2a=dict()
# 	level2b=dict()
# 	
# 	recursive=dict()
# 	
# 	for element in links1a[0]:
# 		htmlsource=get_wiki_page(element)
# 		templinks=get_linked_articles(htmlsource)
# 		level2a[element]=templinks[0]
# 		
# 		recursive[links1a[1]+"/"+element]=(templinks[0]&links1b[0],links1b[1])
# 		
# 	for element in links1b[0]:
# 		htmlsource=get_wiki_page(element)
# 		templinks=get_linked_articles(htmlsource)
# 		level2b[element]=templinks[0]
# 		
# 		recursive[links1b[1]+"/"+element]=(templinks[0]&links1a[0],links1a[1])
# 		
# 	for key, value in recursive.iteritems():
# 		if(len(value[0])!=0):
# 			print key, value
# 	
# 	#print level2a
# 	#print level2b	
# 	
print time.ctime()	
print "</p>"
	
print "</body>"
print "</html>"	
		
		
		
			
	
	






#-*- coding: utf-8 -*-
import os
import json
import time
import sched
import threading
from bs4 import BeautifulSoup
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

scheduler = sched.scheduler(time.time, time.sleep)

FILE_NAME = "pdwait.html"
INTERVAL_SECOND = 5 
gArrPDWaits = None
#gArrPDWaits = [ 'HELLO', 'WORLD' ]

class ThreadJob(threading.Thread):
	def __init__(self,callback,event,interval):
		self.callback = callback
		self.event = event
		self.interval = interval
		super(ThreadJob,self).__init__()

	def run(self):
		while not self.event.wait(self.interval):
			self.callback()

event = threading.Event()

def grabPDWait():
	global gArrPDWaits
	content_link = "http://web.humoruniv.com/board/humor/read.html?table=pdswait&pg=0&number="
	cmd = "wget http://web.humoruniv.com/board/humor/list.html?table=pdswait -q -O " + FILE_NAME
	os.system(cmd)
	
	fResult = open(FILE_NAME, 'r') 
	txtResult = fResult.read() 
	#print txtResult 
	
	soup = BeautifulSoup(txtResult, 'html.parser')
	tbEntire = soup.find('div', {'id': 'cnts_list_new'})
	arrContents = tbEntire.findAll('td', attrs={'class':'li_sbj'})
	arrIcons = tbEntire.findAll('td', attrs={'class':'li_icn'})
	arrDates = tbEntire.findAll('td', attrs={'class':'li_date'})
	
	gArrPDWaits = []
	for i in range(len(arrContents)):
		_link = arrContents[i].a['href']
		_id = _link[-7:]
		_time = arrDates[i].find('span', attrs={'class':'w_time'}).text
		_nick = None
		_span = arrIcons[i].find('span', attrs={'class':'hu_nick_txt'})
		_innerSpan = _span.find('span')
		if _innerSpan == None:
			_nick = _span.text
		else:
			_nick = _innerSpan.text
		gArrPDWaits.append( { 'id': _id, 'link': _link, 'nick': _nick, 'time': _time} )
		#print _link, type(_nick),  _nick, _time , _id
	print 'Grabbing Done gArrPDWaits length: ', len( gArrPDWaits )
	#print str(gArrPDWaits)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json;charset=utf-8')
        self.end_headers()

    def do_GET(self):
	global gArrPDWaits
        self._set_headers()
	for item in gArrPDWaits:
		print item['nick'],item['nick'].encode('utf8')
	json_string = json.dumps(gArrPDWaits, ensure_ascii=False, indent=2)
        encoded_string = json_string.encode('utf8')
	print encoded_string
        self.wfile.write(encoded_string)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=S, port=21101):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

threadGrabingPDWait = ThreadJob(grabPDWait,event,INTERVAL_SECOND)
threadGrabingPDWait.start()
run()
#grabPDWait()

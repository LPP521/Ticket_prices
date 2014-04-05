#!/usr/bin/env python
#coding=utf-8
import sys, threading
import gtk, webkit
import time
import gobject
import parseHTML1
from urllib import quote
import calendar

WAITE_TIME = 30
gobject.threads_init()

class WebView(webkit.WebView):
    def get_html(self):
        self.execute_script('oldtitle=document.title;document.title=document.documentElement.innerHTML;')
        html = self.get_main_frame().get_title()
        self.execute_script('document.title=oldtitle;')
        return html

class TimeSender(gobject.GObject, threading.Thread):
    def __init__(self):
        self.__gobject_init__()
        threading.Thread.__init__(self)

    def myEmit(self):
        window.emit("Sender_signal")

    def run(self):
        print "sleep {0} seconds".format(WAITE_TIME)
        print("time_start at {0}".format(time.time()))
        time.sleep(WAITE_TIME)
        gobject.idle_add(self.myEmit)
        print("time_start end {0}".format(time.time()))


class Window(gtk.Window, gobject.GObject):
    def __init__(self, url):
        self.__gobject_init__()
        gtk.Window.__init__(self)
        self.connect('Sender_signal', self._finished_loading)
        self._url = url

    def open_page(self):
        self.view = WebView()
        self.view.get_html()
        self.view.open(self._url)
        self.add(self.view)
        gtk.main()

    def _finished_loading(self, view1):
        gtk.main_quit()
        a = time.time()
        parseHTML1.parse( self.view.get_html() )
        b = time.time()
        print("Get html and parse:"+ str(b-a))

def url(Depart, Arrival, go_time):

    Depart   =  quote(Depart)
    Arrival  =  quote(Arrival)
    url      =  "http://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport={0}&searchArrivalAirport={1}&searchDepartureTime={2}&searchArrivalTime=2014-04-19&nextNDays=0&startSearch=True&from=fi_ont_search".format(Depart, Arrival, go_time)

    now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    f = open ( '/var/www/plane_price.txt', 'a' )
    f.write ( "{0}       {1}\n".format(go_time, now_time) )
    f.close()

    return url

def append_date(year, month, day):

    if month < 10:
        s_y = str(year)
        s_m = "0{0}".format(month)
        if day<10:
            s_d = "0{0}".format(day)
        else:
            s_d = "{0}".format(day)
    else :
        s_y = str(year)
        s_m = "{0}".format(month)
        if day < 10:
            s_d = "0{0}".format(day)
        else:
            s_d = "{0}".format(day)
    print s_y + "-" + s_m + "-" + s_d
    return s_y + "-" + s_m + "-" + s_d
    


def date_legal(year,month,day):
    if   year<2013:
        print "erro: Year < 2013"
        return False
    elif year>2038:
        print "erro: Year > 2038"
        return False
    elif month<0:
        print "erro: Month < 0"
        return False
    elif month>13:
        print "erro: Month > 13"
        return False
    elif day<0:
        print "erro: day < 0"
        return False
    elif day>calendar.monthrange(year, month)[1]:
        print "erro: day Too Large"
        return False
    elif year%1!=0:
        print "erro: year % 1 != 0"
        return False
    elif month%1!=0:
        print "erro: Month % 1 != 0"
        return False
    elif day%1!=0:
        print "erro: day % 1 != 0"
        return False
    else:
        return True



def arr_days(year,month,day):
    days = []
    first_month_max_day = calendar.monthrange(year, month)[1]
    
    if first_month_max_day == day:
        days.append(day)
    elif first_month_max_day > day:
        for i in xrange(day, first_month_max_day+1):
            days.append(i)
    for i in xrange(1, 1 + calendar.monthrange(year, month + 1)[1]):
        days.append(i)
    return days


start_time = time.time()
gobject.signal_new("Sender_signal", Window, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
year = 2014
month = 5
day = 25
Depart = "哈尔滨"
Arrival = "上海"

if date_legal(year, month, day):
    arr_days = arr_days(year, month, day)
    for i in arr_days:
        if i < i-1:
            month += 1
        go_time = append_date(year, month, i)
        window   =  Window(url(Depart, Arrival, go_time))
        time_sender = TimeSender()
        time_sender.start()
        print("Window at {0}".format(time.time()))
        window.open_page()
        print("Window end {0}".format(time.time()))
        
        time.sleep(120)

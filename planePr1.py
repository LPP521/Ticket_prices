#!/usr/bin/env python
#coding=utf-8
import sys, threading
#from gi.repository import Gtk
import gtk
import webkit
import time
import gobject
import re

import parseHTML1
from exception import *

from urllib import quote
import calendar


WAITE_TIME = 20
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
        print("sleep {0} seconds".format(WAITE_TIME))
        time.sleep(WAITE_TIME)
        gobject.idle_add(self.myEmit)


class Window(gtk.Window, gobject.GObject):
    def __init__(self, url):
        self.__gobject_init__()
        gtk.Window.__init__(self)
        self.connect('Sender_signal', self._finished_loading)
        self._url = url

    def open_page(self):
        self.view = WebView()
        self.view.open(self._url)
        self.add(self.view)
        gtk.main()

    def _finished_loading(self, view1):
        gtk.main_quit()
        parseHTML1.parse( self.view.get_html() )


def url(Depart, Arrival, go_time):
    Depart   =  quote(Depart)
    Arrival  =  quote(Arrival)
    url      =  "http://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport={0}&searchArrivalAirport={1}&searchDepartureTime={2}&searchArrivalTime=2014-04-19&nextNDays=0&startSearch=True&from=fi_ont_search".format(Depart, Arrival, go_time)
    now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    f = open ( 'plane_price.txt', 'a' )
    f.write ( "{0}       {1}\n".format(go_time, now_time) )
    f.close()
    print("--------------\n{0}\n--------------".format(url))
    return url

def append_date(year, month, day):
    if month < 10:
        str_y = str(year)
        str_m = "0{0}".format(month)
        if day<10:
            str_d = "0{0}".format(day)
        else:
            str_d = "{0}".format(day)
    else :
        str_y = str(year)
        str_m = "{0}".format(month)
        if day < 10:
            str_d = "0{0}".format(day)
        else:
            str_d = "{0}".format(day)
    return str_y + "-" + str_m + "-" + str_d
    

def date_legal(year,month,day):
    try:
        if   year<2013:
            raise InputDateError("Year < 2013")
        elif year>2038:
            raise InputDateError("Year > 2038")
        elif month<0:
            raise InputDateError("Month < 0")
        elif month>13:
            raise InputDateError("Month > 13")
        elif day<0:
            raise InputDateError("Day < 0")
        elif day>calendar.monthrange(year, month)[1]:
            raise InputDateError("No {0} days this month".format(day))
        elif year%1!=0:
            raise InputDateError("Year % 1 != 0")
        elif month%1!=0:
            raise InputDateError("Month % 1 != 0")
        elif day%1!=0:
            raise InputDateError("Day % 1 != 0")
        else:
            pass
    except InputDateError as e:
        print('InputDateError: '+(''.join(e.args)))
        exit()
    



print("-----main start-----")
#def console_arg(argv):
#    str_arg = "".join(argv)
#    print(str_arg)
#    date = re.search('\d\d\d\d', str_arg).group(0)
#    start_area = re.search("[^0-9A-Za-z\.]\w+(?=到\w+)", str_arg).group(0)
#    end_area = re.search("(?<=到)\w+", str_arg).group(0)
#    
#    print(date)
#    print(start_area)
#    print(end_area)

#console_arg(sys.argv)
gobject.signal_new("Sender_signal", Window, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
year    = int(time.strftime('%Y',time.localtime(time.time())))
month   = 8
day     = 30
Depart  = "哈尔滨"
Arrival = "上海"

date_legal(year, month, day)
go_time     = append_date(year, month, day)
window      = Window( url(Depart, Arrival, go_time) )
time_sender = TimeSender()
time_sender.start()
window.open_page()

        

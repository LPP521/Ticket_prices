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
        self.view.get_html()
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

    f = open ( '/var/www/plane_price.txt', 'a' )
    f.write ( "{0}       {1}\n".format(go_time, now_time) )
    f.close()

    return url

def append_date(year, month, day):
    if year>2013 and year<2038 and month>0 and month<13 and day>0 and year%1==0 and month%1==0:
        if calendar.monthrange(year, month)[1] >= day:
            print "Right Go_Time"
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
        else:
            print "DAY Wrong!*********"
            return 0
    else:
        print "Wrong Go_Time!!!"
        return 0



if __name__ == '__main__':
        
        gobject.signal_new("Sender_signal", Window, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
        year = 2014
        month = 5
        day = 25
        Depart = "哈尔滨"
        Arrival = "上海"
        go_time = append_date(year, month, day)
        
        window   =  Window(url(Depart, Arrival, go_time))
        time_sender = TimeSender()

        time_sender.start()
        window.open_page()

        print("退出阻塞，等待重启。")
        #time.sleep(60)
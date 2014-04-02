#!/usr/bin/env python
#coding=utf-8
import sys, threading
import gtk, webkit
import time
import gobject
import parseHTML1
WAITE_TIME = 30
gobject.threads_init()

class WebView(webkit.WebView):
    #return page's content
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


#gobject.type_register(TimeSender)

class Window(gtk.Window, gobject.GObject):
    def __init__(self, url, go_time):
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
    #write html to file
    def _finished_loading(self, view1):
        gtk.main_quit()
        now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        f = open ( '/var/www/plane_price.txt', 'a' )
        f.write ( "{0}       {1}\n".format(go_time, now_time) )
        f.close()
        parseHTML1.parse( self.view.get_html() )


if __name__ == '__main__':
        gobject.signal_new("Sender_signal", Window, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
        while True:
            time_sender = TimeSender()
            go_time = "2014-06-19"
            url = "http://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport=%E5%93%88%E5%B0%94%E6%BB%A8&searchArrivalAirport=%E4%B8%8A%E6%B5%B7&searchDepartureTime={0}&searchArrivalTime=2014-04-19&nextNDays=0&startSearch=true&from=fi_ont_search".format(go_time)
            window = Window(url, go_time)
    
            time_sender.start()
            window.open_page()
            print("退出阻塞，等待重启。")
            time.sleep(60)
    

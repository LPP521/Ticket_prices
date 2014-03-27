#!/usr/bin/env python
import sys, threading
import gtk, webkit
import time
import gobject

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


gobject.type_register(TimeSender)

class Window(gtk.Window, gobject.GObject):
    def __init__(self, time_sender, url):
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
        with open("pagehtml1.html", 'w') as f:
            f.write(self.view.get_html())
        gtk.main_quit()



if __name__ == '__main__':
    gobject.signal_new("Sender_signal", Window, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
    time_sender = TimeSender()
    go_time = "2014-06-30"
    url = "http://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport=%E5%93%88%E5%B0%94%E6%BB%A8&searchArrivalAirport=%E4%B8%8A%E6%B5%B7&searchDepartureTime={0}&searchArrivalTime=2014-04-19&nextNDays=0&startSearch=true&from=fi_ont_search".format(go_time)
    window = Window(time_sender, url)
    
    time_sender.start()
    window.open_page()

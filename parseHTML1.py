#coding=utf-8
from bs4 import BeautifulSoup
import re
def parse(content):
    content = content.encode("utf-8")
    f = open ( '/var/www/log_plane.html', 'w' )
    f.write ( content )
    f.close()
    print("HTML put in file '/var/www/log_plane.html'.")

    p = re.compile( '.*hdivResultPanel')
    useful_info = p.sub( '', content, count=1)
    soup = BeautifulSoup(useful_info)
    
    arr = useful_info.split("avt_column")
    items = soup.find_all(class_="avt_column")
    #print (items)
    
    for i in items:
        item = str(i)
        soup = BeautifulSoup(item)
    
        price = 0
        company_name = soup.find(class_="a_name").get_text().encode("utf-8")
        departure_time = soup.find(class_="a_tm_dep").get_text().encode("utf-8")
        arrival_time = soup.find(class_="a_tm_arv").get_text().encode("utf-8")
    
        width_left = soup.find(style="width:33px;left:-33px")
        if width_left == None:
            #print 'Can't find tag: style="width:33px;left:-33px"'
            continue
        else:
            #print(width_left.string)
            num_width_left = int(width_left.get_text())
    
        left33 = soup.find(style="left:-33px")
        if left33 != None:
            num_left33 = int(left33.get_text())
            #print("left33:%d"%num_left33)
        else:
            #print("no left33[1**]")
            num_left33 = num_width_left / 100
            #print("_left33:%d"%num_left33)
    
        left22 = soup.find(style="left:-22px")
        if left22 != None:
            num_left22 = int(left22.get_text())
            #print("left22:%d"%num_left22)
        else:
            #print("no left22[*1*]")
            num_left22 = num_width_left % 100 / 10
            #print("_left22:%d"%num_left33)
    
        left11 = soup.find(style="left:-11px")
        if left11 != None:
            num_left11 = int(left11.get_text())
            #print("left11:%d"%num_left11)
        else:
            #print("no left11[**1]")
            num_left11 = num_width_left % 10
            #print("_left11:%d"%num_left11)
    
        
        print("{0}   {4} - {5}   ￥{1}{2}{3}".format(company_name,num_left33, num_left22, num_left11, departure_time, arrival_time))

        f = open ( '/var/www/plane_price.txt', 'a' )
        f.write ( "{0}   {4} - {5}   ￥{1}{2}{3}\n".format(company_name,num_left33, num_left22, num_left11, departure_time, arrival_time) )
        f.close()


'''
Created on 2018-1-11

@author: liuchen
'''
#QQ好友动态爬取
import requests
import os
import sys
import time
import util
import csv
#爬取具体操作
class Get_moods(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = util.headers
        self.g_tk = util.g_tk

    def get_moods(self, qqnumber):
        '''利用cookie和header去爬取说说文件并保存到本地文件中'''

        referer = 'http://user.qzone.qq.com/' + qqnumber
        self.headers['Referer'] = referer

        # Get the goal url, except the position argument.
        url_base = util.parse_moods_url(qqnumber)
        
        filepath='/python/qqMoodCollect/mood_result/'+qqnumber+'/'
        filepath=filepath.strip()
        isExists=os.path.exists(filepath)
        if not isExists:
            os.makedirs(filepath)
        else:
            pass
                
        pos = 0
        key = True

        while key:
            print("\tDealing with position:\t%d" % pos)
            url = url_base + "&pos=%d" % pos
            #print(url)
            res = self.session.get(url, headers = self.headers)
            con = res.text
            f=open(filepath+str(pos)+'.txt','w')
            f.write(con)
            f.close()
            
            if '''"msglist":null''' in con:
                key = False

            # Cannot access...
            if '''"msgnum":0''' in con:
                print("%s Cannot access..\n" % qqnumber)
                key = False

            # Cookie expried
            if '''"subcode":-4001''' in con:
                print('Cookie Expried! Time is %s\n' % time.ctime())
                sys.exit()

            pos += 20
            time.sleep(5)
            
class Get_moods_start(object):

    def __init__(self):
        print('Start to get all friend\'s mood file and save it to the mood_result folder')

    def get_moods_start(self):
        app = Get_moods()
        csv_reader = csv.reader(open('/python/qqMoodCollect/QQmail.csv','r',encoding= 'gb18030'))
        qnumber_list=[]
        for row in csv_reader:
            qqnum=str(row[2][:len(row[2])-7])
            qnumber_list.append(qqnum)
        

        while qnumber_list != []:
            qq = qnumber_list.pop()
            print("Dealing with:\t%s" % qq)
            try:
                app.get_moods(qq)
            except KeyboardInterrupt:
                print('User Interrupt, program will exit')
                sys.exit()
            except Exception as e:
                exception_time = time.ctime()
                print("Exception occured: %s\n%s\n" % (exception_time, e))
            else:
                print("%s Finish!" % qq)
        else:
            print("Finish All!")
            
p=Get_moods_start().get_moods_start()
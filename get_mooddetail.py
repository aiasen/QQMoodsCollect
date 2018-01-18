'''
Created on 2018-1-11

@author: liuchen
'''
#从下载的文件中解析出有用信息
import json
import time
import os
import pymysql


def exact_mood_data(filename,qqnum):
    messages=[]
    f=open(filename,encoding= 'utf8',errors='ignore')
    con=f.read()
    con_dict = json.loads(con[10:-2])
    try:
        moods=con_dict['msglist']
    except KeyError:
        return
    if moods == None:
        return
    for mood in moods:
        cmtnum=mood['cmtnum']   #评论数   int
        content=mood['content']  #说说内容   str
        created_time=mood['created_time']   #发布时间    int
        time_local = time.localtime(created_time)
        dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        phone=mood['source_name']    #发布时手机  str
        message=(qqnum,cmtnum,content,dt,phone)
        messages.append(message)
    return messages

def store(messages):
    try:
        conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='python',port=3306,charset='utf8')
        cur=conn.cursor()
        sql='insert into qqfriendsmoods(qqnum,cmtnum,content,dt,phone)values(%s,%s,%s,%s,%s)'
        cur.executemany(sql,messages)
        conn.commit()
        cur.close()
        conn.close()
        return 1
    except Exception as e :
        print(e)
        return 0


basefilepath='E:\\闲时程序代码\\python\\QQFriendsDynamicCollect\\moods\\'
dirlist = os.listdir(basefilepath)
for qqnum in dirlist:
    txtlist = os.listdir(basefilepath+qqnum+'\\')
    print(qqnum+'正在处理')
    for txt in txtlist:
        filename = basefilepath + qqnum + '\\' + txt
        messages=exact_mood_data(filename,qqnum)
        if messages is None:
            continue
        else:
            if store(messages):
                print(txt+'存储成功')
            else:
                print(txt+'存储失败')
    print(qqnum + '处理完成')
    print()


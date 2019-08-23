#coding:utf-8
from django.shortcuts import render, redirect

import pymysql

from  util import sqlheper

import cv2
import time

def first(request):
    if request.method =='POST':
        adminid = request.POST.get('adminid')
        pwd = request.POST.get('adminpwd')
        # print("adminid:",adminid,pwd)
        if len(adminid)==0 or len(pwd)==0:

            return render(request, 'first.html', {"error": "请输入用户名和密码登录"})

        name_dic = sqlheper.get_one("select name from user where name=%s",[adminid,])
        pd_dic = sqlheper.get_list("select pwd from user where pwd=%s",[pwd,])
        # print(name_dic,pd_dic)
        if name_dic!=None and pd_dic!=None:

            nid = sqlheper.get_one("select id from user where name=%s",[name_dic['name'],])
            # nid=None
            # print(nid)

            ####进入主站入口
            return render(request, 'adminok.html',{"id":nid['id'] ,"name":name_dic})
        else:
            return render(request, 'first.html', {"error": "用户名或密码错误"})
    else:
        return render(request, 'first.html')

def admin(request):
    # sqlheper.get_list()
    id = request.POST.get('id')
    cap = cv2.VideoCapture(0)
    suc,img = cap.read()
    path = None
    # if suc:
    user = sqlheper.get_list("select * from user where id=%s",[id,])
    t = time.time()
    path ="/image/"+str(t)+".jpg"
    # cv2.imwrite("."+path, img)
    cap.release()
    # cv2.imshow("asd",img)
    # cv2.waitKey(0)
    return render(request, 'adminok.html', {"img": path, "user":user})

def database(request):

    if request.method == 'POST':
        nid = request.POST.get('nid')
        # nam = request.POST.get('n')
        con = request.POST.get('content')
        # date = request.POST.get('date')
        sqlheper.modify("update user set content=%s where id=%s",[con,nid,])
        # sqlheper.modify("update user set date=%s where id=%s",[date,nid,])
    if request.method == 'GET':
        nid = request.GET.get('nid')
    if nid ==None or len(nid)==0:
        print(nid)
        return redirect("/")
    content = sqlheper.get_list("select content from user",[])
    print(content)
    name = sqlheper.get_list("select name from user where id=%s",[nid,])
    # if content==None:
    #     return render(request, 'database.html', {'user': name, 'nid': nid})
    # else:
    return render(request, 'database.html', {'content': content, 'user': name, 'nid': nid})
    # return redirect('/admin/')


def add_class(request):

    if request.method =="GET":


        return render(request, 'add_content.html')
    # pass

    else:

        v = request.POST.get('name')
        v2 = request.POST.get('number')

        if len(v)>0 and len(v2)>0:

            conn = pymysql.connect(host='127.0.0.1', port=3306, user='liqin', passwd='1234', db='S4DB65')

            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            effect_row = cursor.execute(" insert into student(number,name) values(%s, %s)", [v2, v,])

            conn.commit()

            cursor.close()

            conn.close()

            return redirect("/database/")
        else:
            return render(request, 'add_content.html', {'msg': '请正确输入'})




def del_class(requst):

    nid = requst.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='liqin', passwd='1234', db='S4DB65')

    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 执行SQL,并返回受影响行数
    print(nid)
    effect_row = cursor.execute("update user set content=%s where id=%s", ["NULL",nid, ])
    # effect_row = cursor.execute("update hosts set host = '1.1.1.2' where nid > %s", (1,))

    # class_list = cursor.fetchall()

    # 提交,不然无法保存新建或修改的数据
    conn.commit()

    cursor.close()

    conn.close()

    return render(requst,"/database/?nid=%s" % nid)

def edit_class(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='liqin', passwd='1234', db='S4DB65')

    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 执行SQL,并返回受影响行数
    effect_row = cursor.execute("select * from user where id = %s", [nid, ])
    # effect_row = cursor.execute("update hosts set host = '1.1.1.2' where nid > %s", (1,))

    result = cursor.fetchone()

    # 提交,不然无法保存新建或修改的数据
    conn.commit()

    cursor.close()

    conn.close()

    return render(request , 'edit_class.html' ,{'result':result,'nid':nid})

def students(request):
    """
    学生列表
    :param request:
    :return:
    """

    result = sqlheper.get_list("select name from student",[])


    return  render(request, 'students.html', {'student_list':result})


def add_content(request):

    if request.method =="GET":
        nid = request.GET.get('nid')
    else:
        nid = request.POST.get('nid')
    # result = sqlheper.get_one("select ")

    return render(request, 'add_content.html',{'nid':nid})
    # pass

    # else:
    #
    #     v = request.POST.get('id')
    #     v2 = request.POST.get('content')
    #
    #     if len(v)>0 and len(v2)>0:
    #
    #         sqlheper.modify("insert into user(content) values(%s)",[v2,])
    #         return redirect("/database/")
    #     else:
    #         return render(request, 'add_content.html', {'msg': '请正确输入'})

def regist(requset):
    if requset.method =='POST':
        adminid = requset.POST.get('adminid')
        pwd = requset.POST.get('adminpwd')
        print("admin:",adminid,pwd)
        if len(adminid)!=0 and len(pwd)!=0:
            adm = sqlheper.get_list("select name from user where name=%s",[adminid,])
            if len(adm)==0:
                sqlheper.modify("insert into user(name,pwd) values(%s,%s)",[adminid,pwd])
                return render(requset, 'registerok.html')
            else:
                return render(requset, 'regist.html',{"err": "用户名已存在"})
        else:
            return render(requset, 'regist.html',{"err": "用户名或密码不能为空"})
    else:
        return render(requset, 'regist.html')

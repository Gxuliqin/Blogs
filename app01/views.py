#coding:utf-8
from django.shortcuts import render, redirect

import pymysql

from  util import sqlheper

def first(request):
    adminid = request.POST.get('adminid')
    pwd = request.POST.get('adminpwd')
    print("adminid:",adminid,pwd)
    if adminid==None or pwd==None:

        return render(request, 'first.html', {"error": "请输入用户名和密码登录"})

    name = sqlheper.get_list("select name from user where name=%s",[adminid,])
    pd = sqlheper.get_list("select pwd from user where pwd=%s",[pwd,])
    print(len(name),pd)
    if len(name)!=0 and len(pd)!=0:
        return render(request, 'adminok.html')
    else:
        return render(request, 'first.html', {"error": "用户名或密码错误"})

def admin(request):
    return render(request, 'adminok.html')

def database(request):

    if request.method == 'POST':
        id = request.POST.get('id')
        # nam = request.POST.get('n')
        con = request.POST.get('content')
        sqlheper.modify("insert into user(content) values(%s)",[con,])
    content = sqlheper.get_list("select content from user",[])
    name = sqlheper.get_list("select name from user ",[])
    return render(request, 'database.html', {'content': content, 'name': name})
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
    effect_row = cursor.execute("delete from student where id=%s", [nid, ])
    # effect_row = cursor.execute("update hosts set host = '1.1.1.2' where nid > %s", (1,))

    # class_list = cursor.fetchall()

    # 提交,不然无法保存新建或修改的数据
    conn.commit()

    cursor.close()

    conn.close()

    return redirect("/database/")

def edit_class(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='liqin', passwd='1234', db='S4DB65')

    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 执行SQL,并返回受影响行数
    effect_row = cursor.execute("select * from student where id = %s", [nid, ])
    # effect_row = cursor.execute("update hosts set host = '1.1.1.2' where nid > %s", (1,))

    result = cursor.fetchone()

    # 提交,不然无法保存新建或修改的数据
    conn.commit()

    cursor.close()

    conn.close()

    return render(request , 'edit_class.html' ,{'result':result})

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


        return render(request, 'add_content.html')
    # pass

    else:

        v = request.POST.get('id')
        v2 = request.POST.get('content')

        if len(v)>0 and len(v2)>0:

            sqlheper.modify("insert into user(content) values(%s)",[v2,])
            return redirect("/database/")
        else:
            return render(request, 'add_content.html', {'msg': '请正确输入'})

def regist(requset):
    adminid = requset.POST.get('adminid')
    pwd = requset.POST.get('adminpwd')
    if adminid!=None and pwd!=None:
        adm = sqlheper.get_list("select name from user where name=%s",[adminid,])
        if len(adm)==0:
            sqlheper.modify("insert into user(name,pwd) values(%s,%s)",[adminid,pwd])
            return render(requset, 'registerok.html')
        else:
            return render(requset, 'regist.html',{"err": "用户名已存在"})
    else:
        return render(requset, 'regist.html',{"err": "用户名或密码不能为空"})

#coding:utf-8
from django.shortcuts import render, redirect

import pymysql

from  util import sqlheper

def first(request):
    return render(request, 'first.html')

def admin(request):
    return render(request, 'admin.html')

def database(request):

    if request.method == 'POST':
        nid = request.POST.get('id')
        nam = request.POST.get('name')
        num = request.POST.get('number')

        conn = pymysql.connect(host='127.0.0.1', port=3306, user='liqin', passwd='1234', db='S4DB65')

        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        effect_row = cursor.execute("update  student set name=%s, number=%s where id =%s",[nam,num, nid,])
        # effect_row = cursor.execute("update  student set number=%s where id =%s",[num, nid,])

        result = cursor.fetchall()

        conn.commit()

        cursor.close()

        conn.close()
        print(nid)


    conn = pymysql.connect(host='127.0.0.1', port=3306, user='liqin', passwd='1234', db='S4DB65')

        #创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        #执行SQL,并返回受影响行数
    row = cursor.execute("select * from  student")
        # effect_row = cursor.execute("update hosts set host = '1.1.1.2' where nid > %s", (1,))

    class_list = cursor.fetchall()

        #提交,不然无法保存新建或修改的数据
    conn.commit()

    cursor.close()

    conn.close()

    return render(request, 'database.html', {'class_list': class_list})
    # return redirect('/admin/')


def add_class(request):

    if request.method =="GET":


        return render(request, 'add_class.html')
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
            return render(request, 'add_class.html' ,{'msg':'请正确输入'})




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

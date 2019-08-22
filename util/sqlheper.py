import pymysql

def get_list(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='liqin', passwd='1234', db='S4DB65')

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    effect_row = cursor.execute(sql,args)
    # effect_row = cursor.execute("update  student set number=%s where id =%s",[num, nid,])

    result = cursor.fetchall()

    conn.commit()

    cursor.close()

    conn.close()

    return result

def modify(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='liqin', passwd='1234', db='S4DB65')

    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    effect_row = cursor.execute(sql,args)
    # effect_row = cursor.execute("update  student set number=%s where id =%s",[num, nid,])

    # result = cursor.fetchall()

    conn.commit()

    cursor.close()

    conn.close()

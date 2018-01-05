# blog/views.py

from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import json
import MySQLdb




def hello_world(request):
    '''
    dataobj = [
        {
        'name': '安心亞',
        'shares': 100,
        'price': 542.23
        },
        {
        'name': '測試用',
        'shares': 200,
        'price': 200
        }
    ]
    #return HttpResponse("Hello World!")

    return render(request, 'hello_world.html', {
            'current_time': str(datetime.now()),
            'data_list': dataobj,
        })

    # ----pymysql----
    conn = pymysql.connect(
        host='myforumdb.cixpfwki9s8p.us-east-2.rds.amazonaws.com',
        port=3306,
        user='root',
        password='Aa123456',
        db='myforumdb',
    )


    a = conn.cursor()
    sql = ' select * from TB_USER ;'
    a.execute(sql)

    countrow = a.execute(sql)

    data = a.fetchall()

    return render(request, 'hello_world.html', {'data_list': data, })
    '''

    # connection mysql
    db = MySQLdb.connect(
        host='myforumdb.cixpfwki9s8p.us-east-2.rds.amazonaws.com',
        port=3306,
        user='root',
        password='Aa123456',
        db='myforumdb',
    )
    cursor = db.cursor()

    # 執行mysql查詢
    sql = ' select * from TB_USER ;'
    cursor.execute(sql)

    results = cursor.fetchall()

    return render(request, 'hello_world.html', {'data_list': results, })

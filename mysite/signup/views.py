# -*- coding: utf-8 -*-
from django.shortcuts import render
import MySQLdb
from django.contrib import auth

# 顯示所有文章
def showAllTopic():
    # connection mysql
    db = MySQLdb.connect(
        host='***.amazonaws.com',
        port=3306,
        user='root',
        password='Aa123456',
        db='myforum',
        charset='utf8'
    )
    cursor = db.cursor()

    # 執行mysql查詢
    sql = "SELECT ID_ARTICLE, TOPIC, VIEWS, REPLY_COUNT, CREATION_TIME, \
    DISPLAY_ID, AUTHOR_ID \
    FROM VW_USER_ARTICLE WHERE STATUS = 1 "

    cursor.execute(sql)
    data_list = cursor.fetchall()

    cursor.close()
    db.close()

    return data_list

def show_top_article():
    db = MySQLdb.connect(
        host='***.amazonaws.com',
        port=3306,
        user='root',
        password='Aa123456',
        db='myforum',
        charset='utf8'
    )
    cursor = db.cursor()

    # 執行mysql查詢
    sql = "SELECT ID_ARTICLE, TOPIC,VIEWS FROM VW_USER_ARTICLE WHERE STATUS=1 order by VIEWS DESC"

    cursor.execute(sql)
    top_article = cursor.fetchall()

    cursor.close()
    db.close()

    return top_article

# 登入紀錄
def login_insert_log(userid, session_id):
    # connection mysql
    db = MySQLdb.connect(
        host='***.amazonaws.com',
        port=3306,
        user='root',
        password='Aa123456',
        db='myforum',
        charset='utf8'
    )
    cursor = db.cursor()

    # 執行mysql新增
    sql = "INSERT INTO TB_LOG(LOGIN_USER_ID, SESSION_ID) VALUES ('%s', '%s')" % (userid, session_id)

    try:
        cursor.execute(sql)
        logid = int(cursor.lastrowid)
        db.commit()
    except:
        db.rollback()

    finally:
        cursor.close()
        db.close()
    return logid

def sign_up(request):
    return render(request, 'registration.html')

#登入驗證
def login(request):
    # clear session
    # clearSession()
    session_id = request.session.session_key
    request.session['session_id'] = session_id
    errmsg = ''
    # 過濾 sql injection
    username = request.POST['username'].replace("'"," ")
    password = request.POST['password'].replace("'"," ")




    # connection mysql
    db = MySQLdb.connect(
        host='***.amazonaws.com',
        port=3306,
        user='root',
        password='Aa123456',
        db='myforum',
        charset='utf8'
    )
    cursor = db.cursor()

    # 執行mysql查詢
    sql = "SELECT * FROM TB_USER WHERE DISPLAY_ID = '%s' and PWD = '%s'" % (username,password)

    cursor.execute(sql)

    logindata = cursor.fetchone()

    countrow = cursor.execute(sql)

    cursor.close()
    db.close()
    if countrow > 0 :
        request.session['session_userid'] = logindata[0]
        request.session['session_username'] = logindata[1]

        # 紀錄LOG
        logid = login_insert_log(logindata[0],session_id)
        request.session['session_logid'] = logid

        data_list = showAllTopic()
        top_article = show_top_article()
        return render(request, 'forum.html', {'data_list': data_list,'top_article':top_article })
    else :
        errmsg = '登入失敗，帳號或密碼錯誤'
        return render(request, 'registration.html', {'data_list': errmsg, })

#註冊
def registration (request):
    errmsg =''
    usernamesignup = request.POST['usernamesignup']
    emailsignup = request.POST['emailsignup']

    passwordsignup = request.POST['passwordsignup']
    passwordsignup_confirm = request.POST['passwordsignup']

    # connection mysql
    db = MySQLdb.connect(
        host='***.amazonaws.com',
        port=3306,
        user='root',
        password='Aa123456',
        db='myforum',
        charset='utf8'
    )
    cursor = db.cursor()

    # 檢查id、email是否重複
    sql2 = "SELECT * FROM TB_USER WHERE DISPLAY_ID = '%s' or EMAIL = '%s'" % (usernamesignup,emailsignup)
    cursor.execute(sql2)

    countrow = cursor.execute(sql2)

    if countrow > 0:
        errmsg = '帳號或密碼已註冊，請重新註冊或登入'
        return render(request, 'registration.html', {'data_list': errmsg, })
    else:
        # 執行mysql新增
        sql = "INSERT INTO TB_USER(DISPLAY_ID, \
               PWD, EMAIL, STATUS) \
               VALUES ('%s', '%s', '%s', '%c')" % \
              (usernamesignup, passwordsignup, emailsignup, 1)

        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

        finally:
            cursor.close()
            db.close()

        errmsg = '註冊成功請重新登入'
        return render(request, 'registration.html', {'data_list': errmsg, })

# 顯示作者資訊
def profile(request):
    authorid = request.GET['authorid']

    # connection mysql
    db = MySQLdb.connect(
        host='***.amazonaws.com',
        port=3306,
        user='root',
        password='Aa123456',
        db='myforum',
        charset='utf8'
    )
    cursor = db.cursor()

    sql = "SELECT * FROM TB_USER WHERE ID_USER = '%s' " % (authorid)

    sql2 = "SELECT COUNT(*) AS POSTS FROM TB_ARTICLE WHERE AUTHOR_ID = '%s' " %(authorid)

    cursor.execute(sql)
    returnData = cursor.fetchone()

    cursor.execute(sql2)
    posts = cursor.fetchone()


    return render(request, 'profile.html', {'returnData': returnData, 'posts':posts,})

def logout(request):
    del request.session['session_id']
    del request.session['session_userid']
    del request.session['session_username']

    auth.logout(request)

    return render(request, 'registration.html')





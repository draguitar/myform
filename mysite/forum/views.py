# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from signup.views import showAllTopic
from signup.views import show_top_article
import MySQLdb
import operator

# 閱讀紀錄
def read_log(logid, articleid):

    '''
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

    sql = "SELECT * FROM TB_LOG WHERE ID_LOG = '%s' " % (logid)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        sql2 = "UPDATE TB_LOG SET ARTICEL_ID1 = articleid WHERE ID_LOG = '%c'" % (row[0])


    try:
        cursor.execute(sql2)
        db.commit()

    except:
        db.rollback()

    finally:
        cursor.close()
        db.close()

    '''


def go_forum(request):
    try :
        if request.session['session_logid'] is None :
            return HttpResponseRedirect('/signup/')
        else :
            data_list = showAllTopic()
            top_article = show_top_article()
            return render(request, 'forum.html', {'data_list': data_list,'top_article':top_article })
    except:
        return HttpResponseRedirect('/signup/')

# 選擇文章
def topic(request):
    articleid = request.GET['articleid']
    try:
        logid = request.session['session_logid']
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

        # 增加觀看次數
        sql3 = "UPDATE TB_ARTICLE SET VIEWS = VIEWS + 1 WHERE ID_ARTICLE = '%s'" % (articleid)
        cursor.execute(sql3)

        # 執行mysql查詢
        # 主文章
        sql = "SELECT * FROM VW_USER_ARTICLE WHERE ID_ARTICLE = '%s' " % (articleid)
        cursor.execute(sql)
        data_list = cursor.fetchone()

        # 回覆內容
        sql2 = "SELECT * FROM VW_REPLY_ARTICLE WHERE ARTICLE_ID = '%s' " % (articleid)
        cursor.execute(sql2)
        # 回覆次數
        replyies = cursor.execute(sql2)

        replydata_list = cursor.fetchall()

        # 寫入閱讀紀錄
        read_log(logid,articleid)

        # 推薦閱讀演算法

        sql4 = "SELECT ID_LOG,ARTICLE_ID1,ARTICLE_ID2,ARTICLE_ID3 \
               FROM TB_LOG \
               WHERE ARTICLE_ID1 = '%s' or ARTICLE_ID2 = '%s' or ARTICLE_ID3 = '%s'" % (articleid,articleid,articleid)

        sql5 = "SELECT ID_ARTICLE FROM VW_USER_ARTICLE "

        cursor.execute(sql5)
        article_list = cursor.fetchall()

        dist = {}
        for d in article_list :
            dist[d[0]] = 0

        cursor.execute(sql4)
        rows = cursor.fetchall()


        for row in rows :
            if int(row[1]) != int(articleid):
                dist[row[1]] = int(dist[row[1]])+1
            if int(row[2]) != int(articleid):
                dist[row[2]] = int(dist[row[2]])+1
            if int(row[3]) != int(articleid):
                dist[row[3]] = int(dist[row[3]])+1



        dist_sorted = sorted(zip(dist.values(), dist.keys()))
        new_dist = zip(dist.values(), dist.keys())
        # 推薦文章的ID
        recommend_article_id = max(new_dist)[1]

        sql = "SELECT ID_ARTICLE, TOPIC FROM VW_USER_ARTICLE WHERE ID_ARTICLE = '%s' " % (recommend_article_id)
        cursor.execute(sql)
        recommend_article = cursor.fetchone()

        db.commit()

        cursor.close()
        db.close()

        return render(request, 'content.html', {'data_list': data_list, 'replydata_list':replydata_list,'replyies':replyies,'recommend':recommend_article})
    except:
        return HttpResponseRedirect('/signup/')
def new_post(request):
    return render(request, 'new_article.html')

def save_post(request):
    errmsg = ''
    # 檢查是否有輸入
    if request.POST['topic'].strip() == '' or request.POST['content'].strip() == '':
        errmsg = '欄位請勿空白'
        return render(request, 'new_article.html', {'errmsg': errmsg})

    else :
        userid = request.session['session_userid']
        topic = request.POST['topic'].replace("'", " ")
        topic = topic.replace('"', ' ')

        content = request.POST['content'].replace("'", " ")
        content = content.replace('"', ' ')
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

        sql = "INSERT INTO TB_ARTICLE(TOPIC, CONTENT, AUTHOR_ID) \
                       VALUES ('%s', '%s', '%s')" % (topic, content, userid)

        try:
            cursor.execute(sql)
            db.commit()

        except:
            db.rollback()

        finally:
            cursor.close()
            db.close()

        data_list = showAllTopic()
        top_article = show_top_article()
        return render(request, 'forum.html', {'data_list': data_list, 'top_article': top_article})

# 回覆文章
def save_reply(request):

    article_id = request.POST['article_id']
    userid = request.session['session_userid']
    reply = request.POST['replyArea']

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

    sql = "INSERT INTO TB_REPLY(ARTICLE_ID, REPLY_CONTENT, AUTHOR_ID) VALUES ('%s', '%s', '%s')" % (article_id, reply, userid)
    sql2 = "UPDATE TB_ARTICLE SET REPLY_COUNT = REPLY_COUNT + 1 WHERE ID_ARTICLE = '%s'" % (article_id)

    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        db.commit()

    except:
        db.rollback()

    finally:
        cursor.close()
        db.close()



    data_list = showAllTopic()
    return render(request, 'forum.html', {'data_list': data_list, })
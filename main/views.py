import flask 
from flask import request, make_response
from main import app, db
from main.models import Entry
from sqlalchemy import desc
import datetime
from io import StringIO
import csv

@app.route('/', methods=['get','post'])
def show_entries():
    entries_head = Entry.query\
                    .order_by(desc(Entry.date))\
                    .limit(5)\
                    .all()
    return flask.render_template('entry.html', entries_head=entries_head)

@app.route('/entry-done', methods=['GET','POST'])
def add_entry():
    entry = Entry(\
            jcode=flask.request.form['jcode']\
            ,temp=flask.request.form['temp']\
            ,date =datetime.datetime.now()\
            ,comment =flask.request.form['comment']\
            ,breathlessness =flask.request.form['breathlessness']\
            ,dullness =flask.request.form['dullness'])
    db.session.add(entry)
    db.session.commit()
    specified_jcode = request.form.get('jcode')
    sorted_result = db.session.query(Entry)\
                    .filter(Entry.jcode == specified_jcode)\
                    .order_by(desc(Entry.date))\
                    .all()
    return flask.render_template('logs-result.html', specified_jcode=specified_jcode, sorted_result=sorted_result)

@app.route('/logs-specify', methods=['get','post'])
def specify_logs():
    return flask.render_template('logs-specify.html')

@app.route('/logs-result', methods=['post'])
def sort_logs():
    specified_jcode = request.form.get('jcode') 
    sorted_result = db.session.query(Entry)\
                    .filter(Entry.jcode == specified_jcode)\
                    .order_by(desc(Entry.date))\
                    .all()
    return flask.render_template('logs-result.html', specified_jcode=specified_jcode, sorted_result=sorted_result)

@app.route('/download/<key>/', methods=['get','post'])
def download_csv(key):
    f = StringIO()
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")

    if key == 'all':
        writer.writerow(['id','jcode','date','temp','breathlessness','dullness','comment'])
        for i in Entry.query.all():
            writer.writerow([i.id, i.jcode, i.date, i.temp, i.breathlessness, i.dullness, i.comment])
    else:
        writer.writerow(['記録ID','Myコード','記録日時','体温','息つらい','体だるい','その他メモ'])
        for i in Entry.query.filter(Entry.jcode == key).all():
            writer.writerow([i.id, i.jcode, i.date.strftime('%a %m-%d %H:%M'), i.temp, i.breathlessness, i.dullness, i.comment])

    res = make_response()
    res.data = f.getvalue()
    res.headers['Content-Type'] = 'text/csv'
    res.headers['Content-Disposition'] = 'attachment; filename = ken-on-log_'+ key +'.csv'
    return res



# SQLクエリの書き方
# 本来の記述はsessionを使う。           db.session.query(Entry).all()
# 'Entry'クラスが持つヘルパー機能のため   Entry.query.all() 　に省略可能
#   'Entry'         クラス名＝テーブル名
#   .query          クエリ（指示）
#   .order_by()     並び順を指定
#   desc(Entry.date)    'date'カラムの降順で
#   .all()          全件取得
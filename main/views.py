import flask 
from flask import request, make_response
from main import app, db
from main.models import Entry
from sqlalchemy import desc
import datetime
from io import StringIO
import csv

@app.route('/', methods=['get','post'])
def show_entry():
    return flask.render_template('entry.html')

@app.route('/entry-done', methods=['GET','POST'])
def add_entry():
    entry = Entry(\
            line_id =flask.request.form['line_id']\
            ,line_name =flask.request.form['line_name']\
            ,temp =flask.request.form['temp']\
            ,date =datetime.datetime.now()\
            ,breathlessness =flask.request.form['breathlessness']\
            ,dullness =flask.request.form['dullness']\
            ,comment =flask.request.form['comment'])
    db.session.add(entry)
    db.session.commit()
    specified_id = request.form.get('line_id')
    specified_name = request.form.get('line_name')
    sorted_result = db.session.query(Entry)\
                    .filter(Entry.line_id == specified_id)\
                    .order_by(desc(Entry.date))\
                    .all()
    return flask.render_template('logs-result.html', specified_id=specified_id, specified_name=specified_name, sorted_result=sorted_result)

@app.route('/logs-result', methods=['GET','post'])
def sort_logs():
    specified_id = request.form.get('line_id')
    specified_name = request.form.get('line_name')
    sorted_result = db.session.query(Entry)\
                    .filter(Entry.line_id == specified_id)\
                    .order_by(desc(Entry.date))\
                    .all()
    return flask.render_template('logs-result.html', specified_id=specified_id, specified_name=specified_name, sorted_result=sorted_result)

@app.route('/download/<key>/', methods=['get','post'])
def download_csv(key):
    f = StringIO()
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")

    if key == 'all':
        writer.writerow(['id','line_id','line_name','date','temp','breathlessness','dullness','comment'])
        for i in Entry.query.all():
            writer.writerow([i.id, i.line_id, i.line_name, i.date, i.temp, i.breathlessness, i.dullness, i.comment])
    else:
        writer.writerow(['管理No','LINE名','記録日時','体温','息つらい','体だるい','その他メモ'])
        for i in Entry.query.filter(Entry.line_id == key).all():
            writer.writerow([i.id, i.line_name ,i.date.strftime('%a %m-%d %H:%M'), i.temp, i.breathlessness, i.dullness, i.comment])
    
    dt_now = datetime.datetime.now()
    res = make_response()
    res.data = f.getvalue()
    res.headers['Content-Type'] = 'text/csv'
    res.headers['Content-Disposition'] = 'attachment; filename = ken-on-log_'+ dt_now.strftime('%Y%m%d-%H:%M:%S') +'.csv'
    return res



# SQLクエリの書き方
# 本来の記述はsessionを使う。           db.session.query(Entry).all()
# 'Entry'クラスが持つヘルパー機能のため   Entry.query.all() 　に省略可能
#   'Entry'         クラス名＝テーブル名
#   .query          クエリ（指示）
#   .order_by()     並び順を指定
#   desc(Entry.date)    'date'カラムの降順で
#   .all()          全件取得
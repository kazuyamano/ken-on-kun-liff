from main import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.String)
    line_name = db.Column(db.String)
    temp = db.Column(db.Float)
    date = db.Column(db.DateTime)
    breathlessness = db.Column(db.String)
    dullness = db.Column(db.String)
    comment = db.Column(db.String)

    def __repr__(self):
        return "<Entry id={} line_id={} line_name={!r} temp={} date={} breathlessness={!r} dullness={!r} comment={!r}>"\
            .format(self.id, self.line_id, self.line_name, self.temp, self.date, self.breathlessness, self.dullness, self.comment)

def init():
    db.create_all()

# __repr__はデバッグの時に正式な文字列を返す（たとえば'1'は 1 でなく、'1'と返される）　←repr()を呼ぶ
# !rも上と同じことを.format()メソッドの結果に対して行う!
from main.models import Entry
import pandas as pd

if key == 'all': 
  l = [[i.id,i.jcode,i.date,i.temp,i.breathlessness,i.dullness,i.comment] for i in Entry.query.all()]
  df= pd.DataFrame(l, columns=['id','jcode','created_at','temp','breathlessness','dullness','comment'])
else:
  l = [[i.id,i.jcode,i.date.strftime('%a %m-%d %H:%M'),i.temp,i.breathlessness,i.dullness,i.comment] for i in Entry.query.filter(Entry.jcode == key).all()]
  df= pd.DataFrame(l, columns=['登録No','社員コード','登録日時','体温','息苦しさ','強いだるさ','その他メモ'])

df.to_csv(''+ key +'.csv', index=False)
from flask import Flask, render_template
import pandas as pd
import langid
from matplotlib import pyplot as plt
import glob
import collections

app = Flask(__name__)
plt.xkcd()



df_history = pd.read_json('Takeout\YouTube and YouTube Music\history\watch-history.json')
print(df_history)




files = glob.glob("Takeout\YouTube and YouTube Music\playlists\*.csv")
plt.style.use("fivethirtyeight")
df_playlists = pd.DataFrame()
playlists_vid_count=0

for f in files:
    csv = pd.read_csv(f)
    df_playlists = df_playlists.append(csv)
    playlists_vid_count += len(csv.index)

df_playlists = df_playlists.drop(columns=['Description','Visibility','Title'])

years = []
for i in range(playlists_vid_count):
    if(type(df_playlists.iloc[i][2]) == str):
        years.append(df_playlists.iloc[i][2][0:4])


years = collections.Counter(years)
pie_year_data = []
years_labes = []

for k,v in years.items():
    pie_year_data.append(v)
    years_labes.append(k)

plt.pie(pie_year_data, labels=years_labes)
plt.title('Playlists Creation Years')
plt.tight_layout
plt.savefig('static/img/pie_playlist_years.png')
plt.clf()

df_sub = pd.read_csv('Takeout\YouTube and YouTube Music\subscriptions\subscriptions.csv')
sub_count = len(df_sub.index)
hebrew_count = 0    

for row in df_sub.iterrows():
    if langid.classify(row[1][-1])[0] == 'he':
        hebrew_count += 1
pie_data = [hebrew_count ,len(df_sub.index)-hebrew_count]
pie_labels = ['Hebrew', 'Others']
plt.pie(pie_data, labels=pie_labels)
plt.title('Subcribers Languages')
plt.tight_layout
plt.savefig('static/img/pie_lang.png')

@app.route("/")
def home():
    return render_template('index.html', sub_tables=[df_sub.to_html(classes='data')], playlists_tables=[df_playlists.to_html(classes='data')],sub_count = sub_count, hebrew_count = hebrew_count,
        playlists_vid_count =playlists_vid_count)
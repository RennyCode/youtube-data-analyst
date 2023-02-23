from flask import Flask, render_template
import pandas as pd
import langid
from matplotlib import pyplot as plt
import glob
import collections
import datetime
app = Flask(__name__)
plt.xkcd()
plt.style.use("fivethirtyeight")

files = glob.glob("Takeout\YouTube and YouTube Music\playlists\*.csv")
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
active_years = years.most_common(1)[0][0]
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
plt.clf()


last_years_count = [0,0,0]
hours = [0,0,0,0]
labels_hours = ["6am-11am","11am-6pm","6pm-11pm","11pm-6am"] 
current_year = datetime.datetime.now().date().strftime("%Y")
last_years = [int(current_year),int(current_year)-1,int(current_year)-2]
df_search = pd.read_json('Takeout\YouTube and YouTube Music\history\search-history.json')
i = 0
for item in df_search["time"]:
    if int(item[0:4]) == int(current_year)-1:
        last_years_count[0] = i-1
        time = int(item[14:16]) 
        if time >= 6 and time < 11:
            hours[0] += 1
        elif time >= 11 and time < 18:
            hours[1] += 1
        elif time >= 18 and time < 23:
            hours[2] += 1
        else:
            hours[3] += 1

    elif int(item[0:4]) == int(current_year)-2:
        last_years_count[1] = i-1
    elif int(item[0:4]) == int(current_year)-3:
        last_years_count[2] = i-1
    elif int(item[0:4]) < int(current_year)-3:
        break
    i +=1

plt.pie(last_years_count, labels=last_years)
plt.title('Search Years Activity')
plt.tight_layout
plt.savefig('static/img/pie_years_search.png')
plt.clf()

plt.pie(hours, labels=labels_hours)
plt.title('Search Hours Activity')
plt.tight_layout
plt.savefig('static/img/pie_hours_search.png')
plt.clf()

df_history = pd.read_json('Takeout\YouTube and YouTube Music\history\watch-history.json')
bar_data = [0,0,0,0,0]
libs_counts = [0,0,0,0,0]
codes_counts = [0,0,0,0]
games_counts = [0,0,0,0]
history_count = len(df_history['title'])
for item in df_history["title"]:
    if item.find('anime') != -1 or item.find('Anime') != -1:      
        bar_data[0] += 1
    elif item.find('game') != -1 or item.find('Game') != -1:  
        bar_data[1] += 1
    elif item.find('music') != -1 or item.find('Music') != -1:  
        bar_data[2] += 1
    elif item.find('Tiktok') != -1 or item.find('tiktok') != -1:  
        bar_data[3] += 1
    elif item.find('motivation') != -1 or item.find('insparation') != -1 or  item.find('Motivation') != -1 or item.find('insparation') != -1:
        bar_data[4] += 1
    elif item.find('numpy')!= -1 or item.find('NumPy')!= -1:  
        libs_counts[0] += 1 
    elif item.find('pandas')!= -1 or item.find('Pandas') != -1:  
        libs_counts[1] += 1
    elif item.find('langid') != -1 or item.find('Langrid') != -1:
        libs_counts[2] += 1
    elif item.find('matplotlib') != -1 or item.find('Matplotlib') != -1:
        libs_counts[3] += 1   
    elif item.find('flask') != -1 or item.find('FLASK') != -1 or item.find('Flask') != -1:
        libs_counts[4] += 1
    elif item.find('python')!= -1 or item.find('Python') != -1:  
        codes_counts[0] += 1
    elif item.find('java') != -1 or item.find('Java') != -1:
        codes_counts[1] += 1
    elif item.find('php') != -1 or item.find('PHP') != -1:
        codes_counts[2] += 1
    elif item.find('C++') != -1 or item.find('C#') != -1:
        codes_counts[3] += 1
    elif item.find('pokemon')!= -1 or item.find('Pokemon') != -1:  
        games_counts[0] += 1
    elif item.find('League Of Legends') != -1 or item.find('league of legends') != -1:
        games_counts[1] += 1
    elif item.find('hearthstone') != -1 or item.find('Hearthstone') != -1:
        games_counts[2] += 1
    elif item.find('Apex') != -1 or item.find('APEX') != -1 or item.find('apex') != -1:
        games_counts[3] += 1

libs = ['Numpy', 'Pandas','Langid','Matplotlib','flask']
plt.bar(libs, libs_counts)
plt.title('Watch Code Language')
plt.tight_layout
plt.savefig('static/img/pie_lib_history.png')
plt.clf()

codes = ['Python', 'Java','Php','C++/C#']
plt.bar(codes, codes_counts)
plt.title('Watch Code Language')
plt.tight_layout
plt.savefig('static/img/pie_code_history.png')
plt.clf()

games = ['Pokemon', 'League','Hearthstone','Apex']
plt.bar(games, games_counts)
plt.title('Watch Games')
plt.tight_layout
plt.savefig('static/img/pie_game_history.png')
plt.clf()

bar_labels = ['Music','Game', 'Anime', 'Tiktok','Motivation']
plt.bar(bar_labels, bar_data)
plt.title('Hisory Watch')
plt.tight_layout
plt.savefig('static/img/bar_history.png')

@app.route("/")
def home():
    return render_template('index.html', active_years = active_years,sub_count = sub_count, hebrew_count = hebrew_count,
        playlists_vid_count =playlists_vid_count, anime_count = bar_data[0], history_count = history_count)
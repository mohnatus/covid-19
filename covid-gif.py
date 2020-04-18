# Section 1 - Importing Libraries
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import glob
import moviepy.editor as mpy

# Section 2 - Loading Data into Dataframes
df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv', parse_dates=['date'])
populations = pd.read_csv('nst-est2019-alldata.csv?#', usecols=['NAME', 'POPESTIMATE2019'])

# Section 3 - Merging in Population Data & Calculating Rates
df = pd.merge(df, populations, how = 'left', left_on = 'state', right_on = 'NAME')
df['rate'] = df['cases'] / df['POPESTIMATE2019'] * 100000

# Section 4 - Identifying States
df_today = df[df['date'] == datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')]
topfivestates_rate = list(df_today.sort_values(by='rate', ascending=False).head()['state'])
topfivestates_rate.append('California')
topfivestates_rate.append('Washington')

# Section 5 - Filtering our Dataset
df = df[df['state'].isin(topfivestates_rate)]
df = df[df['date'] >= '2020-03-01']
df = df.pivot(index = 'date', columns = 'state', values = 'rate')

# Section 6 - Preparing out Dataset for Graphing
df = df.reset_index()
df = df.reset_index(drop=True)
df = df.drop(columns = 'date')

# Section 7 - Graphing our Data
plt.style.use('fivethirtyeight')
length = len(df.index)
for i in range(10,length+10):
    ax = df.iloc[:i].plot(figsize=(12,8), linewidth=5, color = ['#173F5F', '#20639B', '#2CAEA3', '#F6D55C', '#ED553B', '#B88BAC', '#827498'])
    ax.set_ylim(0, 1000)
    ax.set_xlabel('Days since March 1, 2020')
    ax.set_ylabel('# of Cases per 100,000 People')
    ax.set_title("Cases per 100,000 People", fontsize = 18)
    ax.legend(loc='upper left', frameon=False)
    ax.grid(axis='x')
    fig = ax.get_figure()
    fig.savefig(f"[path to folder]/pngs/{i}.png")

# Section 8 - Generating our GIF
gif_name = 'COVID.gif'
fps = 6
file_list = glob.glob('[path to your PNG folder]/*')
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('{}.gif'.format(gif_name), fps=fps)pip install
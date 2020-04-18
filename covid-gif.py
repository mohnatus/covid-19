# Импорт библиотек
import pandas as pd
import matplotlib.pyplot as plt
import glob
import moviepy.editor as mpy

# Преобразование данных в датафреймы
df = pd.read_csv('us-states.csv', parse_dates=['date'])
populations = pd.read_csv('nst-est2019-alldata.csv', usecols=['NAME', 'POPESTIMATE2019'])

# Мерж данных по населению; пересчет на 100 тыс.
df = pd.merge(df, populations, how = 'left', left_on = 'state', right_on = 'NAME')
df['rate'] = df['cases'] / df['POPESTIMATE2019'] * 100000

# Отбор штатов
df_today = df[df['date'] == '2020-04-16']
topfivestates_rate = list(df_today.sort_values(by='rate', ascending=False).head()['state'])
topfivestates_rate.append('California')
topfivestates_rate.append('Washington')

# Фильтрация датасета
df = df[df['state'].isin(topfivestates_rate)]
df = df[df['date'] >= '2020-03-01']
df = df.pivot(index = 'date', columns = 'state', values = 'rate')

# Подготовка данных к отображению
df = df.reset_index()
df = df.reset_index(drop=True)
df = df.drop(columns = 'date')

# Построение графиков
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
    fig.savefig(f"pngs/{i}.png")

# Генерация GIF
gif_name = 'COVID'
fps = 6
file_list = glob.glob('pngs/*')
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('{}.gif'.format(gif_name), fps=fps)

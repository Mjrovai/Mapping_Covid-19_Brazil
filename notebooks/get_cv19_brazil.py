'''
# Covid19 - Brazil (Cities) Basic Geographic Analysis
- by Marcelo Rovai
- 27 April 2020

Datasets:
1. Worldometers Daily Data: https://www.worldometers.info/coronavirus/

2. Confirmed cases by day, using information from the news. Covid19br dataset is available at GitHub: https://github.com/wcota/covid19br, 

- Raw data by city compiled from original dataset provided by Brasil.IO (https://brasil.io/dataset/covid19/caso/).

Thanks to: 
- Wesley Cota (https://wesleycota.com), PhD candidate - Complex Networks/Physics (Universidade Federal de Viçosa - Brazil and Universidad de Zaragoza - Spain) 
- Alvaro Justen(https://blog.brasil.io/author/alvaro-justen.html) from Brasil.IO

License: Creative Commons Attribution-ShareAlike 4.0 International
(CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/)

More information: 
- https://wcota.me/covid19br and 
- https://brasil.io/covid19/

run script:
$ python get_cv19_brazil.py

'''

## Main Libraries and setup
print ('\n[INFO] Starting Covid19 - Brazil (Cities) Basic Geographic Analysis - WAIT')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly
import plotly.graph_objs as go
import geopandas as gpd
from shapely.geometry import Point, Polygon
from unicodedata import normalize
from PIL import Image
import imageio
import bar_chart_race as bcr

# Functions used on Brazil Covid-19 Geo Mepping Analysis
from cv_util_func import *

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.float_format', lambda x: '%.f' % x)
pd.options.display.float_format = '{:,}'.format
mpl.rcParams['figure.dpi']= 150
plt.style.use('seaborn-paper')

## definitions
capital_cities = ['Belém/PA', 
'Fortaleza/CE',
'Recife/PE',
'Manaus/AM',
'Rio de Janeiro/RJ',
'São Luís/MA',
'São Paulo/SP',
'Maceió/AL',
'Rio Branco/AC',
'Vitória/ES',
'Macapá/AP',
'Boa Vista/RR',
'Porto Velho/RO',
'João Pessoa/PB',
'Salvador/BA',
'Natal/RN',
'Teresina/PI',
'Aracaju/SE',
'Brasília/DF',
'Goiânia/GO',
'Porto Alegre/RS',
'Cuiabá/MT',
'Curitiba/PR',
'Palmas/TO',
'Belo Horizonte/MG',
'Florianópolis/SC',
'Campo Grande/MS']

## Datasets
print ('\n[INFO] Retriving Covid-19 Brazil Info - WAIT')
today = datetime.datetime.today()

# Plot WM Table
worldmetersLink = "https://www.worldometers.info/coronavirus/"
plot_wm_table('World', worldmetersLink, show=False, save=True)
plot_wm_table('South America', worldmetersLink, show=False, save=True)
plot_wm_table('Brazil', worldmetersLink, show=False, save=True)

# Covid19 - Number of total cases by city & State

dt, dt_st, dt_tm, dt_tm_city, dt_state, total_cases, deaths, cfr = get_brazil_cv_data(
    today)

# Plot State Table

dt_st = dt_st.fillna(0)
dt_st['recovered'] = dt_st['recovered'].astype('int64')
dt_st['suspects'] = dt_st['suspects'].astype('int64')
dt_st['tests'] = dt_st['tests'].astype('int64')

date_today = list(dt_st.date[-2:-1])[0]
dt_st_today = dt_st[dt_st.date == date_today]

dx = dt_st_today.sort_values('deaths', ascending=False)
plot_table(dx, show=False, save=True)


# Timeline of Brazil Total cases cases
print ('\n[INFO] Plotting Covid-19 Brazil cases')

plot_cases(dt_tm, 'TOTAL', y_scale='linear', n_0=1_000)
plot_cases(dt_tm, 'TOTAL', y_scale='log', n_0=1_000)


# Timeline of cases per top-cities

top_cities = list(dt.sort_values('totalCases', ascending=False)[:10].city)
for city in top_cities:
    plot_cases(dt_tm, city, y_scale='linear', n_0=100)
    plot_cases(dt_tm, city, y_scale='log', n_0=100) 

    
# Timeline New Deaths versus Previus Week    
plot_mov_ave_deaths_last_week(dt_tm, 'TOTAL', y_scale='linear', n_0=100, mov=7, show=False, save=True)   

for city in top_cities:
    tst = plot_mov_ave_deaths_last_week_2(dt_tm, city, y_scale='linear', n_0=1, mov=7, show=False, save=True)
    
# special graphics

# Recife
tst = plot_mov_ave_deaths_last_week_2(dt_tm,
                                    'Recife/PE',
                                    y_scale='linear',
                                    n_0=3,
                                    mov=7,
                                    graph='line',
                                    show=False,
                                    save=True,
                                    rect=True, 
                                    x0='2020-05-16',
                                    x1='2020-05-31',
                                    text="Lock-Down")

# Fortaleza
tst = plot_mov_ave_deaths_last_week_2(dt_tm,
                                    'Fortaleza/CE',
                                    y_scale='linear',
                                    n_0=3,
                                    mov=7,
                                    graph='line',
                                    show=False,
                                    save=True,
                                    rect=True, 
                                    x0='2020-05-07',
                                    x1='2020-05-31',
                                    text="Lock-Down")
    

# Sampa
tst = plot_mov_ave_deaths_last_week_2(dt_tm,
                                    'São Paulo/SP',
                                    y_scale='linear',
                                    n_0=3,
                                    mov=7,
                                    graph='line',
                                    show=False,
                                    save=True,
                                    rect=True, 
                                    x0='2020-05-20',
                                    x1='2020-05-25',
                                    text="Holidays")
    
      
# GeoData (Brasil & Municipalities)
print ('\n[INFO] Getting Brazilian Geodata\n') 

br_shp, br_cities = load_geodata()

# Mapping CoronaVirus data
print ('\n[INFO] Mapping Covid-19 Brazil cases - WAIT \n')

# Plot State Maps
state = dt_st_today.copy()
state.rename(columns={'state':'UF'}, inplace = True)

state = pd.merge(br_shp, state, on='UF')

plot_state_map(state, 'deaths')
plot_state_map(state, 'totalCases')
plot_state_map(state, 'deaths_per_100k_inhabitants')
plot_state_map(state, 'tests_per_100k_inhabitants')



# Nationwide Analysis
date = datetime.datetime.today()
cv_city, deaths_city, cv_city_pnt, deaths_city_pnt, total_cases, deaths, cfr, number_cities_cases, number_cities_deaths = get_Brazil_data(dt, br_shp, br_cities)

perc_cases = round((number_cities_cases/5570)*100, 0)
perc_deaths = round((number_cities_deaths/5570)*100, 0)

geo = [
    'Total number of Cases', 'Total number of Deaths', 'CFR [%]',
    'Total number of Brazil cities', 'Number of Identified cities with cases',
    'Brazilian cities with cases [%]',
    'Number of Identified cities with deaths',
    'Brazilian cities with deaths [%]'
]
data_geo = [
    total_cases, deaths, cfr, 5570, number_cities_cases, perc_cases,
    number_cities_deaths, perc_deaths
]

plot_geo_table(today, geo, data_geo, show=False, save=True)

plt_Brasil_cities(cv_city, deaths_city, date, total_cases, deaths, cfr, br_shp, br_cities, deaths_only=False)
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, n=1)
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, metrics='deaths', n=4)

# Other Pandemic metrics maps
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, metrics='TotalCases/1M pop', n=0.1 )
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, metrics='Deaths/1M pop', n=1 )
plt_Brasil_cv_metrics(cv_city_pnt, deaths_city_pnt, date, total_cases, deaths, cfr, br_shp, br_cities, metrics='CFR[%]', n=5)


# Selected State Analysis
print ('\n[INFO] Mapping Covid-19 Brazil state cases - WAIT \n')

cv_sp, deaths_sp, sp_total_cases, sp_deaths = get_state_info(cv_city, dt_state, br_shp, br_cities, 'SP')
cv_rj, deaths_rj, rj_total_cases, rj_deaths = get_state_info(cv_city, dt_state, br_shp, br_cities, 'RJ')
cv_mg, deaths_mg, mg_total_cases, mg_deaths = get_state_info(cv_city, dt_state, br_shp, br_cities, 'MG')
cv_ce, deaths_ce, ce_total_cases, ce_deaths = get_state_info(cv_city, dt_state, br_shp, br_cities, 'CE')

     
# Creating Gifs
print ('\n[INFO] Creating GIFs - WAIT ', end =" ")  

cv_city_t = pd.merge(br_cities, dt_tm_city, on='COD. IBGE')
deaths_city_t = cv_city_t.loc[cv_city_t['deaths'] != 0].copy()
dates = list(set(cv_city_t.date))
dates.sort()
dates = dates[-60:] 

create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'BR') ; print ('.', end =" ") 
create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'SP'); print ('.', end =" ") 
create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'RJ'); print ('.', end =" ") 
create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'MG'); print ('.', end =" ") 
create_state_gif(dates, cv_city_t, deaths_city_t, br_shp, 'CE'); print ('.')


### Creating videos from Gifs
print ('\n[INFO] Creating Movies - WAIT ', end =" ") 

conv_gif_to_mp4('BR', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('SP', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('RJ', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('MG', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('CE', fps=5); print ('.') 


dead_city = get_dataframe(df=dt_tm,
                          cities=top_cities,
                          feature='deaths_per_100k_inhabitants',
                          rnd=0,
                          in_data='2020-03-20')

bcr.bar_chart_race(dead_city, 
                   title='Brazil Top Cities with COVID-19 cases - Deaths per 100K inhabitants',
                  filename='../videos/top_cities_deaths_100K.mp4')



dead_capital = get_dataframe(df=dt_tm,
                          cities=capital_cities,
                          feature='deaths_per_100k_inhabitants',
                          rnd=0,
                          in_data='2020-03-20')

bcr.bar_chart_race(dead_capital, 
                   title='Brazil Capital Cities - COVID-19 - Deaths per 100K inhabitants',
                  filename='../videos/capital_cities_deaths_100K.mp4')



print ('\n[INFO] End script MJRoBot.org @ {}\n'.format(today)) 


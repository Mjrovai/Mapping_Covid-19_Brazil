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

# Functions used on Brazil Covid-19 Geo Mepping Analysis
from cv_util_func import *

import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.float_format', lambda x: '%.f' % x)
pd.options.display.float_format = '{:,}'.format
mpl.rcParams['figure.dpi']= 150
plt.style.use('seaborn-paper')



### Creating videos from Gifs
print ('\n[INFO] Creating Movies - WAIT ', end =" ") 

conv_gif_to_mp4('BR', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('SP', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('RJ', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('MG', fps=5); print ('.', end =" ") 
conv_gif_to_mp4('CE', fps=5); print ('.') 

print ('\n[INFO] End script MJRoBot.org @ {}\n'.format(today)) 




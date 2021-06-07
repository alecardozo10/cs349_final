import sys
sys.path.insert(0, '..')

from utils import data
import os
import sklearn
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
#%matplotlib inline
plt.style.use('fivethirtyeight')

def print_dict(dictio):
    for key, value in dictio.items():
        print(key, ' : ', value)

def n_data():
    path = os.path.join('results', 'raw_jsons', 'knn_raw_{}.json'.format())
    file = open(path,)
    data = json.load(file)
    return data

most_pop = ['China', 'India', 'US', 'Indonesia', 'Pakistan', 'Nigeria', 'Brazil', 'Bangladesh', 'Russia', 'Mexico']
x_axis = np.array([i for i in range(498)]).astype('float')

# ------------ HYPERPARAMETERS -------------
BASE_PATH = '../COVID-19/csse_covid_19_data/'
MIN_CASES = 1000
# ------------------------------------------

confirmed = os.path.join(
    BASE_PATH, 
    'csse_covid_19_time_series',
    'time_series_covid19_confirmed_global.csv')
confirmed = data.load_csv_data(confirmed)
features = []
targets = []

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(111)
cm = plt.get_cmap('jet')
NUM_COLORS = 0
LINE_STYLES = ['solid']#, 'dashed', 'dotted']
NUM_STYLES = len(LINE_STYLES)

for val in np.unique(confirmed["Country/Region"]):
    if val in most_pop:
        df = data.filter_by_attribute(
            confirmed, "Country/Region", val)
        cases, labels = data.get_cases_chronologically(df)
        cases = cases.sum(axis=0)

        if cases.sum() > MIN_CASES:
            NUM_COLORS += 1

colors = [cm(i) for i in np.linspace(0, 1, NUM_COLORS)]
legend = []
handles = []

for val in np.unique(confirmed["Country/Region"]):
    if val in most_pop:
        df = data.filter_by_attribute(
            confirmed, "Country/Region", val)
        cases, labels = data.get_cases_chronologically(df)
        #print('cases = ', type(cases), '\n', cases, '\n', cases.shape, '\n')
        #print('labels = ', type(labels), '\n', labels, '\n')
        #print('x = ', x_axis)
        cases = cases.sum(axis=0)

        if cases.sum() > MIN_CASES:
            i = len(legend)
            lines = ax.plot(cases, label=labels[0,1])
            handles.append(lines[0])
            lines[0].set_linestyle(LINE_STYLES[i%NUM_STYLES])
            lines[0].set_color(colors[i])
            legend.append(labels[0, 1])

            y = cases.copy().astype('float')
            #print('y = ', '\n', y, '\n')
            m, b = np.polyfit(x_axis, y, 1)
            plt.plot(x_axis, m*x_axis + b, label='{} line of best fit'.format(labels[0, 1]), linestyle='dotted', color=colors[i])
            

ax.set_ylabel('# of confirmed cases')
ax.set_xlabel("Time (days since Jan 22, 2020)")

ax.set_yscale('log')
ax.legend(handles, legend, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4)
plt.tight_layout()
plt.title("Lines of Best Fit for Number of Confirmed Cases in \n Top 10 Most Populated Countries")
plt.legend(loc="lower right", fontsize=8)#, bbox_to_anchor=(0.5, -0.3))
#plt.show()
plt.savefig('results/lines_of_best_fit_top_10_pop.png')
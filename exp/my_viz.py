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

def knn_raw_func():
    n_neighbors = [5,10,15,20]

    def n_data(n):
        path = os.path.join('results', 'raw_jsons', 'knn_raw_{}.json'.format(n))
        file = open(path,)
        data = json.load(file)
        return data

    master_dict = {5: {}, 10: {}, 15: {}, 20: {}}
    dat = n_data(5)
    countries =[i for i in dat.keys()]

    for n in n_neighbors:
        master_dict[n] = {}
        for c in countries:
            master_dict[n][c] = {'minkowski': 0, 'manhattan': 0}

    # dict keys:
        # 1. n neighbors
        # 2. country
        # 3. minkowski, manhattan => numbers

    for n in n_neighbors:
        data = n_data(n)
        for c in data.keys():
            mink_country = data[c]['minkowski'][0]
            manh_country = data[c]['manhattan'][0]
            master_dict[n][mink_country]['minkowski'] += 1
            master_dict[n][manh_country]['manhattan'] += 1
        #print('n = {} France: '.format(n), master_dict[n]['France']['minkowski'])

    relevant_countries = []
    for n in n_neighbors:
        for c in countries:
            if master_dict[n][c]['minkowski'] != 0 or master_dict[n][c]['manhattan'] != 0:
                if c not in relevant_countries:
                    relevant_countries.append(c)
    relevant = sorted(relevant_countries)

    relevant_data_dict = {5: [], 10: [], 15: [], 20: []}
    for n in n_neighbors:
        relevant_data_n = {r:master_dict[n][r] for r in relevant_countries}
        #relevant_data_n = sorted(relevant_data_n)
        lst = []
        for i in relevant_data_n.keys():
            lst.append((i, relevant_data_n[i]['minkowski'], relevant_data_n[i]['manhattan']))
        relevant_data_dict[n] = lst

    for n in [5,10,15,20]:
        rel_countries = []
        minkowski = []
        manhattan = []

        for i in range(len(relevant_data_dict[n])):
            rel_countries.append(relevant_data_dict[n][i][0])
            minkowski.append(relevant_data_dict[n][i][1])
            manhattan.append(relevant_data_dict[n][i][2])
            
        #rd = relevant_data_dict[n].T

        fig = plt.subplots()
        barWidth = 0.5

        br1 = [i for i in range(len(rel_countries))]
        br2 = [x + barWidth for x in br1]

        plt.bar(br1, list(minkowski), color='r', width=barWidth, edgecolor ='grey', label='Minkowski')
        plt.bar(br2, list(manhattan), color='b', width=barWidth, edgecolor ='grey', label='Manhattan')
        plt.title('Number of Countries that Find a Given Country to be \n Most Similar Using {} Neighbors, knn_raw'.format(n))
        plt.xlabel('Country')
        plt.ylabel('Number of Countries that have a \n Given Country as Most Similar')
        plt.xticks([r + (barWidth/2) for r in range(len(rel_countries))], rel_countries, rotation=90, fontsize=8)
        
        plt.savefig('results/raw_jsons/knn_raw_{}_pic.png'.format(n), bbox_inches='tight')
        #plt.legend()
        #plt.show()

def knn_diff_func():
    n_neighbors = [5,10,15,20]

    def n_data(n):
        path = os.path.join('results', 'diff_jsons', 'knn_diff_{}.json'.format(n))
        file = open(path,)
        data = json.load(file)
        return data

    master_dict = {5: {}, 10: {}, 15: {}, 20: {}}
    dat = n_data(5)
    countries =[i for i in dat.keys()]

    for n in n_neighbors:
        master_dict[n] = {}
        for c in countries:
            master_dict[n][c] = {'minkowski': 0, 'manhattan': 0}

    # dict keys:
        # 1. n neighbors
        # 2. country
        # 3. minkowski, manhattan => numbers

    for n in n_neighbors:
        data = n_data(n)
        for c in data.keys():
            mink_country = data[c]['minkowski'][0]
            manh_country = data[c]['manhattan'][0]
            master_dict[n][mink_country]['minkowski'] += 1
            master_dict[n][manh_country]['manhattan'] += 1
        #print('n = {} France: '.format(n), master_dict[n]['France']['minkowski'])

    relevant_countries = []
    for n in n_neighbors:
        for c in countries:
            if master_dict[n][c]['minkowski'] != 0 or master_dict[n][c]['manhattan'] != 0:
                if c not in relevant_countries:
                    relevant_countries.append(c)
    relevant = sorted(relevant_countries)


    relevant_data_dict = {5: [], 10: [], 15: [], 20: []}
    for n in n_neighbors:
        relevant_data_n = {r:master_dict[n][r] for r in relevant_countries}
        #relevant_data_n = sorted(relevant_data_n)
        lst = []
        for i in relevant_data_n.keys():
            lst.append((i, relevant_data_n[i]['minkowski'], relevant_data_n[i]['manhattan']))
        relevant_data_dict[n] = lst

    for n in [5,10,15,20]:
        rel_countries = []
        minkowski = []
        manhattan = []

        for i in range(len(relevant_data_dict[n])):
            rel_countries.append(relevant_data_dict[n][i][0])
            minkowski.append(relevant_data_dict[n][i][1])
            manhattan.append(relevant_data_dict[n][i][2])
            
        #rd = relevant_data_dict[n].T

        fig = plt.subplots()
        barWidth = 0.5

        br1 = [i for i in range(len(rel_countries))]
        br2 = [x + barWidth for x in br1]

        plt.bar(br1, list(minkowski), color='r', width=barWidth, edgecolor ='grey', label='Minkowski')
        plt.bar(br2, list(manhattan), color='b', width=barWidth, edgecolor ='grey', label='Manhattan')
        plt.title('Number of Countries that Find a Given Country to be \n Most Similar Using {} Neighbors, knn_diff'.format(n))
        plt.xlabel('Country')
        plt.ylabel('Number of Countries that have a \n Given Country as Most Similar')
        plt.xticks([r + (barWidth/2) for r in range(len(rel_countries))], rel_countries, rotation=90, fontsize=8)
        
        plt.savefig('results/diff_jsons/knn_diff_{}_pic.png'.format(n), bbox_inches='tight')
        #plt.legend()
        #plt.show()

knn_raw_func()
knn_diff_func()


# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 14:44:24 2023

@author: Yun Ni

This program is to genarate graphs.
"""

import json
from pyecharts import options as opts
from pyecharts.charts import Graph
import os
from wordcloud import WordCloud
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from imageio import imread

mpl.rcParams['font.sans-serif'] = ['SimHei'] # 支持中文显示

nodes = []
links = []
categories = []
V = []
ver = {}
dep = {}
max_dep = {}
deg = {}

def generate_graph():
    c = (
        Graph()
        .add(
            '',
            nodes,
            links,
            categories,
            repulsion = 50,
            linestyle_opts = opts.LineStyleOpts(curve = 0.2),
            label_opts = opts.LabelOpts(is_show = False),
        )
        .set_global_opts(
            legend_opts = opts.LegendOpts(is_show = False),
            title_opts = opts.TitleOpts(title = f'ACM Digital Library 论文引用网络 (N = {str(len(nodes))})'),
        )
        .render(f'../result/Citation Network (N = {str(len(nodes))}).html')
    )

def generate_worldcloud():
    wordlist = []
    for x in nodes:
        title = x['name'].split(' - ')[0]
        words = title.split()
        wordlist += words
    freq = {}
    stopwords = ['a', 'an', 'by', 'through', 'when', 'as', 'if', 'while', 'for', 'the', 'in', 'on', 'under', 'and', 'or', 'not', 'of', 'out', 'with', 'using', 'from', 'via', 'case', 'towards', 'to', 'systems', 'analysis']
    for word in wordlist:
        if word.lower() not in stopwords:
            freq[word.lower()] = freq.get(word.lower(), 0) + 1
    
    wc = WordCloud(
        width = 10000,
        height = 10000,
        font_path = 'msyh.ttc',
        background_color = 'rgba(0, 0, 0, 0)',
        mask = imread('../data/mask.png'),
        colormap = 'Pastel2',
        max_words = 10000
    )
    wc.generate_from_frequencies(freq)
    wc.to_file('../result/word cloud.png')

def process_graph():
    for x in nodes:
        title = x['name']
        V.append(title)
    for y in links:
        u = y['target']
        v = y['source']
        ver[u] = ver.get(u, []) + [v]

def calculate_depth():
    for x in V:
        if not dep.get(x):
            dep[x] = 0
        if ver.get(x):
            for y in ver[x]:
                dep[y] = max(dep.get(y, 0), dep[x] + 1)
    for x in V:
        max_dep[dep[x]] = max_dep.get(dep[x], 0) + 1

def calculate_degree():
    for x in V:
        if ver.get(x):
            deg[len(ver[x])] = deg.get(len(ver[x]), 0) + 1

def handle(ws):
    global V, ver, dep, max_dep, deg
    V = []
    ver = {}
    dep = {}
    max_dep = {}
    deg = {}
    
    with open(f'../data/{ws}/data.json', 'r', encoding = 'utf-8') as f:
        j = json.load(f)
        global nodes, links, categories
        nodes, links, categories = j
        
    process_graph()
    calculate_depth()
    calculate_degree()
    
    return max_dep, deg

if __name__ == '__main__':
    if not os.path.exists('../result'):
        os.mkdir('../result')
    
    with open('../data/lab_1/data.json', 'r', encoding = 'utf-8') as f:
        j = json.load(f)
        nodes, links, categories = j
    #generate_graph()
    generate_worldcloud()
    
    '''
    dep1, deg1 = handle('lab_8')
    dep2, deg2 = handle('lab_9')
    dep3, deg3 = handle('lab_10')
    dep4, deg4 = handle('lab_11')
    '''
    '''
    s = set(list(dep1.keys())) | set(list(dep2.keys())) | set(list(dep3.keys())) | set(list(dep4.keys()))
    ind = np.arange(max(s) + 1)
    for i in ind:
        if not dep1.get(i):
            dep1[i] = 0
        if not dep2.get(i):
            dep2[i] = 0
        if not dep3.get(i):
            dep3[i] = 0
        if not dep4.get(i):
            dep4[i] = 0
    val1 = [x[1] for x in sorted(dep1.items())]
    val2 = [x[1] for x in sorted(dep2.items())]
    val3 = [x[1] for x in sorted(dep3.items())]
    val4 = [x[1] for x in sorted(dep4.items())]
    plt.bar(ind - 0.3, dep1.values(), width = 0.2, label = 'recent 5 years')
    plt.bar(ind - 0.1, dep2.values(), width = 0.2, label = 'recent 6 years')
    plt.bar(ind + 0.1, dep3.values(), width = 0.2, label = 'recent 7 years')
    plt.bar(ind + 0.3, dep4.values(), width = 0.2, label = 'recent 8 years')
    plt.style.use('ggplot')
    plt.legend(loc = 'best')
    plt.title('引用链长度分布统计图')
    plt.savefig('../result/depth.png')
    '''
    '''
    s = set(list(deg1.keys())) | set(list(deg2.keys())) | set(list(deg3.keys())) | set(list(deg4.keys()))
    ind = np.arange(max(s) + 1)
    for i in ind:
        if not deg1.get(i):
            deg1[i] = 0
        if not deg2.get(i):
            deg2[i] = 0
        if not deg3.get(i):
            deg3[i] = 0
        if not deg4.get(i):
            deg4[i] = 0
    val1 = [x[1] for x in sorted(deg1.items())]
    val2 = [x[1] for x in sorted(deg2.items())]
    val3 = [x[1] for x in sorted(deg3.items())]
    val4 = [x[1] for x in sorted(deg4.items())]
    plt.plot(ind, val1, label = 'recent 5 years')
    plt.plot(ind, val2, label = 'recent 6 years')
    plt.plot(ind, val3, label = 'recent 7 years')
    plt.plot(ind, val4, label = 'recent 8 years')
    plt.style.use('ggplot')
    plt.legend(loc = 'best')
    plt.title('节点度数分布曲线')
    plt.savefig('../result/degree.png')
    '''
    
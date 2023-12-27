# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 14:09:56 2023

@author: Yun Ni

This program is to request data from online.
"""


'''
Packages
'''
import requests
import re
import json
import math
import time
from queue import Queue
from datetime import datetime
import os


'''
Links to help requesting
'''
headers1 = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'}
headers2 = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
headers = headers1
search_page_l1 = 'https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&SeriesKeyAnd=sigcomm-ccr&EpubDate=%5B20181218+TO+20231218%5D&sortBy=cited&startPage='
search_page_r1 = '&pageSize=50'
# Journal of the ACM
search_page_l2 = 'https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&SeriesKeyAnd=jacm&sortBy=cited&startPage='
search_page_r2 = '&pageSize=50'
# 2019 - 2023
search_page_l3 = 'https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&SeriesKeyAnd=jacm&EpubDate=%5B20181225+TO+20231225%5D&sortBy=cited&startPage='
search_page_r3 = '&pageSize=50'
# 2018
search_page_l4 = 'https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&SeriesKeyAnd=jacm&AfterYear=2018&BeforeYear=2018&sortBy=cited&startPage='
search_page_r4 = '&pageSize=50'
# 2017
search_page_l5 = 'https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&SeriesKeyAnd=jacm&AfterYear=2017&BeforeYear=2017&sortBy=cited&startPage='
search_page_r5 = '&pageSize=50'
# 2016
search_page_l6 = 'https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&SeriesKeyAnd=jacm&AfterYear=2016&BeforeYear=2016&sortBy=cited&startPage='
search_page_r6 = '&pageSize=50'
# 2015
search_page_l7 = 'https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&field1=AllField&SeriesKeyAnd=jacm&AfterYear=2015&BeforeYear=2015&sortBy=cited&startPage='
search_page_r7 = '&pageSize=50'
search_page_l = search_page_l7
search_page_r = search_page_r7
info_head = 'https://dl.acm.org/doi/'
cite_head = 'https://dl.acm.org/action/ajaxShowCitedBy?doi='
workspace = 'main'


'''
Regular expressions
'''
search_regex = '<h5 class="issue-item__title"><span class="hlFld-Title"><a.*?>(.*?)</a></span></h5><ul class="rlist--inline loa truncate-list" aria-label="authors" data-lines="[0-9](.*?)</ul>.*?">.*?href="https://doi.org/(.*?)"'
search_author_regex = '<a href="/profile/[0-9].*?" title="(.*?)">'
cite_regex = '<li id="[0-9a-z]*?" class="references__item">(.*?)</li>'
cite_title_regex = '<span class="references__article-title">(.*?)</span>'
cite_author_regex = '<a href="/author/.*?">(.*?)</a>'
cite_doi_regex = '<a href="https://doi.org/(.*?)" class="link" target="_blank">'
count_regex = '<div class="citation">Total Citations<span class="bold">([0-9,]*?)</span></div>'
block_regex = '<title>ACM Error: IP blocked</title>'


'''
Data structures
'''
q = Queue()
nodes = []
links = []
categories = [{'name': str(i)} for i in range(8)]
vis = set()
category_convert = [7, 0, 4, 5, 1, 2, 6, 3]
maxn = 1000000
flg = False
timestamp = time.time()


'''
Functions
'''
def Log(*args):
    '''
    Write information in terminal and log
    '''
    print(*args)
    with open(f'../data/{workspace}/log/run.log', 'a', encoding = 'utf-8') as f:
        f.writelines(args)
        f.writelines('\n')

def init():
    '''
    Initialize files
    '''
    if not os.path.exists(f'../data/{workspace}'):
        os.mkdir(f'../data/{workspace}')
    if not os.path.exists(f'../data/{workspace}/run'):
        os.mkdir(f'../data/{workspace}/run')
    if not os.path.exists(f'../data/{workspace}/log'):
        os.mkdir(f'../data/{workspace}/log')
    if not os.path.exists(f'../data/{workspace}/save'):
        os.mkdir(f'../data/{workspace}/save')
    
    if os.path.exists(f'../data/{workspace}/run/vis.txt'):
        with open(f'../data/{workspace}/run/vis.txt', 'r', encoding = 'utf-8') as f:
            for s in f:
                vis.add(s[:-1])
    if os.path.exists(f'../data/{workspace}/run/queue.txt'):
        with open(f'../data/{workspace}/run/queue.txt', 'r', encoding = 'utf-8') as f:
            for s in f:
                q.put(eval(s))
    global nodes, links
    if os.path.exists(f'../data/{workspace}/data.json'):
        with open(f'../data/{workspace}/data.json', 'r', encoding = 'utf-8') as f:
            j = json.load(f)
            nodes, links, fw = j

def final():
    '''
    Finalize files
    '''
    if not flg:
        with open(f'../data/{workspace}/run/queue.txt', 'w', encoding = 'utf-8') as f, open(f'../data/{workspace}/save/queue_save{str(len(nodes))},{datetime.now().strftime("%a %b %d %Y, %H.%M")}.txt', 'w', encoding = 'utf-8') as f_save:
            while not q.empty():
                x = q.get()
                f.write(str(x) + '\n')
                f_save.write(str(x) + '\n')
                
    with open(f'../data/{workspace}/run/vis.txt', 'w', encoding = 'utf-8') as f, open(f'../data/{workspace}/save/vis_save{str(len(nodes))},{datetime.now().strftime("%a %b %d %Y, %H.%M")}.txt', 'w', encoding = 'utf-8') as f_save:
        for x in vis:
            f.writelines(x + '\n')
            f_save.writelines(x + '\n')
    with open(f'../data/{workspace}/data.json', 'w', encoding = 'utf-8') as f, open(f'../data/{workspace}/save/data_save{str(len(nodes))},{datetime.now().strftime("%a %b %d %Y, %H.%M")}.json', 'w', encoding = 'utf-8') as f_save:
        json.dump([nodes, links, categories], f, indent = 4)
        json.dump([nodes, links, categories], f_save)

def fetch(url, headers):
    '''
    Fetah a page from a given url
    '''
    i = 0
    while True:
        try:
            global timestamp
            while time.time() - timestamp < 1:
                time.sleep(0.01)
            timestamp = time.time()
            
            i += 1
            Log(f'Try fetching: {i}')
            Log('=======Haltable========')
            Log('------requesting-------')
            r = requests.get(url, headers = headers, timeout = 10)
            Log('--requesting finished--')
            Log('----matching block-----')
            res = re.findall(re.compile(block_regex), r.text)
            Log('---matching finished---')
            while len(res):
                Log('Blocked')
                for i in range(300):
                    time.sleep(1)
                if headers == headers1:
                    headers = headers2
                else:
                    headers = headers1
                res = re.findall(re.compile(block_regex), r.text)
            Log('======Unhaltable=======')
            return r
        except KeyboardInterrupt:
            return -1
        except:
            Log('Fetch fails')
            continue

def cited_count(doi):
    '''
    Get the total citation number of a paper
    '''
    Log('[Fetch zero]')
    r = fetch(info_head + doi, headers)
    if r == -1:
        return -1
    Log('-----matching zero-----')
    res = re.findall(re.compile(count_regex), r.text)
    Log('---matching finished---')
    r.close()
    if len(res) == 0:
        return 0
    else:
        return int(res[0].replace(',', ''))

def add_node(title, size):
    '''
    Add a node (paper) into the network
    '''
    node = {
        'name': title,
        'symbolSize': math.log(size + 2) * 5,
        'value': size,
        'category': category_convert[int(math.log(size + 2))]
        }
    nodes.append(node)

def add_link(source, target):
    '''
    Add a link (citation relationship) into the network
    '''
    link = {
        'source': source,
        'target': target
        }
    links.append(link)

def recover(doi, title, par):
    '''
    Save current scene when halted
    '''
    with open(f'../data/{workspace}/run/queue.txt', 'w', encoding = 'utf-8') as f, open(f'../data/{workspace}/save/queue_save{str(len(nodes))},{datetime.now().strftime("%a %b %d %Y, %H.%M")}.txt', 'w', encoding = 'utf-8') as f_save:
        f.write(str((doi, title, par)) + '\n')
        f_save.write(str((doi, title, par)) + '\n')
        while not q.empty():
            x = q.get()
            f.write(str(x) + '\n')
            f_save.write(str(x) + '\n')

def search(l, r):
    '''
    Search papers from page l to page r as anchors for bfs
    '''
    for i in range(l - 1, r):
        r = fetch(search_page_l + str(i) + search_page_r, headers)
        res = re.findall(re.compile(search_regex), r.text)
        r.close()
        for title, author_all, doi in res:
            authors = re.findall(re.compile(search_author_regex), author_all)
            q.put((doi, title + ' - ' + ', '.join(authors), None))

def bfs():
    '''
    Search all citations
    '''
    while not q.empty():
        if len(nodes) == maxn:
            Log('Enough')
            return 0
        else:
            Log(f'n = {len(nodes)}')
            Log(f'link number = {len(links)}')
            Log(f'queue length = {q.qsize()}')
            Log(f'vis number = {len(vis)}')
        
            doi, title, par = q.get()
            Log('\n', doi, title)
            
            if title in vis: # node already added, only need to add link
                Log('Visited')
                if (par != None):
                    add_link(title, par)
            else:
                cite_cnt = cited_count(doi)
                if cite_cnt == -1: # fetch fails, recover and halt
                    Log('Halt\n')
                    recover(doi, title, par)
                    return -1
                else:
                    Log('Citation = {}'.format(cite_cnt))
                    
                    if cite_cnt == 0: # no citations, add node and its link to par, then skip
                        add_node(title, 0)
                        if par != None:
                            add_link(title, par)
                    else: # add node and link, then search its children
                        Log('[Fetch citations]')
                        r = fetch(cite_head + doi, headers)
                        if r == -1: # fetch fails, recover and halt
                            Log('Halt\n')
                            recover(doi, title, par)
                            return -1
                        else:
                            Log('---matching citation---')
                            res = re.findall(re.compile(cite_regex), r.text)
                            Log('---matching finished---')
                            r.close()
                            
                            valid_cite_cnt = 0
                            Log('----matching detail----')
                            for x in res:
                                child_title = re.findall(re.compile(cite_title_regex), x)
                                child_authors = re.findall(re.compile(cite_author_regex), x)
                                child_doi = re.findall(re.compile(cite_doi_regex), x)
                                if len(child_title) == 1 and len(child_authors) != 0 and len(child_doi) == 1:
                                    q.put((child_doi[0], child_title[0] + ' - ' + ', '.join(child_authors), title))
                                    valid_cite_cnt += 1
                            Log('---matching finished---')
                            Log('Valid citation = {}'.format(valid_cite_cnt))
                            
                            add_node(title, valid_cite_cnt)
                            if par != None:
                                add_link(title, par)
                vis.add(title)
    return 0


'''
Main module
'''
if __name__ == '__main__':
    init()
    '''
    search(1, 1)
    '''
    '''
    if bfs() == -1:
        flg = True
    
    if not flg:
        if not os.path.exists(f'../data/{workspace}/run/number.txt'):
            start = 0
        else:
            with open(f'../data/{workspace}/run/number.txt', 'r', encoding = 'utf-8') as f:
                start = eval(f.readline())
        with open(f'../data/{workspace}/run/anchor.txt', 'r', encoding = 'utf-8') as f:
            anchors = f.readlines()
        for i in range(start, len(anchors)):
            Log(f'Anchor {i} begin')
            q.put(eval(anchors[i]))
            if bfs() == -1:
                flg = True
                with open(f'../data/{workspace}/run/number.txt', 'w', encoding = 'utf-8') as f:
                    f.writelines(str(i + 1) + '\n')
                break
            Log(f'Anchor {i} over')
            with open(f'../data/{workspace}/run/number.txt', 'w', encoding = 'utf-8') as f:
                f.writelines(str(i + 1) + '\n')
    '''
    final()

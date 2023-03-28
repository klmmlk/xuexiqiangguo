#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Jiong.L
@time: 2023/3/28 23:18
"""
from bs4 import BeautifulSoup as bs
from requests import get
import difflib
import re


def get_anser(key):
    matches = re.findall(r"([\u4E00-\uFA20]{3,})", key)
    response = get(f'http://www.syiban.com/search/index/init.html?modelid=1&q={max(matches)}')
    response.encoding = 'utf-8'
    soup = bs(response.text, 'lxml')
    anser_node = soup.select(".yzm-news-right")
    anser_lists = [[], []]
    for i, each in enumerate(anser_node):
        qus = each.find('a').text
        anser = each.find('p').text
        anser_lists[0].append(qus)
        anser_lists[1].append(re.search(r"(?<=、)(.+)", anser).group())
    if not anser_lists[0]:
        return False
    similarity = []
    for each in anser_lists[0]:
        similarity.append(difflib.SequenceMatcher(None, key, each).ratio())
    print(similarity.index(max(similarity)))
    return anser_lists[1][similarity.index(max(similarity))]


if __name__ == '__main__':
    str1 = f'阿赛站额'
    str2 = f'补全唐代诗人杜牧《江南春绝句》诗句：南朝四百八十寺，（ ）。'
    print(get_anser(str1))

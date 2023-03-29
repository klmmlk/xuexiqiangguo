#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: Jiong.L
@time: 2023/3/28 23:18
"""
from bs4 import BeautifulSoup as bs
from requests import get
import re
from difflib import SequenceMatcher


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
        similarity.append(SequenceMatcher(None, key, each).ratio())
    print(similarity.index(max(similarity)))
    return anser_lists[1][similarity.index(max(similarity))]


def get_string_diff(qustion_text, tips_text):
    qustion_text = "".join(qustion_text.split())
    matcher = SequenceMatcher(None, qustion_text, tips_text)
    diff = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'insert':
            diff.append(tips_text[j1:j2])
    return diff


if __name__ == '__main__':
    str1 = f'公元前707年，郑庄公在         中取得胜利，称霸中原，史称“郑庄公小霸”，同时也揭开了春秋争霸的序幕。'
    str2 = f'公元前707年，郑庄公在繻（xū）葛之战中取得胜利，称霸中原，史称“郑庄公小霸”，同时也揭开了春秋争霸的序幕。'
    # print(get_anser(str2))
    print(get_string_diff(str1, str2))
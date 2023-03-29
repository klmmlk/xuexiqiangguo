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
    matches = re.findall(r"([\u4E00-\uFA20]{3,10})", key)
    print(max(matches))
    response = get(f'http://www.syiban.com/search/index/init.html?modelid=1&q={max(matches)}')
    response.encoding = 'utf-8'
    soup = bs(response.text, 'lxml')
    anser_node = soup.select(".yzm-news-right")
    anser_lists = [[], []]
    for i, each in enumerate(anser_node):
        qus = each.find('a').text
        anser = each.find('p').text
        anser_lists[0].append(qus)
        try:
            anser_lists[1].append(re.search(r"(?<=、)(.+)", anser).group())
        except:
            anser_lists[1].append(False)
    if not anser_lists[0]:
        return False
    similarity = []
    for each in anser_lists[0]:
        similarity.append(SequenceMatcher(None, key, each).ratio())
    print(anser_lists)
    return [anser_lists[1][similarity.index(max(similarity))]]


def get_string_diff(qustion_text, tips_text):
    qustion_text = "".join(qustion_text.split())
    matcher = SequenceMatcher(None, qustion_text, tips_text)
    diff = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'insert':
            diff.append(tips_text[j1:j2])
    return diff


if __name__ == '__main__':
    str1 = f'国家知识产权局商标局作出宣告注册商标无效的决定，应当书面通知当事人。当事人对商标局的决定不服的，可以自收到通知之日起         内向商标评审委员会申请复审。'
    str2 = f'《中华人民共和国商标法》第四十四条规定，商标局作出宣告注册商标无效的决定，应当书面通知当事人。当事人对商标局的决定不服的，可以自收到通知之日起十五日内向商标评审委员会申请复审。'
    print(get_anser(str1))
    # print(get_string_diff(str1, str2))
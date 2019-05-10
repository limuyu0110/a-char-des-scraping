# -*- coding:utf-8 _*-
""" 
@author:limuyu
@file: web_rel.py 
@time: 2019/05/10
@contact: limuyu0110@pku.edu.cn

"""

from bs4 import BeautifulSoup as soup
import urllib.request
from urllib.request import urlopen as ureq
import logging
import re
from utils import *
import codecs
import json

logger = logging.getLogger('main.web_rel')

proxy = "http://localhost:1080"
proxy_support = urllib.request.ProxyHandler({'http': proxy})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)


def get_soup_from_url(url):
    pgsoup = None
    try:
        uClient = ureq(url)
        pgsoup = soup(uClient, 'html.parser')
        uClient.close()
    except Exception:
        logger.info(F"Failed to get url: {url}")

    return pgsoup


def judge_soup_is_valid(url, pgsoup):
    # Blank Page
    if not pgsoup:
        logger.info(F"soup from url: {url} is blank")
        return False

    if 'ゲーム' in pgsoup.title:
        if_char_column = pgsoup.find(name='div', string=re.compile('キャラクター'))
        year = get_year(pgsoup)
        if not year or year < YEAR_AFTER:
            logger.info(F"soup from url: {url} is too early")
            return False
        if not if_char_column:
            logger.info(F"soup from url: {url} has no char column")
            return False

    return True


def get_src_and_desc(pgsoup):
    tit = pgsoup.find(name='div', string=re.compile('キャラクター'))
    table = tit.next_sibling.next_sibling
    descs = table.find_all(lambda x: x.name == 'td' and x.get('class') and 'chara-text' in x.get('class'))
    L = []
    for desc in descs:
        img = desc.previous_sibling.previous_sibling.img
        if img:
            img_src = img.get('src')
            L.append({'src': img_src, 'desc_raw': str(desc), 'desc_str': '\n'.join(desc.strings)})

    return L


def get_game_name(pgsoup):
    return pgsoup.title.string


def get_year(pgsoup):
    year = pgsoup.find(id='tooltip-day')
    if year:
        year = int(year.string.split('/')[0])
        return year
    return None


def process_one_url(url):
    pgsoup = get_soup_from_url(url)
    if judge_soup_is_valid(url, pgsoup):
        L = get_src_and_desc(pgsoup)
        fn = get_game_name(pgsoup) + '.json'
        with codecs.open(os.path.join(JSON_PATH, fn), 'w', 'utf8') as f:
            json.dump(L, f, ensure_ascii=False, indent=4)

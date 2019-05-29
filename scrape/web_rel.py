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
from http import cookiejar

logger = logging.getLogger('main.web_rel')

COOKIE_FILE = './raw_data/cookie.txt'
proxy = "http://localhost:1080"
proxy_support = urllib.request.ProxyHandler({'http': proxy})

cookie = cookiejar.MozillaCookieJar()
cookie.load(COOKIE_FILE)
cookie_support = urllib.request.HTTPCookieProcessor(cookie)

# opener = urllib.request.build_opener(proxy_support, cookie_support)
opener = urllib.request.build_opener(cookie_support)
opener.add_handler(proxy_support)

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
    if is_blank(pgsoup):
        logger.info(F"soup from url: {url} is blank")
        return False

    if 'ゲーム' in pgsoup.title.string:
        if_char_column = pgsoup.find(name='div', string=re.compile('キャラクター'))
        year = get_year(pgsoup)
        if not year or year < YEAR_AFTER:
            logger.info(F"soup from url: {url} is too early")
            return False
        if not if_char_column:
            logger.info(F"soup from url: {url} has no char column")
            return False

        return True

    return False


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


def is_blank(pgsoup):
    return not bool(pgsoup.title)


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
        fn = re.sub(r'[*\/:?"<>|]', '', fn)
        with codecs.open(os.path.join(JSON_PATH, fn), 'w', 'utf8') as f:
            json.dump(L, f, ensure_ascii=False, indent=4)

        logger.info(F"succeeded in url: {url}")


def next_page_url_in_search(pgsoup):
    return ROOT_URL + pgsoup.find('a', title='next page')['href']


def urls_in_one_search_page(pgsoup):
    tmp = list(filter(lambda x: not x.img, pgsoup.find_all('a', href=re.compile('soft.phtml'))))
    urls = [ROOT_URL + '/' + a['href'] for a in tmp]
    return urls

# -*- coding:utf-8 _*-
""" 
@author:limuyu
@file: dump_urls.py 
@time: 2019/05/10
@contact: limuyu0110@pku.edu.cn

"""

from web_rel import next_page_url_in_search, urls_in_one_search_page, get_soup_from_url
from tqdm import tqdm
from config import SEARCH_URL_GAME, URLS_FILE
import codecs
import json

if __name__ == "__main__":
    tmpurl = SEARCH_URL_GAME
    pgsoup = get_soup_from_url(tmpurl)
    urls = []
    for i in tqdm(range(1259, 1600)):
        try:
            urls.extend(urls_in_one_search_page(pgsoup))
            tmpurl = next_page_url_in_search(pgsoup)
            pgsoup = get_soup_from_url(tmpurl)
        except Exception:
            print("Error but continue")

    with codecs.open(URLS_FILE, 'w', 'utf8') as f:
        json.dump(urls, f, ensure_ascii=False, indent=4)

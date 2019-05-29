# -*- coding:utf-8 _*-
""" 
@author:limuyu
@file: text.py 
@time: 2019/05/13
@contact: limuyu0110@pku.edu.cn

"""

import codecs, json, os, re
import MeCab
from tqdm import tqdm

DESCS_PATH = "E:\\#Projects\\workspace\\a-char-des-scraping\\scrape\\raw_data\\descs"
FINAL_DESCS_PATH = "E:\\#Projects\\workspace\\a-char-des-scraping\\scrape\\raw_data\\final.json"


def judge(s):
    ban_list = ['年齢', '身長', 'スリーサイズ', '誕生日', 'cv', 'CV']
    for ban in ban_list:
        if ban in s:
            return False
    return True


def process_text(s):
    li = re.split('\u3000?\n+\u3000?', s)[2:]
    res = ''.join(list(filter(judge, li)))
    return res


if __name__ == '__main__':
    final_di = {}
    fl = os.listdir(DESCS_PATH)

    mecab = MeCab.Tagger('-Owakati')

    for fn in tqdm(fl):
        idx = int(fn.replace('.json', ''))
        with codecs.open(os.path.join(DESCS_PATH, fn), 'r', 'utf8') as g:
            text = process_text(json.load(g)['desc_str'])
        final_di[idx] = mecab.parse(text)

    with codecs.open(FINAL_DESCS_PATH, 'w', 'utf8') as f:
        json.dump(final_di, f, ensure_ascii=False, indent=4)

#-*- coding:utf-8 _*-  
""" 
@author:limuyu
@file: download_and_map.py 
@time: 2019/05/10
@contact: limuyu0110@pku.edu.cn

"""

from config import *
import codecs
import json
import concurrent.futures as cf
from tqdm import tqdm
import requests


def download_img(idx, url):
    r = requests.get(url, proxies={"http": "localhost:1080"})
    with open(os.path.join(IMG_PATH, F"{idx}.jpg"), 'wb') as f:
        f.write(r.content)


def g(item):
    idx = item['idx']
    desc_raw = item['desc_raw']
    desc_str = item['desc_str']
    url = ROOT_URL + item['src'][1:]

    with codecs.open(os.path.join(DESC_PATH, F"{idx}.json"), 'w', 'utf8') as f:
        json.dump({'desc_raw': desc_raw, 'desc_str': desc_str}, f, ensure_ascii=False, indent=4)

    download_img(idx, url)


if __name__ == '__main__':
    fl = [os.path.join(JSON_PATH, a) for a in os.listdir(JSON_PATH)]
    L = []
    for fn in fl:
        with codecs.open(fn, 'r', 'utf8') as f:
            L.extend(json.load(f))

    for i, a in enumerate(L):
        a['idx'] = i

    for i in tqdm(range(len(L) // CHUNK_SIZE + 1)):
        with cf.ProcessPoolExecutor(max_workers=20) as exe:
            exe.map(g, L[i * CHUNK_SIZE: i * CHUNK_SIZE + CHUNK_SIZE])



#-*- coding:utf-8 _*-  
""" 
@author:limuyu
@file: main.py 
@time: 2019/05/10
@contact: limuyu0110@pku.edu.cn

"""

import logging
from utils import *
from config import *
from web_rel import process_one_url
import codecs
import json
from tqdm import tqdm

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(processName)s - %(funcName)s - %(message)s'
log_filename = 'logs/run.log'

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

formatter = logging.Formatter(FORMAT)

handler_1 = logging.StreamHandler()
handler_1.setFormatter(formatter)

handler_2 = logging.FileHandler('logs/run.log', mode='a', encoding='utf8')
handler_2.setFormatter(formatter)

logger.addHandler(handler_1)
logger.addHandler(handler_2)


def trial_one_page():
    url = construct_page_url(URL_ID_TRIAL)
    process_one_url(url)


def seq():
    with codecs.open(URLS_FILE, 'r') as f:
        urls = json.load(f)
        for url in tqdm(urls):
            process_one_url(url)


if __name__ == '__main__':
    # trial_one_page()
    seq()

#-*- coding:utf-8 _*-  
""" 
@author:limuyu
@file: config.py 
@time: 2019/05/10
@contact: limuyu0110@pku.edu.cn

"""

import os

# Automatically Creating DataPath
RAW_DATA_PATH = os.path.join(os.path.abspath(os.path.curdir), 'raw_data')
JSON_PATH = os.path.join(RAW_DATA_PATH, 'jsons')
DESC_PATH = os.path.join(RAW_DATA_PATH, 'descs')
IMG_PATH = os.path.join(RAW_DATA_PATH, 'imgs')
LOG_PATH = os.path.join(os.path.abspath(os.path.curdir), 'logs')
URLS_FILE = os.path.join(RAW_DATA_PATH, 'urls')
COOKIE_FILE = os.path.join(RAW_DATA_PATH, 'cookie.txt')

os.makedirs(RAW_DATA_PATH, exist_ok=True)
os.makedirs(JSON_PATH, exist_ok=True)
os.makedirs(IMG_PATH, exist_ok=True)
os.makedirs(DESC_PATH, exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)

# urls
BASE_URL = "http://www.getchu.com/soft.phtml?id="
ROOT_URL = "http://www.getchu.com"
URL_ID_START = 100001
URL_ID_END = 1000000
URL_ID_TRIAL = 933144

SEARCH_URL_GAME = "http://www.getchu.com/sp/search.phtml?genre=pc_soft&search_keyword=&x=15&y=22&sort2=&sort=sales&pageID=1"


# others
YEAR_AFTER = 2010
CHUNK_SIZE = 100



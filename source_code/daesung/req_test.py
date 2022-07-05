import datetime
import time

import requests

# cookies = {
#     'visit%5Froot': 'OK',
#     'ASPSESSIONIDASSTBBTR': 'BEEDADLAAIJFBEPIDJCGFOBP',
#     'smtg_cKey': '1655278056122503027',
#     'smtg_fsID': '1',
#     'smtg_sKey': '1655278056732212601',
#     'smtg_sAd': '0',
#     '__utmc': '238667157',
#     '__utmz': '238667157.1655278057.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
#     'smtg_vTime': '1655281640',
#     'wcs_bt': '2406925d333a28:1655281640',
#     '__utma': '238667157.739928518.1655278057.1655278057.1655281640.2',
#     '__utmt': '1',
#     '__utmb': '238667157.1.10.1655281640',
# }

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'visit%5Froot=OK; ASPSESSIONIDASSTBBTR=BEEDADLAAIJFBEPIDJCGFOBP; smtg_cKey=1655278056122503027; smtg_fsID=1; smtg_sKey=1655278056732212601; smtg_sAd=0; __utmc=238667157; __utmz=238667157.1655278057.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); smtg_vTime=1655281640; wcs_bt=2406925d333a28:1655281640; __utma=238667157.739928518.1655278057.1655278057.1655281640.2; __utmt=1; __utmb=238667157.1.10.1655281640',
    'Referer': 'http://b2c.ds98.co.kr/shop/new_lst2.asp?cPage=99&num=11&flag=&cond=1&cate1=&cate2=&cate3=&image=',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

params = {
    'cPage': '96',
    'num': '0',
    'flag': '',
    'cond': '1',
    'cate1': '',
    'cate2': '',
    'cate3': '',
    'image': '',
}
"http://b2c.ds98.co.kr/shop/pro0102.asp?id=32422"
while True:
    response = requests.get("http://b2c.ds98.co.kr/shop/pro0102.asp?id=32422", params=params, headers=headers, verify=False)
    print(datetime.datetime.now(), response)
    time.sleep(2)
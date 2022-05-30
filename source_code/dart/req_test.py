import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

cookies = {
    'WMONID': 'zQ1Y_5IW2k5',
    'JSESSIONID': 'PAKahmexzpe4Z2D4VMCD5Sl7esXZBmtNqgtD9KfWUfzNKPRa7yyXihW2z3kLjJG0.ZG1fZGFydC9kYXJ0MV9kYXJ0X21zMw==',
}

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'WMONID=zQ1Y_5IW2k5; JSESSIONID=PAKahmexzpe4Z2D4VMCD5Sl7esXZBmtNqgtD9KfWUfzNKPRa7yyXihW2z3kLjJG0.ZG1fZGFydC9kYXJ0MV9kYXJ0X21zMw==',
    'Origin': 'https://dart.fss.or.kr',
    'Referer': 'https://dart.fss.or.kr/dsab001/main.do',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


excel_file = 'input.xlsx'

excel_dir = os.path.join(excel_file)

df_from_excel = pd.read_excel(excel_dir,  # write your directory here
                              sheet_name='Sheet1',
                              )

urls = df_from_excel['회사명'].values.tolist()

results = []
for x in urls:
    data = {
        'currentPage': '1',
        'maxResults': '15',
        'maxLinks': '10',
        'sort': 'date',
        'series': 'desc',
        # 'textCrpCik': '00158398',
        'pageGubun': 'corp',
        'attachDocNmPopYn': '',
        'textCrpNm': x,
        'startDate': '20150101',
        'endDate': '20200530',
        'decadeType': '',
        'attachDocNm': '',
    }


    response = requests.post('https://dart.fss.or.kr/dsab001/searchCorp.ax', cookies=cookies, headers=headers, data=data)
    res = response.text
    soup = BeautifulSoup(res, 'html.parser')
    try:
        a = 'https://dart.fss.or.kr'+soup.find(href=re.compile('/'), text=re.compile('감사보고서') and re.compile('2015'))['href']
        results.append([x, a,'2015'])
    except:
        pass

    try:
        b = 'https://dart.fss.or.kr'+soup.find(href=re.compile('/'), text=re.compile('감사보고서') and re.compile('2016'))['href']
        results.append([x, b, '2016'])
    except:

        pass
    try:
        c = 'https://dart.fss.or.kr'+soup.find(href=re.compile('/'), text=re.compile('감사보고서') and re.compile('2017'))['href']
        results.append([x, c, '2017'])
    except:

        pass
    try:
        d = 'https://dart.fss.or.kr'+soup.find(href=re.compile('/'), text=re.compile('감사보고서') and re.compile('2018'))['href']
        results.append([x, d, '2018'])
    except:

        pass
    try:
        e = 'https://dart.fss.or.kr'+soup.find(href=re.compile('/'), text=re.compile('감사보고서') and re.compile('2019'))['href']
        results.append([x, e, '2019'])
    except:
        pass
print(results)


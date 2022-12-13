# https://shopping.naver.com/outlet/branch/10011

# coding: utf-8
import datetime
import json
import os
import re
import time

import chromedriver_autoinstaller
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
path = chromedriver_autoinstaller.install(True)
file_datetime = datetime.datetime.now().strftime('%y%m%d_%H%M')


os.mkdir(f'./{file_datetime}')


def explicitly_wait(driver, by, name):
    try:
        return WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((by, name)))
    except Exception as e:
        raise ValueError(by, name)


def log_flush(driver):
    while driver.get_log('performance'):
        time.sleep(.5)


def print_xlsx(list_, path, header, header_size):
    df = pd.DataFrame(list_, )
    writer = pd.ExcelWriter(f"./{file_datetime}/{path}.xlsx", engine='xlsxwriter', )
    df.to_excel(writer, header=header, index=False)
    for column, column_length in zip(df, header_size):
        col_idx = df.columns.get_loc(column)
        writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)
    writer.close()


def log_filter(log_, filter_url):
    return (
        # is an actual response
            log_["method"] == "Network.responseReceived"
            # and json
            and "json" in log_["params"]["response"]["mimeType"]
            # and log_["params"]["response"]["url"].find(filter_url) > 1
            and re.compile(fr'({filter_url})').findall(log_["params"]["response"]["url"])
    )
    # if res:
    #     re.compile(fr'{filter_url}').findall(log_["params"]["response"]["url"])
    #
    # return res


# log_["params"]["response"]["url"].find(filter_url) > 1


def extract_logs(driver, filter_url):
    try:
        cnt = 0
        requests_ids = [[]] * len(filter_url)
        browser_log = []
        results = [[]] * len(filter_url)
        while True:
            [browser_log.append(x) for x in driver.get_log('performance')]
            logs = [json.loads(lr["message"])["message"] for lr in browser_log]

            for idx, url in enumerate(filter_url):
                results[idx] = list(filter(lambda x: log_filter(x, url), logs))

            if sum(x != [] for x in results) == len(filter_url):
                break
            time.sleep(.5)
            cnt += 1
            if cnt > 50:
                # print(browser_log)
                break
                # raise ValueError('no logs')

        for idx, log in enumerate(results):
            # request_id = log["params"]["requestId"]
            try:
                requests_ids[idx] = log[0]["params"]["requestId"]
            except:
                requests_ids[idx] = log
        return requests_ids
    except:
        pass


# pymysql.install_as_MySQLdb()

# warnings.simplefilter("ignore", category=pymysql.Warning)

# Base = declarative_base()
# metadata = Base.metadata

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

WAITTIME = 30
# if os.name == 'nt':
#     CHROMEDRIVERPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver')
# else:
#     CHROMEDRIVERPATH = 'chromedriver'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument('--incognito')
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--lang=en-US")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('user-agent={0}'.format(user_agent))

# prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 40960}
# options.add_experimental_option("prefs", prefs)
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}


def driver_setting():
    driver = webdriver.Chrome(executable_path=path, options=options,
                              desired_capabilities=caps)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


if __name__ == '__main__':
    # driver = driver_setting()
    #
    results = []
    header = ['링크', '강의명', '만족비율', '카테고리', '평가 수', '평균 별점', '컨텐츠 평가 카운트', '별점 비율', '습득기술', '설명', 'x주차 교육']
    with open(r'links2.txt', 'r', encoding='utf8') as f:
        links = f.readlines()
    for link in links:

        try:
            link = link.split('\n')[0]
            headers = {
                'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
                'Connection': 'keep-alive',
                'Origin': 'https://www.coursera.org',
                'Referer': 'https://www.coursera.org/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'cross-site',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
                'accept': 'application/json',
                'content-type': 'application/x-www-form-urlencoded',
                'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
                'sec-ch-ua-mobile': '?0',
            }
            # link = "https://www.coursera.org/learn/financial-markets-global"
            res = requests.get(link, headers=headers)
            res.encoding = 'utf8'
            reg = re.compile(r'window.__APOLLO_STATE__ = (.*);\n')
            xx = json.loads(reg.search(res.text).group(1))
            # name =
            r = re.compile(".*XdpV1:COURSE.*")
            id_ = list(filter(r.match, xx.keys()))[0].split('~')[1]
            # xx2[list(filter(r.match, xx2.keys()))[0]]
            # print(list(filter(r.match, xx2.keys()))[0])
            # print(list(filter(r.match, xx.keys()))[0])

            r2 = re.compile(".*domains.0.*")
            # print(list(filter(r2.match, xx2.keys())))
            # print(list(filter(r2.match, xx.keys())))

            r3 = re.compile(f".*XdpV1_org_coursera_xdp_cdp_CDPMetadata:{id_}")
            # print(list(filter(r32.match, xx2.keys()))[0])
            # print(list(filter(r3.match, xx.keys()))[0])

            r4 = re.compile(f".*XdpV1_org_coursera_xdp_cdp_CDPMetadata:{id_}.ratings.*")
            # print(list(filter(r42.match, xx2.keys())))
            # print(list(filter(r4.match, xx.keys())))

            r5 = re.compile(f"XdpV1_org_coursera_xdp_common_XDPCourseModule")
            # print(list(filter(r5.match, xx2.keys())))
            # for x in list(filter(r5.match, xx2.keys())):
            #     print(xx2[x])
            result = []
            # print(xx[list(filter(r3.match, xx.keys()))[0]]['name'])
            # print(round(xx[list(filter(r3.match, xx.keys()))[0]]['averageContentSatisfactionScore']))
            # print(xx[list(filter(r2.match, xx.keys()))[0]]['domainName'] + ' > '+ xx[list(filter(r2.match, xx.keys()))[0]]['subdomainName'])
            # print(xx[list(filter(r4.match, xx.keys()))[0]]['ratingCount'], round(xx[list(filter(r4.match, xx.keys()))[0]]['averageFiveStarRating'], 1),xx[list(filter(r3.match, xx.keys()))[0]]['contentSatisfactionRatingsCount'] )
            weeks = []
            for x in list(filter(r5.match, xx.keys())):
                cc = xx[x]
                try:
                    dt = datetime.datetime.strptime(str(datetime.timedelta(seconds=cc['totalDuration'] / 1000)), "%H:%M:%S.%f")
                except:
                    dt = datetime.datetime.strptime(str(datetime.timedelta(seconds=cc['totalDuration'] / 1000)), "%H:%M:%S")
                if dt.minute > 30:
                    hours = dt.hour + 1
                else:
                    hours = dt.hour
                if hours == 0:
                    hours = 1
                hours = f'완료하는 데 {hours}시간 필요 '
                videos = f"{cc['totalVideos']}개 동영상(총 {round(cc['totalLectureDuration'] / 1000 / 60)}분), {cc['totalReadings']} 개의 읽기 자료, {cc['totalQuizzes'] if cc['totalReadings'] else 0} 개의 테스트"
                weeks.append(hours + videos)

            # //div[@class='ProductGlance']/div[contains(@class,'_y1d9czk m-b-2 p-t-1s')]

            # //div[@data-unit]
            explain = []
            soup = BeautifulSoup(res.text, 'lxml')
            for x in soup.find('div', attrs={'class': 'ProductGlance'}).find_all('div', attrs={'class': '_1tu07i3a'})[1:]:
                tmp = []
                for xxx in x.findAll('div')[:2]:
                    tmp.append(xxx.text)
                explain.append(" : ".join(tmp))
            # print(soup.find('div', attrs={'data-unit': 'reviews-bar-graph'}).text.replace("%", "%\n").replace("star","stars : ").replace(': s', ': ').replace('1 stars', '1 star'))
            try:
                skills = xx[list(filter(r3.match, xx.keys()))[0]]['skills']['json']
            except:
                skills = ['None']
            result.append(link)
            result.append(xx[list(filter(r3.match, xx.keys()))[0]]['name'])
            try:
                result.append(round(xx[list(filter(r3.match, xx.keys()))[0]]['averageContentSatisfactionScore']))
            except:
                result.append(0)

            result.append(xx[list(filter(r2.match, xx.keys()))[0]]['domainName'] + ' > '+ xx[list(filter(r2.match, xx.keys()))[0]]['subdomainName'])
            try:
                result.append(xx[list(filter(r4.match, xx.keys()))[0]]['ratingCount'])
            except:
                result.append(0)
            try:
                result.append(round(xx[list(filter(r4.match, xx.keys()))[0]]['averageFiveStarRating'], 1))
            except:
                result.append(0)
            try:
                result.append(xx[list(filter(r3.match, xx.keys()))[0]]['contentSatisfactionRatingsCount'] )
            except:
                result.append(0)
            try:
                result.append(soup.find('div', attrs={'data-unit': 'reviews-bar-graph'}).text.replace("%", "%\n").replace("star","stars : ").replace(': s', ': ').replace('1 stars', '1 star'))
            except:
                result.append('None')
            result.append(", ".join(skills))
            result.append("\n".join(explain))
            result.append("\n".join(weeks))
            result = [str(x) for x in result]

            print(result)
            results.append(result)
        except:
            none_list = [link] + [None]*(len(header)-1)
            print(none_list)
            results.append(none_list)

    # list_, path, header, header_size
    print_xlsx(results, './결과물',header,[20, 20, 20, 20, 20, 20,20, 20, 20, 20, 20, ])
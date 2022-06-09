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
# os.mkdir(f'./{file_datetime}')


# os.mkdir(f'./{file_datetime}/Top 100')


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
            log_["method"] == 'Network.requestWillBeSent'
            # and json
            # and "json" in log_["params"]["response"]["mimeType"]
            # and log_["params"]["response"]["url"].find(filter_url) > 1
            and re.compile(fr'({filter_url})').findall(log_["params"]["documentURL"])
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
                requests_ids[idx] = log[-1]["params"]['documentURL']
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
options.add_argument('--headless')
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
s = Service(path)


def driver_setting():
    driver = webdriver.Chrome(service=s, options=options,
                              desired_capabilities=caps)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


if __name__ == '__main__':
    excel_file = 'results.xlsx'

    excel_dir = os.path.join(excel_file)

    df_from_excel = pd.read_excel(excel_dir,  # write your directory here
                                  sheet_name='Sheet1',
                                  )

    names = df_from_excel['회사명'].values.tolist()
    urls = df_from_excel['url'].values.tolist()
    years = df_from_excel['연도'].values.tolist()

    a = ''
    b = ''
    d = ''
    e = ''
    f = ''
    g = ''
    h = ''
    i = ''
    j = ''
    k = ''
    l = ''
    gap = 32
    try:
        for idx, name in enumerate(names[gap:]):
            try:
                driver = driver_setting()
                driver.get(urls[idx+gap])
                driver.find_element(By.XPATH, "//a[contains(text(),'재무')]").click()
                xx = extract_logs(driver, ['eleId'])
                driver.get(xx[0])
                soup = BeautifulSoup(driver.page_source, 'lxml')
                for x in soup.find(['td','p'], text=re.compile(r"유동자산")).find_all_next('td', align='RIGHT'):
                    if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                        a = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                        # print(soup.find(['td','p'], text=re.compile(r"유동자산")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                        break
                for x in soup.find(['td','p'], text=re.compile(r"비유동자산")).find_all_next('td', align='RIGHT'):
                    if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                        b = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                        # print(soup.find(['td', 'p'], text=re.compile(r"비유동자산")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                        break
                try:
                    for x in soup.find(['td','p'], text=re.compile(r"자([ ]*\xa0[ ]*){0,}본([ ]*\xa0[ ]*){0,}총([ ]*\xa0[ ]*){0,}계")).find_all_next('td', align='RIGHT'):
                        if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                            d = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                            # print(soup.find(['td','p'], text=re.compile(r"자([ ]*\xa0[ ]*){0,}본([ ]*\xa0[ ]*){0,}총([ ]*\xa0[ ]*){0,}계")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                            break
                except:
                    for x in soup.find(['td','p'], text=re.compile(r"자(\xa0 ){0,}본(\xa0 ){0,}총(\xa0 ){0,}계")).find_all_next('td', align='RIGHT'):
                        if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                            d = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                            # print(soup.find(['td','p'], text=re.compile(r"자(\xa0 ){0,}본(\xa0 ){0,}총(\xa0 ){0,}계")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                            break
                try:
                    for x in soup.find(['td','p'], text=re.compile(r"자([ ]*\xa0[ ]*){0,}산([ ]*\xa0[ ]*){0,}총([ ]*\xa0[ ]*){0,}계")).find_all_next('td', align='RIGHT'):
                        if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                            e = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                            # print(soup.find(['td','p'], text=re.compile(r"자([ ]*\xa0[ ]*){0,}산([ ]*\xa0[ ]*){0,}총([ ]*\xa0[ ]*){0,}계")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                            break
                except:
                    for x in soup.find(['td','p'], text=re.compile(r"자( \xa0){0,}산( \xa0){0,}총( \xa0){0,}계")).find_all_next('td', align='RIGHT'):
                        if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                            e = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                            # print(soup.find(['td','p'], text=re.compile(r"자( \xa0){0,}산( \xa0){0,}총( \xa0){0,}계")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                            break
                for x in soup.find(['td','p'], text=re.compile(r"매출액")).find_all_next('td', align='RIGHT'):
                    if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                        f = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                        # print(soup.find(['td','p'], text=re.compile(r"매출액")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                        break
                for x in soup.find(['td','p'], text=re.compile(r"매출총이익")).find_all_next('td', align='RIGHT'):
                    if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                        g = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                        # print(soup.find(['td','p'], text=re.compile(r"매출총이익")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                        break
                try:
                    for x in soup.find(['td','p'], text=re.compile(r"1. 급여")).find_all_next('td', align='RIGHT'):
                        if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                            h = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                            # print(soup.find(['td','p'], text=re.compile(r"1. 급여")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                            break
                except:
                    try:
                        for x in soup.find(['td','p'], text="급여").find_all_next('td', align='RIGHT'):
                            if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                                h = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                                # print(soup.find(['td','p'], text="급여").find_parent('table').find_previous('table').text.split(':')[1].strip())
                                break
                    except:
                        try:
                            for x in soup.find(['td','p'], text="급여및상여").find_all_next('td', align='RIGHT'):
                                if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                                    h = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                                    # print(soup.find(['td','p'], text="급여및상여").find_parent('table').find_previous('table').text.split(':')[1].strip())
                                    break
                        except:
                            try:
                                for x in soup.find(['td','p'], text=re.compile("급료와수당")).find_all_next('td', align='RIGHT'):
                                    if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                                        h = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                                        # print(soup.find(['td','p'], text=re.compile("급료와수당")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                                        break
                            except:
                                for x in soup.find(['td', 'p'], text=re.compile("급여[ ]*및[ ]*상여")).find_all_next('td', align='RIGHT'):
                                    if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-', '').replace('\xa0', ''):
                                        h = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0', '')
                                        # print(soup.find(['td', 'p'], text=re.compile("급여[ ]*및[ ]*상여")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                                        break
                try:
                    for x in soup.find(['td','p'], text=re.compile(r"교육훈련비")).find_all_next('td', align='RIGHT'):
                        if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                            i = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                            # print(soup.find(['td','p'], text=re.compile(r"교육훈련비")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                            break
                except:
                    try:
                        for x in soup.find(['td','p'], text=re.compile(r"교육비")).find_all_next('td', align='RIGHT'):
                            if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                                i = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                                # print(soup.find(['td','p'], text=re.compile(r"교육비")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                                break
                    except:
                        i='0'
                for x in soup.find(['td','p'], text=re.compile(r"영업이익")).find_all_next('td', align='RIGHT'):
                    if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                        j = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                        # print(soup.find(['td','p'], text=re.compile(r"영업이익")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                        break
                try:
                    for x in soup.find(['td','p'], text=re.compile(r"법인세비용차감전순이익")).find_all_next('td', align='RIGHT'):
                        if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                            k = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                            # print(soup.find(['td','p'], text=re.compile(r"법인세비용차감전순이익")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                            break
                except:
                    for x in soup.find(['td','p'], text=re.compile(r"법인세비용차감전순손실")).find_all_next('td', align='RIGHT'):
                        if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                            k = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                            # print(soup.find(['td','p'], text=re.compile(r"법인세비용차감전순손실")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                            k = '-'+ k
                            break
                for x in soup.find(['td','p'], text=re.compile(r"당기순이익")).find_all_next('td', align='RIGHT'):
                    if x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0',''):
                        l = x.text.replace(' ', '').replace('　', '').replace(',', '').replace('-','').replace('\xa0','')
                        # print(soup.find(['td','p'], text=re.compile(r"당기순이익")).find_parent('table').find_previous('table').text.split(':')[1].strip())
                        # if len(l) < 7:
                        #     l = l + '000'
                        break

                print([name, urls[idx+gap], years[idx+gap], a, b, d, e, f, g, h, i, j, k, l])
                a = ''
                b = ''
                d = ''
                e = ''
                f = ''
                g = ''
                h = ''
                i = ''
                j = ''
                k = ''
                l = ''
                # print(1)
                driver.close()
            except:
                a = ''
                b = ''
                d = ''
                e = ''
                f = ''
                g = ''
                h = ''
                i = ''
                j = ''
                k = ''
                l = ''
                print([name, urls[idx + gap], years[idx + gap], a, b, d, e, f, g, h, i, j, k, l])
                driver.close()
                pass

    except Exception as exc:
        # print([name, urls[idx+gap], years[idx+gap], a, b, d, e, f, g, h, i, j, k, l])
        # print(exc)
        # driver.close()
        pass

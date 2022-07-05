# coding: utf-8
import datetime
import json
import re
import time

import chromedriver_autoinstaller
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from apscheduler.schedulers.blocking import BlockingScheduler

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
path = chromedriver_autoinstaller.install(True)
file_datetime = datetime.datetime.now().strftime('%y%m%d_%H%M')

# 스케줄러를 활용하기위한 라이브러리
sched = BlockingScheduler()


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
            and re.compile(fr'({filter_url})').findall(log_["params"]["response"]["url"])
    )


def extract_logs(driver, filter_url):
    try:
        requests_ids = []
        browser_log = []
        results = []
        [browser_log.append(x) for x in driver.get_log('performance')]
        logs = [json.loads(lr["message"])["message"] for lr in browser_log]

        for idx, url in enumerate(filter_url):
            results = list(filter(lambda x: log_filter(x, url), logs))

        for idx, log in enumerate(results):
            requests_ids.append(log["params"]["requestId"])

        return requests_ids
    except:
        pass


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

WAITTIME = 30

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

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}


def driver_setting():
    driver = webdriver.Chrome(executable_path=path, options=options,
                              desired_capabilities=caps)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


# decorator로 스케줄을 관리
@sched.scheduled_job('cron', minute=0, id='job_1')  # 매 시각 0분마다 실행
def get_data():
    driver = driver_setting()
    driver.get("https://finance.daum.net/domestic/kospi")
    while True:
        try:
            driver.find_element(By.XPATH, "//*[contains(@title,'예상지수')]").click()
            driver.find_element(By.XPATH, "//*[contains(@title,'시간별')]").click()
            break
        except:
            driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
            time.sleep(.5)

    while True:
        try:
            for _ in range(0, 2):
                for x in range(0, 9):
                    driver.find_elements(
                        By.XPATH, "//div[contains(@id,'boxHistories')]//a[contains(@class,'btnMove')]")[x].click()
                    time.sleep(.2)
                driver.find_element(
                    By.XPATH, "//div[contains(@id,'boxHistories')]//a[contains(@class,'btnNext')]").click()
                time.sleep(.2)
            break
        except:
            driver.find_element(By.XPATH, "//body").send_keys(Keys.PAGE_DOWN)
            time.sleep(.5)

    requests_ids = extract_logs(driver, ["finance.daum.net/api/market_index/times?"])
    data = []

    for req_id in requests_ids:
        [data.append(x) for x in json.loads(driver.execute_cdp_cmd(
            "Network.getResponseBody", {"requestId": req_id})['body'])['data']]
    seen = set()
    new_l = []
    for d in data:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)

    # datalist 파싱 활용하시면 됩니다.
    datalist = sorted(new_l, key=lambda d: d['date'])


if __name__ == '__main__':
    # 시각마다 돌기 전 처음 실행
    get_data()

    # 스케줄러 실행
    sched.start()
    while True:
        # 0.5초마다 체크하면서 스케줄러를 실행
        time.sleep(.5)

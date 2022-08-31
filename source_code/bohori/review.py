# coding: utf-8
import glob
import datetime
import json
import re
import time

import chromedriver_autoinstaller
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import numpy as np
from tqdm import tqdm
import os.path


chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
path = chromedriver_autoinstaller.install(True)
file_datetime = datetime.datetime.now().strftime('%y%m%d_%H%M')

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
    excel_file = 'input.xlsx'

    excel_dir = os.path.join(excel_file)

    df_from_excel = pd.read_excel(excel_dir,  # write your directory here
                                  sheet_name='Sheet1',
                                  )
    reviews = df_from_excel.values.tolist()

    for idx, review in enumerate(tqdm(reviews, '리뷰')):
        driver = driver_setting()
        pic = idx + 2
        pic_list = []

        [pic_list.append(os.path.abspath(x)) for x in glob.glob(f'./picture/{pic}.*')]
        [pic_list.append(os.path.abspath(x)) for x in glob.glob(f'./picture/{pic}-*')]
        driver.get(review[3])
        driver.find_element(By.XPATH, "//a[contains(@href,'login')]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[contains(@name,'member_id')]").send_keys(review[0])
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[contains(@name,'member_passwd')]").send_keys(review[1])
        time.sleep(1)
        try:
            driver.find_element(By.XPATH, "//button[contains(@class,'btn loginBtn')]").click()
        except:
            driver.find_element(By.XPATH, "//a[contains(@onclick,'login')]").click()
        time.sleep(1)
        driver.get(review[3])
        # explicitly_wait(driver, By.XPATH, "//div[contains(@class,'create_review')]")
        already_review = False
        while True:
            try:
                driver.switch_to.default_content()
                if review[3].find('amenz') > 0:
                    driver.switch_to.frame('crema-product-reviews-1')
                else:
                    driver.switch_to.frame('crema-product-reviews-2')
                time.sleep(1)
                try:
                    driver.find_element(By.XPATH, "//div[contains(@class,'create_review')]").click()
                except Exception as e:
                    already_review = True
                    print('이미 작성된 리뷰')
                    break
                time.sleep(2)
                try:
                    driver.switch_to.alert
                    break
                except:
                    pass
            except:
                pass
        if already_review:
            driver.quit()
            continue
        driver.switch_to.alert.accept()
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame("crema-review-popup")
        except:
            print('이미 작성된 리뷰')
            driver.quit()
            continue
        time.sleep(.5)
        driver.find_element(By.XPATH, "//*[@id='review_message']").send_keys(review[2])

        driver.switch_to.default_content()
        driver.switch_to.frame("crema-review-popup")
        time.sleep(.5)
        driver.find_element(By.XPATH, "//*[@class='select2-choice']").click()

        driver.switch_to.default_content()
        driver.switch_to.frame("crema-review-popup")
        time.sleep(.5)
        driver.find_element(By.XPATH, f'//*[@id="select2-results-1"]/li[{6-review[4]}]').click()

        for idx, x in enumerate(review[5:]):
            if np.isnan(x):
                break
            driver.switch_to.default_content()
            driver.switch_to.frame("crema-review-popup")
            driver.find_element(By.XPATH,
                                f"//div[@class='review_popup_form__section'][{idx + 5}]//div[contains(@class,'section_button_item')][{int(x)}]").click()

        if pic_list:
            driver.find_element(By.XPATH, "//input[contains(@class,'_field_input_file')][contains(@accept,'image')]").send_keys("\n".join(pic_list))
        driver.find_element(By.XPATH, f"//button[@name='commit']").click()

        while True:
            try:
                driver.switch_to.default_content()
                driver.switch_to.frame("crema-review-popup")
                time.sleep(1)
            except:
                break
        driver.quit()



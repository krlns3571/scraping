# https://shopping.naver.com/outlet/branch/10011

# coding: utf-8
import datetime
import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

from powernad.API.Campaign import *


chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
path = chromedriver_autoinstaller.install(True)
file_datetime = datetime.datetime.now().strftime('%y%m%d_%H%M')

# 날짜 입력 부분
START_DATE = '2022-07-01'
END_DATE = '2022-07-05'

KWD_API_CUSTOMER_ID_ID = 726614
KWD_API_ACCESS_LICCENSE = "0100000000a32791b0b22d898089e52054e050cef3484a0b0915a34ac04f012c0c15199152"
KWD_API_SECRET_KEY = "AQAAAACjJ5Gwsi2JgInlIFTgUM7zplfppOJbvH5/bY+q2emssQ=="
KRW_API_URL = "https://api.naver.com"


def explicitly_wait(driver, by, name):
    try:
        return WebDriverWait(driver, WAITTIME).until(EC.presence_of_element_located((by, name)))
    except Exception as e:
        raise ValueError(by, name)


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

WAITTIME = 30

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

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

def driver_setting():
    driver = webdriver.Chrome(executable_path=path, options=options,
                              desired_capabilities=caps)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


daily_cost = []

if __name__ == '__main__':
    driver = driver_setting()
    driver.get("https://searchad.naver.com/")

    campaign = Campaign(KRW_API_URL,
                        KWD_API_ACCESS_LICCENSE,
                        KWD_API_SECRET_KEY,
                        KWD_API_CUSTOMER_ID_ID)
    campaign_lists = campaign.get_campaign_list()
    [print(str(idx + 1) + ')\t' + x.name) for idx, x in enumerate(campaign_lists)]
    while True:
        num = input("조회하실 캠페인의 번호를 입력해주세요 : ")
        try:
            if int(num) <= len(campaign_lists):
                break
            else:
                print('잘못된 캠페인을 입력하셨습니다. 다시 입력해주세요')
        except:
            print('잘못된 캠페인을 입력하셨습니다. 다시 입력해주세요')

    driver.find_element(By.XPATH, "//input[contains(@name,'id')]").send_keys("photoyoda")
    driver.find_element(By.XPATH, "//input[contains(@name,'pw')]").send_keys("ahtusapdlzj09@")
    driver.find_element(By.XPATH, "//span[contains(@class,'btn_login')]/button").send_keys(Keys.ENTER)

    explicitly_wait(driver, By.XPATH, "//a[contains(@class,'btn_add ad')]")

    driver.find_element(By.XPATH, "//a[contains(@class,'btn_add ad')]").send_keys(Keys.ENTER)

    explicitly_wait(driver, By.XPATH, "//button[contains(@class,'btn-sm btn-toggle')]")

    driver.find_element(By.XPATH, "//button[contains(@class,'btn-sm btn-toggle')]").click()
    driver.find_element(By.XPATH, "//button[contains(@role,'menuitem')][contains(text(),'100')]").click()

    driver.find_element(By.XPATH, "//body").send_keys(Keys.HOME)
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[contains(@data-toggle,'dropdown')]").click()

    s_date = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
    t_date = datetime.datetime.strptime(START_DATE, '%Y-%m-%d')
    e_date = datetime.datetime.strptime(END_DATE, '%Y-%m-%d')

    while True:
        ts_year, ts_month = driver.find_elements(By.XPATH,
                                                 "//div[contains(text(),'시작일')]/..//span[contains(@class,'month-title')]/span")
        if str(s_date.year) == ts_year.text:
            if str(s_date.month) == ts_month.text:
                driver.find_elements(By.XPATH,
                                     f"//div[contains(text(),'시작일')]/..//span[contains(@class,'w-100')][contains(text(),'')]")[
                    s_date.day - 1].click()

            else:
                driver.find_element(By.XPATH,
                                    '//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[3]/div/button[1]').click()
                driver.find_elements(By.XPATH,
                                     f"//div[contains(text(),'시작일')]/..//span[contains(@class,'w-100')][contains(text(),'')]")[
                    s_date.day - 1].click()
            break
        driver.find_element(By.XPATH, "//div[contains(text(),'시작일')]/..//i[contains(@class,'angle-left')]").click()

    while True:
        te_year, te_month = driver.find_elements(By.XPATH,
                                                 "//div[contains(text(),'종료일')]/..//span[contains(@class,'month-title')]/span")
        if str(e_date.year) == te_year.text:
            if str(e_date.month) == te_month.text:
                driver.find_elements(By.XPATH,
                                     f"//div[contains(text(),'종료일')]/..//span[contains(@class,'w-100')][contains(text(),'')]")[
                    e_date.day - 1].click()
                break
        driver.find_element(By.XPATH, "//div[contains(text(),'종료일')]/..//i[contains(@class,'angle-left')]").click()
    driver.find_element(By.XPATH, "//button[contains(text(),'적용')]").click()
    time.sleep(3)

    month_cost = [f"{START_DATE} ~ {END_DATE}",
                  driver.find_elements(By.XPATH, "//tr[contains(@class,'  ')]")[int(num) - 1].find_elements(
                      By.XPATH, './td')[
                      -1].text]

    while True:
        print('\r'+str(t_date.date())+ '\t' + '수집중', end='')
        driver.find_element(By.XPATH, "//body").send_keys(Keys.HOME)
        driver.find_element(By.XPATH, "//div[contains(@data-toggle,'dropdown')]").click()

        driver.find_elements(By.XPATH,
                             f"//div[contains(text(),'시작일')]/..//span[contains(@class,'w-100')][contains(text(),'')]")[
            t_date.day - 1].click()
        driver.find_elements(By.XPATH,
                             f"//div[contains(text(),'종료일')]/..//span[contains(@class,'w-100')][contains(text(),'')]")[
            t_date.day - 1].click()

        driver.find_element(By.XPATH, "//button[contains(text(),'적용')]").click()
        time.sleep(.2)

        daily_cost.append([t_date.strftime('%Y-%m-%d'),
                           driver.find_elements(By.XPATH, "//tr[contains(@class,'  ')]")[
                               int(num) - 1].find_elements(By.XPATH, './td')[
                               -1].text])
        t_date = t_date + datetime.timedelta(days=1)

        if t_date == e_date + datetime.timedelta(days=1):
            break

    driver.quit()
    print('\n')
    print(campaign_lists[int(num) - 1].name)
    print("\n".join(month_cost))
    # [print("\n".join(x)) for x in daily_cost]
    for date, cost in daily_cost:
        print(date)
        print(cost)

# coding: utf-8
import glob
import datetime
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service

import numpy as np
from tqdm import tqdm
import os.path

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  # 크롬드라이버 버전 확인
path = chromedriver_autoinstaller.install(True)
file_datetime = datetime.datetime.now().strftime('%y%m%d_%H%M')

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
s = Service(path)


# CHROMEDRIVER 세팅
def driver_setting():
    driver = webdriver.Chrome(service=s, options=options,
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

    # 엑셀 ROW별 리뷰 작성
    for idx, review in enumerate(tqdm(reviews, '리뷰')):
        driver = driver_setting()
        pic = idx + 2
        # 사진목록을 담을 리스트
        pic_list = []

        # 리스트에 사진을 담는 작업 ex) 1.jpg, 1-1.jpg...
        [pic_list.append(os.path.abspath(x)) for x in glob.glob(f'./picture/{pic}.*')]
        [pic_list.append(os.path.abspath(x)) for x in glob.glob(f'./picture/{pic}-*')]

        # 리뷰작성할 페이지 접속
        driver.get(review[3])

        # 로그인 버튼 클릭
        driver.find_element(By.XPATH, "//a[contains(@href,'login')]").click()
        time.sleep(1)

        # 아이디 입력
        driver.find_element(By.XPATH, "//input[contains(@name,'member_id')]").send_keys(review[0])
        time.sleep(1)
        # 패스워드 입력
        driver.find_element(By.XPATH, "//input[contains(@name,'member_passwd')]").send_keys(review[1])
        time.sleep(1)

        # 로그인버튼 클릭
        try:
            driver.find_element(By.XPATH, "//button[contains(@class,'btn loginBtn')]").click()
        except:
            driver.find_element(By.XPATH, "//a[contains(@onclick,'login')]").click()
        time.sleep(1)
        driver.get(review[3])
        while True:
            try:
                driver.switch_to.default_content()
                # amenz를 제외하고는 iframe 설정
                if review[3].find('amenz') > 0:
                    driver.switch_to.frame('crema-product-reviews-1')
                else:
                    driver.switch_to.frame('crema-product-reviews-2')
                try:
                    driver.find_element(By.XPATH, "//div[contains(@class,'create_review')]").click()
                except:
                    # 이미 리뷰를 작성한 계정이라면 넘어가는 구조
                    print('이미 작성된 리뷰')
                    break
                time.sleep(2)
                try:
                    # alert창이 뜬다면 넘어가서 accept로 수락
                    driver.switch_to.alert
                    break
                except:
                    pass
            except:
                pass

        driver.switch_to.alert.accept()
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame("crema-review-popup")
        except:
            # 이미 리뷰를 작성한 계정이라면 넘어가는 구조
            print('이미 작성된 리뷰')
            break
        time.sleep(.5)
        driver.find_element(By.XPATH, "//*[@id='review_message']").send_keys(review[2])

        driver.switch_to.default_content()
        driver.switch_to.frame("crema-review-popup")
        time.sleep(.5)

        # 별점 클릭후 만족도 클릭
        driver.find_element(By.XPATH, "//*[@class='select2-choice']").click()
        driver.switch_to.default_content()
        driver.switch_to.frame("crema-review-popup")
        time.sleep(.5)
        driver.find_element(By.XPATH, f'//*[@id="select2-results-1"]/li[{6 - review[4]}]').click()

        # 기타 옵션메뉴 선택
        for idx, x in enumerate(review[5:]):
            if np.isnan(x):
                break
            driver.switch_to.default_content()
            driver.switch_to.frame("crema-review-popup")
            driver.find_element(By.XPATH,
                                f"//div[@class='review_popup_form__section'][{idx + 5}]//div[contains(@class,'section_button_item')][{int(x)}]").click()

        # 사진이 있다면 사진 입력, 없으면 PASS
        if pic_list:
            driver.find_element(By.XPATH,
                                "//input[contains(@class,'_field_input_file')][contains(@accept,'image')]").send_keys(
                "\n".join(pic_list))
        # 리뷰 작성 버튼
        driver.find_element(By.XPATH, f"//button[@name='commit']").click()
        driver.quit()

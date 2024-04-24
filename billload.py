#-*- coding: utf-8 -*-

import time
from datetime import date, timedelta

from bs4 import BeautifulSoup
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

cafe_id = '' # id
cafe_pw = '' # pw
service = Service()
options = webdriver.EdgeOptions()
options.add_argument("-inprivate")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0')
options.add_argument('--disable-blink-features=AutomationControlled')
web = Edge(service=service, options=options)

# day = date(2023, 11, 13) + timedelta(days=1)
# sqlyesterday = day.strftime('%Y-%m-%d')

# 카페24 로그인
web.get('https://eclogin.cafe24.com/Shop/')
web.maximize_window()
time.sleep(2)
web.execute_script(f"document.getElementById('mall_id').value = '{cafe_id}';")
web.execute_script(f"document.getElementById('userpasswd').value = '{cafe_pw}';")
time.sleep(2)
web.find_element(By.CSS_SELECTOR, '#frm_user > div > div.mButton > button').click()
time.sleep(2)
web.find_element(By.CSS_SELECTOR, '#iptBtnEm').click()
time.sleep(2)

# 전체 주문 조회
web.get('https://{}.cafe24.com/admin/php/shop1/s_new/order_list.php') # {} mall name
# 날짜
web.execute_script(f"document.getElementById('startDate').value = '2023-10-01';")
time.sleep(2)
web.execute_script(f"document.getElementById('endDate').value = '2023-10-31';")
time.sleep(2)

# 상세검색
web.find_element(By.CSS_SELECTOR, '#QA_deposit1 > div.mOptionToogle > div > span > button').click()
time.sleep(2)

# 결제완료 체크
web.find_element(By.CSS_SELECTOR, '#QA_deposit1 > div.mOption.gDivision > table > tbody > tr:nth-child(1) > td > label:nth-child(6) > input').click()
time.sleep(2)

# 주문경로 체크
web.find_element(By.CSS_SELECTOR, '#QA_deposit1 > div.mOption.gDivision > table > tbody > tr:nth-child(4) > td:nth-child(2) > div > div.value > button').click()
time.sleep(0.5)
web.find_element(By.CSS_SELECTOR, '#QA_deposit1 > div.mOption.gDivision > table > tbody > tr:nth-child(4) > td:nth-child(2) > div > div.result > ul > li:nth-child(3) > label').click()

# 결제수단 체크
web.find_element(By.CSS_SELECTOR, '#QA_deposit1 > div.mOption.gDivision > table > tbody > tr:nth-child(5) > td:nth-child(4) > div > div.value > button').click()
time.sleep(0.5)
# 전체클릭
web.find_element(By.CSS_SELECTOR, '#QA_deposit1 > div.mOption.gDivision > table > tbody > tr:nth-child(5) > td:nth-child(4) > div > div.result > ul > li > label').click()
# 무통장 
web.find_element(By.CSS_SELECTOR, '#QA_deposit1 > div.mOption.gDivision > table > tbody > tr:nth-child(5) > td:nth-child(4) > div > div.result > ul > li > ul > li:nth-child(1) > label').click()
web.find_element(By.CSS_SELECTOR, '#search_button > span').click()

for i in range(0, 499):
    time.sleep(5)
    web.find_element(By.CSS_SELECTOR, '#copyarea_'+str(i)).click()
    time.sleep(5)
    web.switch_to.window(web.window_handles[-1])  
    # 금액 
    order_money = web.find_element(By.CSS_SELECTOR, '#payInfoDetail > div.detailView > ul > li:nth-child(3) > span').text
    time.sleep(5)
    order_num = web.find_element(By.CSS_SELECTOR, '#copyarea').text
    r = web.page_source
    soup = BeautifulSoup(r, 'html.parser')

    if str(soup).find('현금영수증 발급 내역이 없습니다.') != -1:
        print("없다!"+order_num, order_money)

        b = open("aaaa.txt",'a', encoding= 'utf-8')
        b.write(str(order_num)+' / '+str(order_money)+'\n')
        b.close()

        web.close()
        time.sleep(5)
        web.switch_to.window(web.window_handles[0])
        print(i)
    else:
        web.close()
        time.sleep(5)
        web.switch_to.window(web.window_handles[0])

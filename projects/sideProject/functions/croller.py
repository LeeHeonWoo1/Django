from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')

driver = webdriver.Chrome('./chromedriver.exe', options=options)

driver.get('https://www.saramin.co.kr/zf_user/jobs/list/domestic')
search_box_bef = driver.find_element(By.XPATH, '//*[@id="sri_header"]/div[1]/div[1]/button')
search_box_bef.click()
time.sleep(1)
search_box = driver.find_element(By.XPATH, '//*[@id="combineSearchWord"]')
search_btn = driver.find_element(By.XPATH, '//*[@id="submit_button"]')
time.sleep(2)

search_box.send_keys('python')
search_btn.click()

# driver.close()
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def dynamic_crawl(driver: webdriver, url: str):
    driver.get(url)
    time.sleep(5)

    iframe = driver.find_element(By.ID, "mainFrame")
    driver.switch_to.frame(iframe)

    source = driver.page_source
    html = BeautifulSoup(source, "html.parser")

    content = html.select("div.se-main-container")
    content = ''.join(str(content))

    # html태그제거 및 텍스트 다듬기
    content = re.sub(pattern=r'<[^>]*>', repl=r'', string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2, '')
    content = content.replace('\n', '')
    content = content.replace('\u200b', '')
    print(content)

from CrawlerInterface import CrawlingInterface
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
import re

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()  # 자동으로 chromedriver 설치
print("install done")

class NaverBlogCrawler(CrawlingInterface):
    def __init__(self, host: str, authId : str, authPw : str):
        super().__init__(host, authId, authPw)
        self.driver = webdriver.Chrome()

    def select(self, url : str, tags: list):
        self.driver.get(url)
        time.sleep(5)

        iframe = self.driver.find_element(By.ID, "mainFrame")
        self.driver.switch_to.frame(iframe)

        texts = []
        
        for tag in tags:
            try:
                text = self.driver.find_element(By.CSS_SELECTOR, tag).text
            except NoSuchElementException as e:
                text = self.handleNoSuchElementException(e, tag)

            texts.append(text)

        return texts


    def preprocess(self, desc : str) -> str:
        content = re.sub(pattern=r'<[^>]*>', repl=r'', string=desc)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        txt = content.replace(pattern2, '').replace('\n', ' ').replace('\u200b', '')

        return txt

    def postprocess(self, doc : dict, item) -> dict:
        doc["title"] = self.preprocess(item["title"])
        doc["date"] = datetime.strptime(item["postdate"], "%Y%m%d").strftime("%Y-%m-%d")
        return doc

    def handleNoSuchElementException(self, e, tag):
        #블로그 본문인 경우 구버전 고려
        if tag == 'div.se-main-container':
            text = self.driver.find_element(By.CSS_SELECTOR, 'div#content-area').text
        #elif로 태그 추가
        else:
            text = ""
        return text



    def __del__(self):
        super().__del__()


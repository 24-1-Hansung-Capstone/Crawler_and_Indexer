from CrawlerInterface import CrawlingInterface
from selenium import webdriver
from bs4 import BeautifulSoup
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
        self.url = None
        self.title = None

    def select(self, url : str, mainTag : str, titleTag : str):
        self.url = url
        self.driver.get(url)
        time.sleep(5)

        iframe = self.driver.find_element(By.ID, "mainFrame")
        self.driver.switch_to.frame(iframe)

        mainContent =  None
        try:
            mainContent = self.driver.find_element(By.CSS_SELECTOR, 'div.se-main-container').text
        # NoSuchElement 오류시 예외처리(구버전 블로그에 적용)
        except NoSuchElementException:
            mainContent = self.driver.find_element(By.CSS_SELECTOR, 'div#content-area').text

        print(mainContent)
        print(self.title)

        return mainContent, self.title


    def preprocess(self, desc : str) -> str:
        content = re.sub(pattern=r'<[^>]*>', repl=r'', string=desc)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        txt = content.replace(pattern2, '').replace('\n', ' ').replace('\u200b', '')


        print("crawled - preprocessed")
        print(txt)

        return txt

    def __del__(self):
        super().__del__()


from Interface import CrawlingInterface
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import time
import re

class NaverBlogCrawler(CrawlingInterface):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = None

    def select(self, url : str, tag : str):
        self.url = url
        self.driver.get(url)
        time.sleep(5)

        iframe = self.driver.find_element(By.ID, "mainFrame")
        self.driver.switch_to.frame(iframe)

        source = self.driver.page_source
        html = BeautifulSoup(source, "html.parser")

        content = html.select(tag)
        content = ''.join(str(content))

        return content


    def preprocess(self, desc : str) -> str:
        content = re.sub(pattern=r'<[^>]*>', repl=r'', string=desc)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""

        return content.replace(pattern2, '').replace('\n', ' ').replace('\u200b', '')

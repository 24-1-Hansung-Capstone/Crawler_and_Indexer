from Interface import CrawlingInterface
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import time
import re

class NaverBlogCrawler(CrawlingInterface):
    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome()
        self.url = None

    def select(self, url : str, mainTag : str, titleTag : str):
        self.url = url
        self.driver.get(url)
        time.sleep(5)

        iframe = self.driver.find_element(By.ID, "mainFrame")
        self.driver.switch_to.frame(iframe)

        source = self.driver.page_source
        html = BeautifulSoup(source, "html.parser")

        mainContent = html.select(mainTag)
        mainContent = ''.join(str(mainContent))

        titleContent = html.select(titleTag)
        titleContent = ''.join(str(titleContent))

        return mainContent, titleContent


    def preprocess(self, desc : str) -> str:
        content = re.sub(pattern=r'<[^>]*>', repl=r'', string=desc)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        txt = content.replace(pattern2, '').replace('\n', ' ').replace('\u200b', '')

        return txt

    def __del__(self):
        super().__del__()

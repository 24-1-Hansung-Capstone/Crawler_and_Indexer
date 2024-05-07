from CrawlerInterface import CrawlingInterface
from selenium import webdriver
from selenium.webdriver.common.by import By

import re

class Realty_Crawler(CrawlingInterface):
    def __init__(self, host: str, authId: str, authPw: str):
        super().__init__(host, authId, authPw)
        self.driver = webdriver.Chrome()

    def select(self, url: str, tags: list):
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        texts = []

        for tag in tags:
            try:
                text = self.driver.find_element(By.CSS_SELECTOR, tag).text
            except:
                print(f"Skipping link {url} due to missing title tag")
                return None
            texts.append(text)
        return texts


    def preprocess(self, desc : str) -> str:
        content = re.sub(pattern=r'<[^>]*>', repl=r'', string=desc)
        pattern1 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        txt = content.replace(pattern1, '').replace('\n', ' ').replace('\u200b', '')
        return txt


    def postprocess(self, doc : dict, item) -> dict:
        return doc
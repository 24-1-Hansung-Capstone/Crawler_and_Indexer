from Interface import CrawlingInterface
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import requests
import re
import time

class NaverNewsCrawler(CrawlingInterface):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def select(self, url : str, tag : str):
        self.driver.get(url)
        self.driver.implicitly_wait(3)

        source = self.driver.page_source
        html = BeautifulSoup(source, "html.parser")

        content = html.select(tag)
        content = ''.join(str(content))

        return content


    def preprocess(self, desc : str) -> str:
        content = re.sub(pattern=r'<[^>]*>', repl=r'', string=desc)
        pattern1 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""

        return content.replace(pattern1, '').replace('\n', ' ').replace('\u200b', '')
    
        
    # 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
    # 입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
    def makePgNum(self,num):
        if num == 1:
            return num
        elif num == 0:
            return num + 1
        else:
            return num + 9 * (num - 1)
     
    # 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
    def makeUrl(self,search, start_pg, end_pg):
        if start_pg == end_pg:
            start_page = self.makePgNum(start_pg)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(
                start_page)
            print("생성url: ", url)
            return url
        else:
            urls = []
            for i in range(start_pg, end_pg + 1):
                page = self.makePgNum(i)
                url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
                urls.append(url)
            print("생성url: ", urls)
            return urls
      
    # 네이버기사의 URL만 추출
    def extractUrl(self,search_urls,naver_urls):
        for i in search_urls:
            self.driver.get(i)
            time.sleep(1)  # 대기시간 변경 가능
    
            # 네이버 기사 눌러서 제목 및 본문 가져오기#
            # 네이버 기사가 있는 기사 css selector 모아오기
            a = self.driver.find_elements(By.CSS_SELECTOR, 'a.info')
    
            # 위에서 생성한 css selector list 하나씩 클릭하여 본문 url얻기
            for i in a:
                i.click()
    
                # 현재탭에 접근
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(3)  # 대기시간 변경 가능
    
                # 네이버 뉴스 url만 가져오기
    
                url = self.driver.current_url
                print(url)
    
                if "news.naver.com" in url:
                    naver_urls.append(url)
    
                else:
                    pass
                # 현재 탭 닫기
                self.driver.close()
                # 다시처음 탭으로 돌아가기(매우 중요!!!)
                self.driver.switch_to.window(self.driver.window_handles[0])
                
            return naver_urls
        
        
from CrawlerInterface import CrawlingInterface
from selenium import webdriver
from selenium.webdriver.common.by import By

import re

class NaverNewsCrawler(CrawlingInterface):
    def __init__(self, host: str, authId: str, authPw: str):
        super().__init__(host, authId, authPw)
        self.driver = webdriver.Chrome()

    def select(self, url : str, tags: list):
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        texts = []

        for tag in tags:
            print(tag)
            if tag == "meta":  # 동아일보 date 태그
                og_pubdate_content = (self.driver.find_element(By.XPATH, '/html/head/meta[17]')
                                      .get_attribute('content'))
                text = og_pubdate_content
            elif tag == "span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME":  # 네이버페이 부동산 뉴스 입력날짜
                date = str((self.driver.find_element(By.XPATH, '//*[@id="ct"]/div[1]/div[3]/div[1]/div/span')
                           .get_attribute('data-date-time')))
                text = date
            elif tag == "#article_body.article_body.fs3 > p":  # 중앙일보 내용
                elements = self.driver.find_elements(By.CSS_SELECTOR, tag)  # 복수의 요소를 찾습니다.
                text = ' '.join([element.text for element in elements])  # 각 요소의 텍스트를 추출하여 합칩니다.
            elif tag == "div.article-text > p.text":  # 한겨레 내용
                elements = self.driver.find_elements(By.CSS_SELECTOR, tag)  # 복수의 요소를 찾습니다.
                text = ' '.join([element.text for element in elements])  # 각 요소의 텍스트를 추출하여 합칩니다.
            else:
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


    def postprocess(self, doc : dict, item) -> dict: #언론사마다 date형식이 다르기 때문에 후처리 함수를 하위클래스에서 구현
        return doc







    
    #
    # # 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
    # # 입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
    # def makePgNum(self,num):
    #     if num == 1:
    #         return num
    #     elif num == 0:
    #         return num + 1
    #     else:
    #         return num + 9 * (num - 1)
    #
    # # 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
    # def makeUrl(self,search, start_pg, end_pg):
    #     if start_pg == end_pg:
    #         start_page = self.makePgNum(start_pg)
    #         url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(
    #             start_page)
    #         print("생성url: ", url)
    #         return url
    #     else:
    #         urls = []
    #         for i in range(start_pg, end_pg + 1):
    #             page = self.makePgNum(i)
    #             url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
    #             urls.append(url)
    #         print("생성url: ", urls)
    #         return urls
    #
    # # 네이버기사의 URL만 추출
    # def extractUrl(self,search_urls,naver_urls):
    #     for i in search_urls:
    #         self.driver.get(i)
    #         time.sleep(1)  # 대기시간 변경 가능
    #
    #         # 네이버 기사 눌러서 제목 및 본문 가져오기#
    #         # 네이버 기사가 있는 기사 css selector 모아오기
    #         a = self.driver.find_elements(By.CSS_SELECTOR, 'a.info')
    #
    #         # 위에서 생성한 css selector list 하나씩 클릭하여 본문 url얻기
    #         for i in a:
    #             i.click()
    #
    #             # 현재탭에 접근
    #             self.driver.switch_to.window(self.driver.window_handles[1])
    #             time.sleep(3)  # 대기시간 변경 가능
    #
    #             # 네이버 뉴스 url만 가져오기
    #
    #             url = self.driver.current_url
    #             print(url)
    #
    #             if "news.naver.com" in url:
    #                 naver_urls.append(url)
    #
    #             else:
    #                 pass
    #             # 현재 탭 닫기
    #             self.driver.close()
    #             # 다시처음 탭으로 돌아가기(매우 중요!!!)
    #             self.driver.switch_to.window(self.driver.window_handles[0])
    #
    #         return naver_urls
    #
        
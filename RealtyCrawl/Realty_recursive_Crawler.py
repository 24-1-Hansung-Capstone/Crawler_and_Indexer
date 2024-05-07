import urllib.request
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver

from RealtyCrawler.Realty_Crawler import Realty_Crawler
from datetime import datetime
import time

class Realty_recursive_Crawler(Realty_Crawler):
    def __init__(self, host, authId, authPw):
        # 부모 클래스의 생성자 호출
        super().__init__(host, authId, authPw)
    def postprocess(self, doc: dict, item) -> dict:
        date_str = doc["date"].split()[-1]
        date_obj = datetime.strptime(date_str, "%y.%m.%d")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        doc["date"] = formatted_date
        return doc

#id 지정
RealtyCrawler = Realty_recursive_Crawler(host="http://43.202.45.47:9200", authId ="elastic", authPw="changeme")
driver = webdriver.Chrome()

#검색어 지정
url = driver.get("https://www.r114.com/?_c=memul&_m=p10")
# #request
# request = urllib.request.Request(url)
#
# #response 받기
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
links = []
#
# #결과 파싱
# if(rescode == 200):
#     response_body = response.read()
for page_number in range(1, 8):
    # JavaScript 코드 실행
    driver.execute_script(f"goPage({page_number}, 1)")
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    header_tags = soup.find_all('ul', class_='list_article.Best')
    for header_tag in header_tags:
        a_tags = header_tag.find_all('a')
        for a_tag in a_tags:
            onclick_value = a_tag.get('onclick')
            # 추출된 onclick 속성 값에서 매묿번호 "R2405071107909" 값을 추출
            value_start_index = onclick_value.find('\'') + 1
            value_end_index = onclick_value.find('\'', value_start_index)
            extracted_value = onclick_value[value_start_index:value_end_index]
            links.append("https://www.r114.com/?_c=memul&_m=HouseDetail&mulcode=" + extracted_value)
    # 1초 대기 (페이지가 로드될 때까지 충분한 시간을 기다립니다)
    time.sleep(1)

# else:
#     print("Error Code:" + rescode)
#     exit(rescode)

#크롤링
i = 0
print(links)
for link in links:
    i += 1
    print(link)
    print(RealtyCrawler.crawl(link, "realty", ["div.name", "div.build_price > div.mode", "div.build_price > div.value", "div.basic_area", "div.basic_opt", "dl.info_item_list > dd", "div.tag.type08"],
                                 ["title", "mode", "price", "desc", "option", "location", "date"]))

driver.quit()

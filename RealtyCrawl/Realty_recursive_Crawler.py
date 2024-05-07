import urllib.request
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver

from RealtyCrawler.Realty_Crawler import Realty_Crawler
import time

class Realty_recursive_Crawler(Realty_Crawler):
    def __init__(self, host, authId, authPw):
        # 부모 클래스의 생성자 호출
        super().__init__(host, authId, authPw)
    # def postprocess(self, doc: dict, item) -> dict:
    #     input_string = doc["date"].split()[1]
    #
    #     match = re.search(r"확인 (\d{2}.\d{2}.\d{2})", input_string)
    #     if match:
    #         date_str = match.group(1)
    #
    #         # 년도를 현재 년도로 가정하여 완전한 ISO 형식의 날짜로 변환
    #         date_iso = datetime.strptime(date_str, "%y.%m.%d").strftime("%Y-%m-%d")
    #         print(date_iso)
    #     else:
    #         print("날짜를 찾을 수 없습니다.")
    #         date_iso = ""
    #
    #     doc["date"] = date_iso
    #     return doc

#id 지정
RealtyCrawler = Realty_recursive_Crawler(host="http://localhost:9200", authId ="elastic", authPw="elastic")
driver = webdriver.Chrome()

# #검색어 지정
url = driver.get("https://www.r114.com/?_c=memul&_m=p10")
# #request
# request = urllib.request.Request(url)
#
# #response 받기
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
links = []
# #결과 파싱
# if(rescode == 200):
#     response_body = response.read()
for page_number in range(1, 8):
    # JavaScript 코드 실행
    time.sleep(5)
    driver.execute_script(f"goPage({page_number}, 1)")
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    a_tags = soup.find_all('a', class_='cont')
    for a_tag in a_tags:
        onclick_value = a_tag.get('onclick')
        # 추출된 onclick 속성 값에서 매물번호 "R2405071107909" 값을 추출
        value_start_index = onclick_value.find('\'') + 1
        value_end_index = onclick_value.find('\'', value_start_index)
        extracted_value = onclick_value[value_start_index:value_end_index]
        links.append("https://www.r114.com/?_c=memul&_m=HouseDetail&mulcode=" + extracted_value)
    print(links)
    print(len(links))

# else:
#     print("Error Code:" + rescode)
#     exit(rescode)

#크롤링
i = 0
print(links)
for link in links:
    i += 1
    print(link)
    print(RealtyCrawler.crawl(link, "realty", ["div.build_area > div.name", "div.build_price > div.mode", "div.build_price > div.value", "div.basic_area > div > summary", "div.basic_opt", "section#view_danji > div.info_wrap > div > dl.info_item_list > dd"],
                                 ["title", "mode", "price", "desc", "option", "location"]))

driver.quit()

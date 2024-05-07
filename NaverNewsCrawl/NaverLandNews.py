import urllib.request
import urllib.parse

from selenium import webdriver
from bs4 import BeautifulSoup

from NaverNewsCrawler.Naver_News_Crawler import NaverNewsCrawler
from datetime import datetime

class NaverLandNews(NaverNewsCrawler):
    def __init__(self, host, authId, authPw):
        # 부모 클래스의 생성자 호출
        super().__init__(host, authId, authPw)
    def postprocess(self, doc: dict, item) -> dict:
        date_str = doc["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        doc["date"] = formatted_date
        return doc

#id 지정
NewsCrawler = NaverLandNews(host="http://43.202.45.47:9200", authId ="elastic", authPw="elastic")
driver = webdriver.Chrome()
# #검색어 지정
urls = []
for i in range(1, 10):
    url = "https://land.naver.com/news/headline.naver?bss_ymd=20240507&page=" + str(i)  # JSON 결과
    urls.append(url)
# 웹 페이지 열기
for url in urls:
    driver.get(url)

    # for url in urls:
    #     #request
    #     request = urllib.request.Request(url)
    #
    #     #response 받기
    #     response = urllib.request.urlopen(request)
    #     rescode = response.getcode()
    links = []
    #
    #     #결과 파싱
    #     if(rescode == 200):
    #         response_body = response.read()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    div_tags = soup.select('div#content')
    ul_tags = soup.find_all('ul', class_="land_news_list")
    print("Number of ul tags found:", len(ul_tags))  # Add this line for debugging
    for ul_tag in ul_tags:
        a_tags = ul_tag.find_all('a')
        for a_tag in a_tags:
            print(a_tag)
            href = a_tag.get('href')
            if "https://n.news.naver.com" in href:
                links.append(href)
        #
        # else:
        #     print("Error Code:" + rescode)
        #     exit(rescode)

    #크롤링
    i = 0
    print(links)
    for link in links:
        i += 1
        print(link)
        print(NewsCrawler.crawl(link, "news", ["article#dic_area.go_trans._article_content", "h2#title_area span", "span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME"],
                                     ["mainBody", "title", "date"]))
driver.quit()

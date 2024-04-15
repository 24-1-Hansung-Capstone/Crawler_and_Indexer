import urllib.request
import urllib.parse

from bs4 import BeautifulSoup

from NaverNewsCrawler.Naver_News_Crawler import NaverNewsCrawler
from datetime import datetime

class DongaNews(NaverNewsCrawler):
    def __init__(self, host, authId, authPw):
        # 부모 클래스의 생성자 호출
        super().__init__(host, authId, authPw)
    def postprocess(self, doc: dict, item) -> dict:
        date_str = doc["date"]
        # print(date_str, " : ")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        doc["date"] = formatted_date
        return doc

#id 지정
NewsCrawler = DongaNews(host="http://43.202.45.47:9200", authId ="elastic", authPw="changeme")

#검색어 지정
urls = []
encText = urllib.parse.quote("보문역")
for i in range(1, 41, 10):
    url = "https://www.donga.com/news/search?p=" + str(i) + "&query=" + encText + "&check_news=91&sorting=1&search_date=1&v1=&v2=&more=1" # JSON 결과
    urls.append(url)

for url in urls:
    #request
    request = urllib.request.Request(url)

    #response 받기
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    links = []

    #결과 파싱
    if(rescode == 200):
        response_body = response.read()
        soup = BeautifulSoup(response_body, 'html.parser')
        header_tags = soup.find_all('header', class_='news_head')
        for header_tag in header_tags:
            a_tags = header_tag.find_all('a')
            for a_tag in a_tags:
                href = a_tag.get('href')
                if "https://www.donga.com" in href:
                    links.append(href)

    else:
        print("Error Code:" + rescode)
        exit(rescode)

    #크롤링
    i = 0
    print(links)
    for link in links:
        i += 1
        print(link)
        print(NewsCrawler.crawl(link, "news", ["section.news_view", "section.head_group > h1", "meta"],
                                     ["mainBody", "title", "date"]))


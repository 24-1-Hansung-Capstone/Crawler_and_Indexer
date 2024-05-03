import urllib.request
import urllib.parse

from bs4 import BeautifulSoup

from NaverNewsCrawler.Naver_News_Crawler import NaverNewsCrawler
from datetime import datetime

class HangyureNews(NaverNewsCrawler):
    def __init__(self, host, authId, authPw):
        # 부모 클래스의 생성자 호출
        super().__init__(host, authId, authPw)
    def postprocess(self, doc: dict, item) -> dict:
        date_str = doc["date"]
        # print(date_str, " : ")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        doc["date"] = formatted_date
        return doc

#id 지정
NewsCrawler = HangyureNews(host="http://43.202.45.47:9200", authId ="elastic", authPw="changeme")

#검색어 지정
urls = []
now = datetime.now()
date = now.strftime("%Y.%m.%d")
encText = urllib.parse.quote("강남역")
for i in range(1,3):
    url = "https://search.hani.co.kr/search/newslist?searchword=%EA%B0%95%EB%82%A8%EC%97%AD&startdate=1988.01.01&enddate="+date+"&page=" + encText + "&startdate=1988.01.01&enddate=2024.04.08&page=" + str(i) + "&sort=desc" # JSON 결과
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
        header_tags = soup.find_all('article')
        for header_tag in header_tags:
            a_tags = header_tag.find_all('a', class_='flex-inner')
            for a_tag in a_tags:
                href = a_tag.get('href')
                if "https://www.hani.co.kr/" in href:
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
        result = NewsCrawler.crawl(link, "news", ["div.article-text > p.text", "h3.ArticleDetailView_title__fDOCx", "li.ArticleDetailView_dateListItem__6uf9E > span"],
                                     ["mainBody", "title", "date"]) #h3.ArticleDetailView_title__i0jb9을 만나면 끊김
        if result is None:
            continue
        print(result)

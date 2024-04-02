import urllib.request
import urllib.parse
import json

from NaverNewsCrawl.NaverNewsCrawler import Naver_News_Crawler

#id 지정
NewsCrawler = Naver_News_Crawler.NaverNewsCrawler(host="https://localhost:9200", authId ="elastic", authPw="cAh+sWnbfRlXz1KimBpp")

#검색어 지정
encText = urllib.parse.quote("성북구")
url = "https://www.joongang.co.kr/search?keyword=" + encText # JSON 결과

#request
request = urllib.request.Request(url)

#response 받기
response = urllib.request.urlopen(request)
rescode = response.getcode()

#결과 파싱
if(rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
    search_result = json.loads(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
    exit(rescode)

#크롤링
i = 0
for item in search_result["items"]:
    i += 1
    NewsCrawler.title = item["title"]
    print(NewsCrawler.crawl(item["link"], "news", ["div.article_body fs3", "header.article_header > h1.headline", "span.is_blind"],
                                 ["mainBody", "title", "date"], item))


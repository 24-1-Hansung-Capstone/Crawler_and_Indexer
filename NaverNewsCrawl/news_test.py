import urllib.request
import urllib.parse
import json

from NaverNewsCrawl.NaverNewsCrawler import Naver_News_Crawler

#id 지정
NAVER_CLIENT_ID = "Pwl2n4GWNec7VL_RqRGP"
NAVER_CLIENT_SECRET = "HJq5tjv7HY"
naverNewsCrawler = Naver_News_Crawler.NaverNewsCrawler(host="https://localhost:9200", authId ="elastic", authPw="cAh+sWnbfRlXz1KimBpp")

#검색어 지정
encText = urllib.parse.quote("성북구")
url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과

#request
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",NAVER_CLIENT_ID)
request.add_header("X-Naver-Client-Secret",NAVER_CLIENT_SECRET)

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
    naverNewsCrawler.title = item["title"]
    print(naverNewsCrawler.crawl(item["link"], "news", ["#dic_area", "#title_area > span", "span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME"],
                                 ["mainBody", "title", "date"], item))


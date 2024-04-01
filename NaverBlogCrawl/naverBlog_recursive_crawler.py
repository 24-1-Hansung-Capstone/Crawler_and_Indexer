import urllib.request
import json

from NaverBlogCrawler import Naver_blog_crawler

#id 지정
NAVER_CLIENT_ID = "Pwl2n4GWNec7VL_RqRGP"
NAVER_CLIENT_SECRET = "HJq5tjv7HY"
naverBlogCrawler = Naver_blog_crawler.NaverBlogCrawler(host="https://localhost:9200", authId ="elastic", authPw="cAh+sWnbfRlXz1KimBpp") #cAh+sWnbfRlXz1KimBp

#검색어 지정
encText = urllib.parse.quote("월계역")
url = "https://openapi.naver.com/v1/search/blog?query=" + encText  # JSON 결과

#request
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)

#response 받기
response = urllib.request.urlopen(request)
rescode = response.getcode()

#결과 파싱
if (rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
    search_result = json.loads(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
    exit(rescode)

#크롤링
i = 0
for item in search_result["items"]:
    i+=1
    naverBlogCrawler.title = item["title"]
    print(naverBlogCrawler.crawl(item["link"], "blog2", ["div.se-main-container", "span.se-fs-","span.se_publishDate"], ["mainBody", "title", "date"], item))


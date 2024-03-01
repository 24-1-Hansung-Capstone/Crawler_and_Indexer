import urllib.request
import json

import Naver_blog_crawler

#id 지정
NAVER_CLIENT_ID = "Pwl2n4GWNec7VL_RqRGP"
NAVER_CLIENT_SECRET = "HJq5tjv7HY"
naverBlogCrawler = Naver_blog_crawler.NaverBlogCrawler()

#검색어 지정
encText = urllib.parse.quote("보문역")
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
for item in search_result["items"]:
    desc = naverBlogCrawler.select(item["link"], "div.se-main-container")
    print(naverBlogCrawler.preprocess(desc))






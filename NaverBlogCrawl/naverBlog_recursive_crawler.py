import urllib.request
import json

from NaverBlogCrawler import Naver_blog_crawler

#id 지정
NAVER_CLIENT_ID = "Pwl2n4GWNec7VL_RqRGP"
NAVER_CLIENT_SECRET = "HJq5tjv7HY"
naverBlogCrawler = Naver_blog_crawler.NaverBlogCrawler(host="http://221.142.15.180:9200", authId ="elastic", authPw="elastic") #cAh+sWnbfRlXz1KimBp

i = 0
# 파일을 열고 'file'이라는 변수에 저장합니다.
with open('../searchWords.txt', 'r', encoding='utf-8') as file:
    # 파일 1줄 반복
    for line in file:

        # 검색어 지정
        encText = urllib.parse.quote(line.strip())
        url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "display=100"  # JSON 결과

        # request
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
        request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)

        # response 받기
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        # 결과 파싱
        if (rescode == 200):
            response_body = response.read()
            search_result = json.loads(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
            exit(rescode)

        # 크롤링
        for item in search_result["items"]:
            i += 1
            naverBlogCrawler.title = item["title"]
            print(naverBlogCrawler.crawl(item["link"], "blog",
                                         ["div.se-main-container", "span.se-fs-", "span.se_publishDate"],
                                         ["mainBody", "title", "date"], item))

# url = "https://openapi.naver.com/v1/search/blog?query=" + "보문"  # JSON 결과
#
# # request
# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
# request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)
#
# # response 받기
# response = urllib.request.urlopen(request)
# rescode = response.getcode()
#
# # 결과 파싱
# if (rescode == 200):
#     response_body = response.read()
#     print(response_body.decode('utf-8'))
#     search_result = json.loads(response_body.decode('utf-8'))
# else:
#     print("Error Code:" + rescode)
#     exit(rescode)
#
# # 크롤링
# i = 0
# for item in search_result["items"]:
#     i += 1
#     naverBlogCrawler.title = item["title"]
#     print(naverBlogCrawler.crawl(item["link"], "blog",
#                                  ["div.se-main-container", "span.se-fs-", "span.se_publishDate"],
#                                  ["mainBody", "title", "date"], item))
#
#

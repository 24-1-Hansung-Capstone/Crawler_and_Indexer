import urllib.request
import json
from selenium import webdriver
import re
from crawler import crawler_requests
from crawler import crawler_selenium

#id 지정
client_id = "Pwl2n4GWNec7VL_RqRGP"
client_secret = "HJq5tjv7HY"
api_data = None

#검색어 지정
encText = urllib.parse.quote("보문역")
url = "https://openapi.naver.com/v1/search/blog?query=" + encText  # JSON 결과

#request 생성
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

#request
response = urllib.request.urlopen(request)
rescode = response.getcode()

#결과 파싱
if (rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
    api_data = json.loads(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)
    exit(rescode)

#크롤링
driver = webdriver.Chrome()
for item in api_data["items"]:
    crawler_selenium.dynamic_crawl(driver, item["link"])
    #crawler_requests.static_crawl(item["link"])

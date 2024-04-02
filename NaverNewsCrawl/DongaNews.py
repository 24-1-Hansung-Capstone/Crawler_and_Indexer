import urllib.request
import urllib.parse
import json

from bs4 import BeautifulSoup

from NaverNewsCrawl.NaverNewsCrawler import Naver_News_Crawler

#id 지정
NewsCrawler = Naver_News_Crawler.NaverNewsCrawler(host="http://13.125.6.140:9200", authId ="elastic", authPw="changeme")

#검색어 지정
encText = urllib.parse.quote("보문역")
url = "https://www.donga.com/news/search?query=" + encText # JSON 결과

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


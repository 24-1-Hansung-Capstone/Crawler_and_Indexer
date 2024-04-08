import urllib.request
import urllib.parse
import json

from bs4 import BeautifulSoup

from NaverNewsCrawl.NaverNewsCrawler import Naver_News_Crawler

#id 지정
NewsCrawler = Naver_News_Crawler.NaverNewsCrawler(host="http://13.125.6.140:9200", authId ="elastic", authPw="changeme")

#검색어 지정
search_term = "강남역"
encText = urllib.parse.quote(search_term.encode('utf-16'))
url = "https://www.kmib.co.kr/search/searchResult.asp?searchWord=" + encText # JSON 결과

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
    header_tags = soup.find_all('dt', class_='tit')
    for header_tag in header_tags:
        a_tags = header_tag.find_all('a')
        for a_tag in a_tags:
            href = a_tag.get('href')
            if "https://www.kmib.co.kr" in href:
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
    print(NewsCrawler.crawl(link, "news", ["div#articleBody.tx", "h1.article_headline", "span.t11"],
                                 ["mainBody", "title", "date"]))


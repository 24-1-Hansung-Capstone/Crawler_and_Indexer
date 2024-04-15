import urllib.request
import urllib.parse
import json

from bs4 import BeautifulSoup

from NaverNewsCrawl.NaverNewsCrawler import Naver_News_Crawler

#id 지정
NewsCrawler = Naver_News_Crawler.NaverNewsCrawler(host="http://43.202.45.47:9200", authId ="elastic", authPw="changeme")

#검색어 지정
urls = []
search_term = "강남역"
encText = urllib.parse.quote(search_term, encoding='utf-16')

for i in range(1,3):
    url = "https://www.kmib.co.kr/search/searchResult.asp?searchWord=" + encText + "&pageNo=" + str(i) + "&period=" #JSON 결과
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
        header_tags = soup.find_all('div', class_='search_nws')
        for header_tag in header_tags:
            a_tags = header_tag.find_all('a')
            for a_tag in a_tags:
                href = a_tag.get('href')
                if "https://www.kmib.co.kr" in href and href not in links:
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


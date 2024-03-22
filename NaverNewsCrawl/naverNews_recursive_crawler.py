# 크롤링시 필요한 라이브러리 불러오기
from NaverNewsCrawl.NaverNewsCrawler import Naver_News_Crawler

#크롤러 생성
naverNewsCrawler = Naver_News_Crawler.NaverNewsCrawler()


##########뉴스크롤링 시작###################

# 검색어 입력
search = input("검색할 키워드를 입력해주세요:")

# 검색 시작할 페이지 입력
page = int(input("\n크롤링할 시작 페이지를 입력해주세요. ex)1(숫자만입력):"))  # ex)1 =1페이지,2=2페이지...
print("\n크롤링할 시작 페이지: ", page, "페이지")
# 검색 종료할 페이지 입력
page2 = int(input("\n크롤링할 종료 페이지를 입력해주세요. ex)1(숫자만입력):"))  # ex)1 =1페이지,2=2페이지...
print("\n크롤링할 종료 페이지: ", page2, "페이지")

# url 생성
search_urls = naverNewsCrawler.makeUrl(search, page, page2)

## selenium으로 navernews만 뽑아오기##

# selenium으로 검색 페이지 불러오기 #

naver_urls = []

naver_urls = naverNewsCrawler.extractUrl(search_urls, naver_urls)

print(naver_urls)

###naver 기사 본문 및 제목 가져오기###

# ConnectionError방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

titles = []
contents = []
for i in naver_urls:
    
    # 뉴스 제목 가져오기 및 전처리
    title = naverNewsCrawler.select(i,"div#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
    title = naverNewsCrawler.preprocess(title)
    titles.append(title)

    # 뉴스 본문 가져오기 및 전처리 
    content = naverNewsCrawler.select(i,"#dic_area")
    content = naverNewsCrawler.preprocess(content)
    contents.append(content)

print(titles)
print(contents)

# 데이터프레임으로 정리(titles,url,contents)
import pandas as pd

news_df = pd.DataFrame({'title': titles, 'link': naver_urls, 'content': contents})

news_df.to_csv('NaverNews_%s.csv' % search, index=False, encoding='utf-8-sig')
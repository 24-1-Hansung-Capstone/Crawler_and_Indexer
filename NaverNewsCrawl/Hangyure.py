import urllib.request
import urllib.parse

from bs4 import BeautifulSoup

from NaverNewsCrawler.Naver_News_Crawler import NaverNewsCrawler
from datetime import datetime

class HangyureNews(NaverNewsCrawler):
    def __init__(self, host, authId, authPw):
        # 부모 클래스의 생성자 호출
        super().__init__(host, authId, authPw)
    def postprocess(self, doc: dict, item) -> dict:
        date_str = doc["date"]
        # print(date_str, " : ")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        formatted_date = date_obj.strftime("%Y-%m-%d")
        doc["date"] = formatted_date
        return doc

#id 지정
NewsCrawler = HangyureNews(host="http://221.142.15.180:9200", authId ="elastic", authPw="elastic")

# 검색어 파일 읽기
with open("../hangyure.txt", "r", encoding='UTF-8') as file:
    search_words = file.readlines()

# 추가할 단어 목록
additional_keywords = ["부동산", "전세", "월세", "매매", "임대"]

# 검색어별로 처리
for word in search_words:
    word = word.strip()  # 단어 좌우의 공백 제거
    for keyword in additional_keywords:
        search_term = f"{word} {keyword}"  # 단어와 추가 키워드 결합
        encText = urllib.parse.quote(search_term)  # 인코딩
        urls = []
        print(f"검색어: {search_term}")
        now = datetime.now()
        date = now.strftime("%Y.%m.%d")
        for i in range(1,4):
            url = "https://search.hani.co.kr/search/newslist?searchword="+encText+"&startdate=1988.01.01&enddate="+date+"&page="+str(i)+"&sort=desc" # JSON 결과
            urls.append(url)

        for url in urls:
            try:
                #request
                request = urllib.request.Request(url)
                # Response 받기 (타임아웃 3분 설정)
                response = urllib.request.urlopen(request, timeout=180)
                rescode = response.getcode()
                links = []

                #결과 파싱
                if(rescode == 200):
                    response_body = response.read()
                    soup = BeautifulSoup(response_body, 'html.parser')
                    header_tags = soup.find_all('article')
                    for header_tag in header_tags:
                        a_tags = header_tag.find_all('a', class_='flex-inner')
                        for a_tag in a_tags:
                            href = a_tag.get('href')
                            if "https://www.hani.co.kr/" in href:
                                links.append(href)

                else:
                    print("Error Code:" + rescode)
                    exit(rescode)

                #크롤링
                i = 0
                print(links)
                for link in links:
                    i += 1
                    if (i == 40):
                        NewsCrawler = HangyureNews(host="http://221.142.15.180:9200", authId="elastic", authPw="elastic")

                        i = 0
                    print(link)
                    result = NewsCrawler.crawl(link, "news", ["div.article-text > p.text", "h3.ArticleDetailView_title__9kRU_", "li.ArticleDetailView_dateListItem__mRc3d > span"],
                                                 ["mainBody", "title", "date"]) #h3.ArticleDetailView_title__i0jb9을 만나면 끊김
                    if result is None:
                        continue
                    print(result)

            except Exception as e:
                print(f"Error processing {url}: {e}")

import bs4
from bs4 import BeautifulSoup as bs
import requests
import os

url = "https://ko.wikipedia.org/wiki/수도권_전철역_목록?oldformat=true"
fileDir = "../searchWords.txt"
res = requests.get(url)
table = bs(res.text, 'html.parser').findAll('tr')

with open(fileDir, 'r') as f:
    exist_data = f.read()

with open(fileDir, 'w') as f:
    # 기존 내용 유지
    f.write(f"{exist_data}\n")

    # 새로운 내용 추가
    for tag in table:
        try :
            # 실제 데이터가 있는 부분들을 가져온다.
            # t[0] : 역이름
            # t[1] : 영문 역이름
            # t[2] : 소재지(지역)
            # t[3] : 지나가는 호선 번호
            t = tag.find_all('td')

            # 서울 소재가 아니거나, 역정보가 아닌 다른 정보면 패스
            if "서울" not in t[2].text or "-" in t[0].text: continue

            # 논현\n논현역 << 이런식으로 저장한다.
            f.write(f"{t[0].text}\n")
            f.write(f"{t[0].text}역\n")

        # 예외나면 그냥 버린다. 우리가 찾을 정보가 있는 부분에선 예외가 나지 않는다.
        except:
            continue
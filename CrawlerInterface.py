from elasticsearch import Elasticsearch

from konlpy.tag import Okt
from collections import Counter

class MethodNotImplementError(Exception) :
    def __init__(self, methodName=""):
        self.errorMsg = f"{methodName} Method is not implements."
        super().__init__(self.errorMsg)

class CrawlingInterface :
    def __init__(self, host: str, authId : str, authPw : str, isEstate : bool = False):
        self.es = Elasticsearch(hosts=host, basic_auth=(authId, authPw), verify_certs=False)
        self.isEstate = isEstate
        self.real_estate_terms = [
            "부동산", "아파트", "주택", "상가", "오피스텔", "빌라", "매매", "전세", "월세", "임대", "가구", "복합", "대명"
            "매물", "계약", "청약", "분양", "재건축", "재개발", "리모델링", "등기", "건축", "토지", "용지", "래미안",
            "건물", "상가건물", "단독주택", "연립주택", "다가구주택", "주상복합", "상업용지", "주거용지", "상업지역", "주거",
            "공시지가", "감정평가", "중개사", "공인중개사", "부동산중개", "부동산투자", "부동산개발", "단지", "영등포", "강동구"
            "부동산시장", "부동산가격", "매입", "매도", "양도소득세", "취득세", "보유세", "종합부동산세", "하남스타포레", "신축"
            "부동산세", "임대료", "보증금", "관리비", "전월세전환율", "대출", "담보대출", "주택담보대출",
            "이자율", "금리", "주택자금", "임대사업자", "주택공급", "분양가", "전세가율", "청약통장",
            "주택연금", "역세권", "도시개발", "뉴타운", "스마트시티", "미분양", "건축비", "건축자재",
            "주거환경", "부동산정책", "부동산규제", "임대차보호법", "재산세", "소유권", "공동소유",
            "부동산임대", "상가임대", "지분", "입주", "잔금", "계약금", "중도금", "임대차계약",
            "재계약", "임차인", "임대인", "소유주", "매도인", "매수인", "거래가격", "거래량"
        ]

    def keyword_extractor(self, tagger, text, k):
        tokens = tagger.phrases(text)
        tokens = [token for token in tokens if len(token) > 1]  # 한 글자인 단어는 제외
        count_dict = [(token, text.count(token)) for token in tokens]
        ranked_words = sorted(count_dict, key=lambda x: x[1], reverse=True)[:k]
        return [keyword for keyword, freq in ranked_words]

    def contains_any(self, main_list):
        return any(item in main_list for item in self.real_estate_terms)


    def crawl(self, url : str, esIndex : str, tags : list, keys : list, item = None):
        try:
            texts = self.select(url, tags)

            if texts is None:
                return None

            texts = list(map(self.preprocess, texts))
            doc = dict(zip(keys, texts))
            doc["url"] = url
            doc = self.postprocess(doc, item)

            if self.isEstate:
                okt = Okt()
                k_word_lists = self.keyword_extractor(okt, doc["mainBody"], 10)
                print(k_word_lists)
                if not self.contains_any(k_word_lists):
                    return "부동산 관련문서가 아니넹 ㅠㅜ..."

            if doc is None:  # postprocess가 None을 반환하면 문서를 건너뜁니다.
                return False

            print(doc)
            result = self.appendToEs(esIndex, url, doc)
        except Exception as e:
            print(e)
            print("not crawled : ", url)
            result = False
        return result

    def select(self, url : str, tags: list):
        raise MethodNotImplementError("select")

    def preprocess(self, desc : str) -> str :
        return desc

    def postprocess(self, doc: dict, item) -> dict:
        return doc

    def appendToEs(self, esIndex: str, url: any, doc: dict) -> bool:
        self.es.index(index = esIndex, id = url, body = doc)
        return self.es.exists(index = esIndex, id = url)
    def __del__(self):
        self.es.close()

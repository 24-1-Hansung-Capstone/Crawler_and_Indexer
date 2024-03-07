from elasticsearch import Elasticsearch

class MethodNotImplementError(Exception) :
    def __init__(self, methodName=""):
        self.errorMsg = f"{methodName} Method is not implements."
        super().__init__(self.errorMsg)

class CrawlingInterface :
    def __init__(self, host: str, authId : str, authPw : str):
        self.es = Elasticsearch(hosts=host, basic_auth=(authId, authPw), verify_certs=False)

    """
    * @param       : (self), 타겟 url, 본문tag, 제목tag
    * @return type : None
    * @description : 해당 함수를 통해 본문의 내용을 가져온다. 이떄 태그
    *
    """
    def crawl(self, url : str, category: str, mainTag : str, titleTag : str, esIndex : str, esId : any):
        # 가져오고자 하는 내용을 받아온다.
        mainBody,title  = self.select(url, mainTag, titleTag)

        # 전처리
        preprocessedText = self.preprocess(mainBody)
        preprocessedTitle = self.preprocess(title)

        # Es에 추가
        result = self.appendToEs(url, category, preprocessedText, preprocessedTitle, esIndex, esId)
        print(preprocessedText, preprocessedTitle)

        return result


    """
    * @param       : (self), 타겟 url, 본문tag, 제목tag
    * @return      : html dom 객체를 반환하는 것으로 생각
    * @description : 타겟 url에서 본문의 위치를 찾아 해당하는 위치의 내용을 전처리하지 않은 내용을 반환한다.
    *                해당 메서드를 구현해야한다. 구현하지 않은 상태로 호출시, MethodNotImplementError 예외를 raise함.
    """
    def select(self, url : str, mainTag : str, titleTag : str):
        raise MethodNotImplementError("select")
    
    """
    * @param       : (self), desc
    * @return      : 전처리가 완료된 문자열
    * @description : 필요한 경우, 해당 메서드를 구현하여 전처리를 진행한다.
    """
    def preprocess(self, desc : str) -> str :
        return desc

    """
    * @param        : (self), url, mainBody, title
    * @return       : append 성공 여부
    * @description  : Es에 추가
    """
    def appendToEs(self, url: str, category: str, mainBody : str, title : str, esIndex: str, esId: any) -> bool:
        doc = {
            "url": url,
            "category" : category,
            "title": title,
            "mainBody" : mainBody,
            "preview" : mainBody[:min(len(mainBody), 50)]
        }

        self.es.index(index = esIndex,  id = esId, body = doc)

        return self.es.exists(index=esIndex, id = esId)
    def __del__(self):
        self.es.close()

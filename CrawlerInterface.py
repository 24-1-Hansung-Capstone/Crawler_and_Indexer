from elasticsearch import Elasticsearch

class MethodNotImplementError(Exception) :
    def __init__(self, methodName=""):
        self.errorMsg = f"{methodName} Method is not implements."
        super().__init__(self.errorMsg)

class CrawlingInterface :
    def __init__(self, host: str, authId : str, authPw : str):
        self.es = Elasticsearch(hosts=host, basic_auth=(authId, authPw), verify_certs=False)

    def crawl(self, url : str, esIndex : str, tags : list, keys : list, item = None):
        try:
            texts = self.select(url, tags)

            if texts is None:
                return None

            texts = list(map(self.preprocess, texts))
            doc = dict(zip(keys, texts))
            doc["url"] = url
            doc = self.postprocess(doc, item)

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

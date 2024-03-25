import csv
from elasticsearch import Elasticsearch

class CsvUploader:
    def __init__(self, file_path: str, host: str, authId: str, authPw: str):
        self.file_path = file_path
        self.es = Elasticsearch(hosts=host, basic_auth=(authId, authPw), verify_certs=False)

    def uploadCsv(self, esIndex: str, esId: any, encoding: str = "utf-8"):
        with open(self.file_path, 'r', encoding=encoding) as csvfile:
            csvreader = csv.DictReader(csvfile)
            for item in csvreader:
                item = self.processItem(item)
                res = self.appendToEs(esIndex=esIndex, esId=esId, doc=item)
                print(res)
                if not res:
                    return False
                esId += 1
        return True

    def processItem(self, item: dict):
        return item

    def appendToEs(self, esIndex: str, esId: any, doc: dict) -> bool:
        self.es.index(index = esIndex,  id = esId, body = doc)
        return self.es.exists(index=esIndex, id = esId)





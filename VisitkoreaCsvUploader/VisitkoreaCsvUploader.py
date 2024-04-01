import CsvUploaderInterface

class VisitkoreaCsvUploader(CsvUploaderInterface.CsvUploader):
    def __init__(self, file_path: str, host: str, authId: str, authPw: str):
        super().__init__(file_path, host, authId, authPw)
    def processItem(self, item):
        item['Title'] = str(item['Title'])
        item['Location'] = str(item['Location'])
        item['Description'] = str(item['Description'])
        item['Tags'] = str(item['Tags'])
        item['Photo URL'] = str(item['Photo URL'])

        return item

    def __del__(self):
        super().__del__()

visitkorea = VisitkoreaCsvUploader(file_path = "../visitkorea_csv/Visitkorea_Crawled_Data.csv", host="https://localhost:9200", authId ="elastic", authPw="cAh+sWnbfRlXz1KimBpp")
visitkorea.uploadCsv(esIndex = "visitkorea", esId = 1)
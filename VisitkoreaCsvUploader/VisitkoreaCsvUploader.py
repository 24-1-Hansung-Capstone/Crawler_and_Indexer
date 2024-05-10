import CsvUploaderInterface

class VisitkoreaCsvUploader(CsvUploaderInterface.CsvUploader):
    def __init__(self, file_path: str, host: str, authId: str, authPw: str):
        super().__init__(file_path, host, authId, authPw)
    def processItem(self, item):
        item['title'] = str(item['title'])
        item['location'] = str(item['location'])
        item['description'] = str(item['description'])
        item['tags'] = str(item['tags'])
        item['photoURL'] = str(item['photoURL'])

        return item

    def __del__(self):
        super().__del__()

visitkorea = VisitkoreaCsvUploader(file_path = "../visitkorea_csv/Visitkorea_Crawled_Data.csv",
                                   host="http://221.142.15.180:9200", authId ="elastic", authPw="elastic") #cAh+sWnbfRlXz1KimBpp
visitkorea.uploadCsv(esIndex = "visitkorea", esId = 1)
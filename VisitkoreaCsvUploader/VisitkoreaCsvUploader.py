import CsvUploaderInterface

class VisitkoreaCsvUploader(CsvUploaderInterface.CsvUploader):
    def __init__(self, file_path: str, host: str, authId: str, authPw: str):
        super().__init__(file_path, host, authId, authPw)
    def processItem(self, item):
        item['title'] = str(item['Title'])
        item['location'] = str(item['Location'])
        item['description'] = str(item['Description'])
        item['tags'] = str(item['Tags'])
        item['photoURL'] = str(item['Photo URL'])

        return item

    def __del__(self):
        super().__del__()

visitkorea = VisitkoreaCsvUploader(file_path = "../visitkorea_csv/Visitkorea_Crawled_Data.csv", host="http://13.125.6.140:9200", authId ="elastic", authPw="elastic") #cAh+sWnbfRlXz1KimBpp
visitkorea.uploadCsv(esIndex = "visitkorea", esId = 1)
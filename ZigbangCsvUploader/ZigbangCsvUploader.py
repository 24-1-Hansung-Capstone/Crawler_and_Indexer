import CsvUploaderInterface

class ZigbangCsvUploader(CsvUploaderInterface.CsvUploader):
    def __init__(self, file_path: str, host: str, authId: str, authPw: str):
        super().__init__(file_path, host, authId, authPw)
    def processItem(self, item):
        item['danji_id'] = int(item['danji_id'])
        item['totalScore'] = float(item['totalScore'])
        item['trafficScore'] = float(item['trafficScore'])
        item['aroundScore'] = float(item['aroundScore'])
        item['careScore'] = float(item['careScore'])
        item['residentScore'] = float(item['residentScore'])
        del item['age']
        del item['sex']
        del item['residenceType']
        del item['married']

        return item

    def __del__(self):
        super().__del__()

zigbang = ZigbangCsvUploader(file_path = "../zigbang_csv/wydjp.csv", host="https://localhost:9200", authId ="elastic", authPw="cAh+sWnbfRlXz1KimBpp")
zigbang.uploadCsv(esIndex = "zigbang", esId = 1)
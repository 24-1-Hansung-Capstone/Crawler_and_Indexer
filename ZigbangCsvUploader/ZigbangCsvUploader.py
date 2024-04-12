import os

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

i = 0
for foldername, subfolders, filenames in os.walk("../zigbang_csv"):
    for filename in filenames:
        i += 1
        file_path = os.path.join(foldername, filename)
        zigbang = ZigbangCsvUploader(file_path=file_path, host="http://13.125.6.140:9200",
                                     authId="elastic", authPw="elastic")
        zigbang.uploadCsv(esIndex="zigbang", esId=i)



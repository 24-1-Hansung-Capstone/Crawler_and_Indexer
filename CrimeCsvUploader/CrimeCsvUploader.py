import csv
from CsvUploaderInterface import CsvUploader

class CrimeCsvUploader(CsvUploader):
    def __init__(self, file_path: str, host: str, authId: str, authPw: str):
        super().__init__(file_path, host, authId, authPw)

    def processItem(self, item):
        item['location'] = str(item['자치구별(2)'])
        item['sum_generation'] = float(item['소계_발생'])
        item['sum_arrest'] = float(item['소계_검거'])
        item['murder_generation'] = float(item['살인_발생'])
        item['murder_arrest'] = float(item['살인_검거'])
        item['robbery_generation'] = float(item['강도_발생'])
        item['robbery_arrest'] = float(item['강도_검거'])
        item['rape_generation'] = float(item['강간_강제추행_발생'])
        item['rape_arrest'] = float(item['강간_강제추행_검거'])
        item['theft_generation'] = float(item['절도_발생'])
        item['theft_arrest'] = float(item['절도_검거'])
        item['violence_generation'] = float(item['폭력_발생'])
        item['violence_arrest'] = float(item['폭력_검거'])
        del item['자치구별(1)']

        return item

crime = CrimeCsvUploader(file_path="../crime_csv/crime.csv", host="https://54.180.9.119:9200", authId="elastic",
                                 authPw="cAh+sWnbfRlXz1KimBpp")
crime.uploadCsv(esIndex="crime", esId=1)
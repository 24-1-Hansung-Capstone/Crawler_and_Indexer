import requests
import json
import csv


def getSeoulAptId(geohash):
    url = "https://apis.zigbang.com/v2/aparts/items?domain=zigbang&geohash={}".format(geohash)
    req = requests.get(url)
    items = req.json()

    danjiList=[]
    if items["vrItems"] !=[]:       ## vrItems 대상이 있으면 진행
        for i in items["vrItems"]:
            danjiList.append(i["areaDanjiId"])
    if items["recommendItems"] !=[]:       ## recommend 대상이 있으면 진행
        for i in items["recommendItems"]:
            danjiList.append(i["areaDanjiId"])
    if items["items"] !=[]:       ## Items 대상이 있으면 진행
        for i in items["items"]:
            danjiList.append(i["areaDanjiId"])

    danjiList = list(set(danjiList))


    return danjiList

################################################################################################################
def getReviewData(danjiId):
    reviewList=[]

    url = "https://apis.zigbang.com/property/apartments/{}/reviews/v1".format(danjiId)
    req_review = requests.get(url)

    if req_review.status_code == 200:
        review_data = json.loads(req_review.text)
        if review_data["summary"]["reviewCount"] != 0:                  # 리뷰가 없는 아파트는 스킵
            for j in review_data["data"]:
                reviewList.append([danjiId, review_data["summary"]["danjiName"], j["age"], j["sex"],
                                    j["residenceType"], j["married"], j["score"], rmCR(j["desc"]), j["trafficScore"],
                                    rmCR(j["trafficDesc"]),
                                    j["aroundScore"], rmCR(j["aroundDesc"]), j["careScore"], rmCR(j["careDesc"]),
                                    j["residentScore"], rmCR(j["residentDesc"])])

    return reviewList

################################################################################################################
# 리뷰에 \r , \n이 있는 경우 삭제

def rmCR(text):
    while ("\n" in text or "\r" in text):
        text = text.replace("\n"," ")
        text = text.replace("\r", " ")
    return text

################################################################################################################

def makeCSV(geohashName, reviewList):
    fileName = geohashName + ".csv"
    f = open(fileName, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    for i in reviewList:
        wr.writerow(i)
    f.close()

################################################################################################################

seoulGeohash = ['wydq0','wydq4','wydq5','wydjz','wydmb','wydmc','wydmf','wydmg','wydmu','wydmv','wydjt',
                'wydjw','wydjx','wydm8','wydm9','wydmd','wydme','wydms','wydmt','wydmw','wydjq','wydjr',
                'wydm2','wydm3','wydm6','wydm7','wydmk','wydmm','wydjn','wydjp','wydm0','wydm1','wydm4',
                'wydm5','wydmh']


for i in seoulGeohash:
    AptListPerGeohash = getSeoulAptId(i)        # Geohash별로 처리
    reviewPerGeohash=[]
    for j in AptListPerGeohash:
        tmpList = getReviewData(j)
        if len(tmpList) > 0:
            for z in tmpList:
                reviewPerGeohash.append(z)

    # 컬럼이름 생성
    reviewPerGeohash.insert(0,["danji_id", "danji_name", "age", "sex", "residenceType", "married", "totalScore",
                        "totalDesc", "trafficScore", "trafficDesc", "aroundScore",
                        "aroundDesc", "careScore", "careDesc", "residentScore", "residentDesc"])

    makeCSV(i,reviewPerGeohash)
    print("Making CSV for " +i+" has been completed")

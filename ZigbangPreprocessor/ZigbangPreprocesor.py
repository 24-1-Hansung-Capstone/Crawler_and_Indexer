# id	document	label
# 6270596	굳 ㅋ	1

#totalScore,totalDesc,trafficScore,trafficDesc,aroundScore,aroundDesc,careScore,careDesc,residentScore,residentDesc

import os
import csv
import random

#생성
train_file = open("train.txt", "w", encoding="utf-8")
test_file = open("test.txt", "w", encoding="utf-8")

#기초
train_file.write("id\tdocument\tlabel\n")
test_file.write("id\tdocument\tlabel\n")

data = []

#data 채우기
for foldername, subfolders, filenames in os.walk("../zigbang_csv"):
    for filename in filenames:
        file_path = os.path.join(foldername, filename)
        with open(file_path, 'r', encoding="utf-8") as csvfile:
            csvreader = csv.DictReader(csvfile)
            for item in csvreader:
                print(item)
                data.append((item["totalDesc"], item["totalScore"]))
                data.append((item["trafficDesc"], item["trafficScore"]))
                data.append((item["aroundDesc"], item["aroundScore"]))
                data.append((item["careDesc"], item["careScore"]))
                data.append((item["residentDesc"], item["residentScore"]))

#data로 test, train data 만들기
random.shuffle(data)
for i, item in enumerate(data):
    if item[1] != "3":
        senti_from_score = int(item[1]) // 3
        line = str(i) + "\t" + item[0] + "\t" + str(senti_from_score) + "\n"
        if i < len(data) // 2:
            train_file.write(line)
        else:
            test_file.write(line)



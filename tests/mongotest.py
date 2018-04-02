import csv
import pprint
from pymongo import MongoClient
client = MongoClient()

db = client.test
patients = db.mongo_patients
with open('patients.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    categories = next(reader)
    for row in reader:
        i = 0
        entry = {}
        for category in categories:
            entry[category] = row[i]
            i+=1
        patients.insert_one(entry)


for entry in patients.find():
    pprint.pprint(entry)

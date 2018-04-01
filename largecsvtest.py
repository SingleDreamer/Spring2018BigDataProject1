import csv
import numpy as np

import pprint
from pymongo import MongoClient
client = MongoClient()

db = client.test

if(not "mongo_rosmap" in db.collection_names()):
    rosmap = db.mongo_rosmap
    rosmap.drop()

    csvfile = open('ROSMAP_RNASeq_entrez.csv', 'rb')
    reader = csv.reader(csvfile)

    columns = ["patient_id", "diagnosis"]
    for i in next(reader)[2:]:
        columns.append(i)

        for row in reader:
            entry = {}
            for c, i in zip(columns,row) :
                entry [c] = i
            rosmap.insert_one(entry)
            #print 1

    csvfile.close()

else:
    rosmap = db.mongo_rosmap
    values = []
    for entry in (rosmap.find({'diagnosis':'3'})):
        values.append(entry['1'])
    for entry in (rosmap.find({'diagnosis':'2'})):
        values.append(entry['1'])
    values = np.array(map(float, values))
    print np.mean(values)
    print np.std(values)
    
        #print "hi"
#for entry in rosmap.find():
#    pprint.pprint(entry)

"""
i  = 0
    next(reader)
    #for row in reader:
        #print row
    #print next(reader)[2:]
    a = np.array(map(float, next(reader)[2:]))
    for i in a:
        print i
    print np.mean(a)
    print np.std(a)
    """



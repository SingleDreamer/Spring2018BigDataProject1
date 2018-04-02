import csv
import numpy as np
import pprint
from pymongo import MongoClient
from bson.code import Code 

client = MongoClient()

db = client.test

#if(not "mongo_rosmap" in db.collection_names()):



def reset():
    rosmap = db.mongo_rosmap
    rosmap.drop()

    csvfile = open('ROSMAP_RNASeq_entrez.csv', 'rb')
    reader = csv.reader(csvfile)

    columns = ["patient_id", "diagnosis"]
    for i in next(reader)[2:]:
        columns.append(i)

    for row in reader:
        entry = {}
        entry[columns[0]]=row[0]
        entry[columns[1]]=row[1]
        for c, i in zip(columns[2:],row[2:]) :
            entry [c] = i#float(i)
        rosmap.insert_one(entry)
            #print 1

    csvfile.close()

def run(diagnosis, gene):
    rosmap = db.mongo_rosmap
    values = []
    if (diagnosis == "AD"):
        for entry in (rosmap.find({'diagnosis':'4'})):
            values.append(entry[gene])
        for entry in (rosmap.find({'diagnosis':'5'})):
            values.append(entry[gene])
    elif (diagnosis == "MCI"):
        for entry in (rosmap.find({'diagnosis':'2'})):
            values.append(entry[gene])
        for entry in (rosmap.find({'diagnosis':'3'})):
            values.append(entry[gene])
    elif (diagnosis == "NCI"):
         for entry in (rosmap.find({'diagnosis':'1'})):
            values.append(entry[gene])
    else:
        print "invalid"
        return     
            
    values = np.array(map(float, values))
    print np.sum(values)
    print np.mean(values)
    print np.std(values)

#    result = db.mongo_rosmap.map_reduce(map, reduce, "testresults")#, query={"diagnosis": {"$or": ['2', '3']}})
#    for doc in result.find():
#        print doc

input = raw_input("input: ")
if (input == "reset"):
    reset()
else:
    #diagnosis = raw_input("diagnosis: ")
    gene = raw_input("gene: ")
    print "AD"
    run("AD", gene)
    print "MCI"
    run("MCI", gene)
    print "NCI"
    run("NCI", gene)


map = Code("function () {"
           " emit (this.'1'); "
           "}")

reduce = Code("function (value) {"
              " return Array.sum(value); "
              "}")



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



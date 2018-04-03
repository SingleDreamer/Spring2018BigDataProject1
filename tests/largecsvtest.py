import csv
import numpy as np
import pprint
from pymongo import MongoClient
from bson.code import Code
import os
import subprocess

client = MongoClient()

db = client.test

#if(not "mongo_rosmap" in db.collection_names()):

mongod = ["../mongodb-osx-x86_64-3.6.3/bin/mongod", "-dbpath", "../data/mongo"]
subprocess.Popen(mongod, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def reset():
    rosmap = db.mongo_rosmap
    rosmap.drop()

    csvfile = open('../raw_data/ROSMAP_RNASeq_entrez.csv', 'rb')
    reader = csv.reader(csvfile)

    columns = ["patient_id", "diagnosis"]
    for i in next(reader)[2:]:
        columns.append(i)

    for row in reader:
        entry = {}
        entry[columns[0]]=row[0]
        entry[columns[1]]=row[1]
        for c, i in zip(columns[2:],row[2:]) :
            #entry [c] = i#float(i)
            try:
                entry [c] = float(i)
            except:
                entry [c] = float(0)
        rosmap.insert_one(entry)
            #print 1

    print "done"
    csvfile.close()

map1 = Code("function () {"
            " emit (this.diagnosis, this['1']); "
           "}")

reduce1 = Code( """
function (key, values) {
var total = 0;
for (var i = 0; i < values.length; i++) {    
total += values[i];
}
return total;
}
""")


map2 = Code("function () {"
            " emit (this.diagnosis, this['1'], 1); "
           "}")

reduce2 = Code( """
function (key, values) {
var total = 0;
for (var i = 0; i < values.length; i++) {    
total += values[i];
}
return total;
}
""")
    
def run(diagnosis, gene):
    rosmap = db.mongo_rosmap
    """
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
    """
    
    result1 = db.mongo_rosmap.map_reduce(map1, reduce1, "testresults")#, query={"diagnosis": {"$or": ['2', '3']}})
    for doc in result1.find():
        print doc
    

input = raw_input("input: ")
if (input == "reset"):
    reset()
else:
    #diagnosis = raw_input("diagnosis: ")
    gene = raw_input("gene: ")
    print "AD"
    run("AD", gene)
    #print "MCI"
    #run("MCI", gene)
    #print "NCI"
    #run("NCI", gene)

subprocess.Popen(["pkill", "mongod"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)





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



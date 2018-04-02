import csv
import redis
import sqlite3
import os
import subprocess
import numpy as np
import pprint
from pymongo import MongoClient

start = """
Welcome to AD Knowledge Base.\n
Please enter a command.\n
0: exit\n
1: Given a gene, find all of its n-order interacting genes\n
2: Given a gene, find mean and std of gene expression values for AD/MCI/NCI, respectively\n
3: Given a gene, find all other information associated with this gene.\n
4: Given a patient id, find all patient information (age, gender, education etc.)\n
r: reset databases\n
h: list commands
\n\n """

# commands to run servers
mongod = ["./mongodb-osx-x86_64-3.6.3/bin/mongod", "-dbpath", "data/mongo"]
redisserver = ["./redis-stable/src/redis-server"]

# try and catch
subprocess.Popen(mongod, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.Popen(redisserver, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# redis variables
redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

# sqlite3 variables
connection = sqlite3.connect("data/sql/adk.db")
cursor = connection.cursor()

# pymongo variables
client = MongoClient()
db = client.test
rosmap = db.mongo_rosmap

def is_redis_available():
    try:
        redis_db.get(None)
    except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
        return False
    return True

def is_monog_available():
    try:
        client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        return False
    return True



# reset PPI.csv
def reset_redis():
    if (not is_redis_available()):
        print "redis server is unavailable, please run redis-server\n"
        return
    redis_db.flushdb()
    ppi_file = csv.reader(open("PPI.csv"))
    for line in ppi_file:
        redis_db.rpush(line[0], line[1])
    print "reset redis"



# reset patients.csv and entrez_ids_genesymbol.csv   
def reset_sql():
    # create patient table
    sql_command = """
    DROP TABLE IF EXISTS patient;
    """

    cursor.execute(sql_command)
    
    sql_command = """
    CREATE TABLE IF NOT EXISTS patient (
    patient_ID VARCHAR(11) PRIMARY KEY, 
    age INTEGER,
    gender CHAR(1),
    education VARCHAR(10));"""

    cursor.execute(sql_command)
    
    # import patient info from patients.csv
    with open('patients.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            sql_command = """INSERT INTO patient (patient_ID, age, gender, education) 
            VALUES ("{patient_ID}", {age}, "{gender}", "{education}");""".format(
                patient_ID = row[0],
                age = row[1],
                gender = row[2],
                education = row[3],
            )
            cursor.execute(sql_command)
        
    connection.commit()
    csvfile.close()

        #create gene table
    sql_command = """
    DROP TABLE IF EXISTS gene;
    """

    cursor.execute(sql_command)
    
    sql_command = """
    CREATE TABLE IF NOT EXISTS gene (
    entrez_id INTEGER PRIMARY KEY, 
    gene_symbol VARCHAR(10),
    gene_name VARCHAR(30));"""
    
    cursor.execute(sql_command)
        
        #import patient info from entrez_ids_genesymbol.csv
    with open('entrez_ids_genesymbol.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            sql_command = """INSERT INTO gene (entrez_id, gene_symbol, gene_name) 
            VALUES ({entrez_id}, "{gene_symbol}", "{gene_name}");""".format(
                entrez_id = row[0],
                gene_symbol = row[1],
                gene_name = row[2]
            )
            cursor.execute(sql_command)
        
    connection.commit()
    csvfile.close()
    print "reset sql"


def reset_mongo():
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
            entry [c] = i
        rosmap.insert_one(entry)

    csvfile.close()
    print "reset mongo"

    
def reset():
    reset_redis()
    reset_sql()
    reset_mongo()

def c1():
    if (not is_redis_available()):
        print "redis server is unavailable, please run redis-server\n"
    else:
        input_entrez_id = raw_input("Enter entrez_ID: ")
        try:
            input_entrez_id = int(input_entrez_id)
        except:
            print "Invalid input"
            return
        print "interactor A\tinteractor B"
        for b in redis_db.lrange(input_entrez_id, 0,-1):
            print "" + str(input_entrez_id) + "\t\t" +  b

def run_c2(diagnosis, gene):
    values = []
    if (diagnosis == "AD"):
        for entry in (rosmap.find({'diagnosis':'4'})):
            if not gene in entry:
                return
            values.append(entry[gene])
        for entry in (rosmap.find({'diagnosis':'5'})):
            values.append(entry[gene])
    elif (diagnosis == "MCI"):
        for entry in (rosmap.find({'diagnosis':'2'})):
            if not gene in entry:
                return
            values.append(entry[gene])
        for entry in (rosmap.find({'diagnosis':'3'})):
            values.append(entry[gene])
    elif (diagnosis == "NCI"):
        for entry in (rosmap.find({'diagnosis':'1'})):
            if not gene in entry:
                return
        values.append(entry[gene])
    else:
        print "Invalid input"
        return
    values = np.array(map(float, values))
    #print np.sum(values)
    print diagnosis
    print "mean: " + str( np.mean(values) )
    print "std: " + str( np.std(values) )
            
def c2():
    gene = raw_input("gene: ")
    #print "AD"
    run_c2("AD", gene)
    #print "MCI"
    run_c2("MCI", gene)
    #print "NCI"
    run_c2("NCI", gene)
            
def c3():
    input_entrez_id = raw_input("Enter entrez_ID: ")
    sql_command = """SELECT * FROM gene WHERE entrez_id ="{entrez_id}";""".format(
        entrez_id = input_entrez_id )
    cursor.execute(sql_command)
    ans = cursor.fetchone()
    if ans is None:
        print "Invalid input or no results"
        return
    print("\n")
    print("Gene ID: " + str(ans[0]))
    print("Gene Symbol: " + ans[1])
    print("Gene Name: " + ans[2])

def c4():
    input_patient_ID = raw_input("Enter patient ID: ")
    sql_command = """SELECT * FROM patient WHERE patient_ID ="{patient_ID}";""".format(
        patient_ID = input_patient_ID )
    cursor.execute(sql_command)
    ans = cursor.fetchone()
    if ans is None:
        print "Invalid input or no results"
        return
    print("\n")
    print("Patient ID: " + ans[0])
    print("Age: " + str(ans[1]))
    print("Gender: " + ans[2])
    print("Education: " + ans[3])
    print("\n")



print (start)
command = raw_input( "\n> ")
    
while (command != "0"):
    if (command == "1"):
        c1()
    elif (command == "2"):
        c2()
    elif (command == "3"):
        c3()
    elif (command == "4"):
        c4()
    elif (command == "r"):
        reset()
    elif (command == "rr"):
        reset_redis()
    elif (command == "rs"):
        reset_sql()
    elif (command == "rm"):
        reset_mongo()
    elif (command == "h"):
        print(start)
    else:
        print "Invalid Command"

    command = raw_input( "\n> ")


print "\nThank you for using AD Knowledge Database\n\n"

# kill servers
subprocess.Popen(["pkill", "mongod"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.Popen(["pkill", "redis-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

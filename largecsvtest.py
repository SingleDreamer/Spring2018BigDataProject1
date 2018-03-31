import csv
import sqlite3
import numpy as np 
"""
connection = sqlite3.connect("largecsvtest.db")
cursor = connection.cursor()

sql_command = """ """
DROP TABLE IF EXISTS patient;
"""

i  = 0
# import patient info from patients.csv
with open('ROSMAP_RNASeq_entrez.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    #for row in reader:
        #print row
    #print next(reader)[2:]
    a = np.array(map(float, next(reader)[2:]))
    for i in a:
        print i
    print np.mean(a)
    print np.std(a)
    
csvfile.close()

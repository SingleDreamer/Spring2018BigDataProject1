# AD Knowledge Base (Spring2018BigDataProject1)
### Eunice Hew and Jessica Ng

## How to Run

Create and activate the virtualenv. 

`virtualenv --python=/usr/bin/python 2.7 ENV`
`source ENV/bin/activate`

Make sure you have all the dependecies (see belwo)

Run the main program

`python adkbase.py`

## How to Use

Commands: 

1: Given a gene, find all of its n-order interacting genes

2: Given a gene, find mean and std of gene expression values for AD/MCI/NCI, respectively

3: Given a gene, find all other information associated with this gene.

4: Given a patient id, find all patient information (age, gender, education etc.)

If no data is showing or databases have not been set up: 

r: reset databases

   rs: reset sql only

   rm: reset mongodb only

   rr: reset redis only 

h: list commands

e: exit


## dependencies (use virtualenv) 
- sqlite3
- numpy
- pymongo
- redis

## notes
- django?? not set up yet
- needs stress tetsitn gomg 
- need to use mapreduce in the mongo large csv part c2(???) part too workon that


# Testing Notes (please ignore)

## adkbase.py

main running program, will tell computer to run servers, just run adkbase.py. also will kill servers at end so yearh

## sqltest.py

uses patient.db, can run by itself without servers. will check if data has already been stored, and upload thee newestdata(double check if this is true?). Stores data for entrez_ids_genesybmol.csv and patiensts.csv?


## testred.py and checkredis.py

uses redis. first run ./redis-stable/src/redis-server, then run checkredis.py. Data is stored in dump.rdb The file testred.py stores all the from PPI.csv into redis server. Currenly does not store uniquely, so running testred.py again will cause replaiction in data. 


## largecsvtest.py

checking if large csv file can be ued with csvreader; speed seems acceptable. Need to figure out storage for this. Using numpy for mean and std seems fine, need to seperate values based on diagnosis. 


## testxml.py

Still need to fucking deal with this. Can process XML files, but XML file so large that takes too much time. Need to decide what data to store, and with what format. Large XML file can't be uploaed bc too large, so make sure it is here locally before running this program. 
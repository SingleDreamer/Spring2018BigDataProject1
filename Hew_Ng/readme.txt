AD Knowledge Base (Spring2018BigDataProject1)
Eunice Hew and Jessica Ng

## How to Run 

1) Make sure you are using python2.7 to run this program.

2) Optional: create and activate the virtualenv in the folder. 

$ virtualenv --python=/usr/bin/python2.7 ENV
$ source ENV/bin/activate

3) Run MongoDB (mongod) and Redis (redis-server)

$ ./mongodb-osx-x86_64-3.6.3/bin/mongod -dbpath data/mongo

$ ./redis-stable/src/redis-server redis-stable/redis.conf

If necessary, download the following:

MongoDB: https://www.mongodb.com/download-center#community

Redis: http://download.redis.io/redis-stable.tar.gz

If you unzip these in the same folder as adkbase.py, there is an option to let the programs start the servers and store the databases in data/, as long as you edit redis.conf

4) Make sure you have all the dependecies (see below). If you are using a virtualenv, download the dependencies:

$ pip install pymongo redis numpy

If you plan to use the Django interface, make sure you install that as well.

$ pip install Django

5) Make sure the source files are in the /raw_data folder: 
entrez_ids_genesymbol.csv
entrez_ids_uniprot.txt
patients.csv
PPI.csv
ROSMAP_RNASeq_entrez.csv

6) Run the main program

$ python main.py

7) Enter 'r' to reset and build the databases

$ > r

Please be aware this will take some time.


## How to Run the Django interaface

For convenience, reset at least once using the program. 

1) Run MongoDB (mongod) and Redis (redis-server) manually. Make sure you are using the same settings as you were when using the program. This will allow you to access the preloaded databases. Otherwise, there is an option to reset and rebuild the databases using the interface, but this will take time. 

2) In django_app, run:

$ python manage.py runserver

3) In a web browser, go to localhost:8000/adkbase

## How to Use

Commands: 

1: Given a gene, find all of its n-order interacting genes

2: Given a gene, find mean and std of gene expression values for AD/MCI/NCI, respectively. (Takes slightly more time)

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
This requires Python2.7
- sqlite3
- numpy
- pymongo
- redis

## notes
- django?? not set up yet
- needs stress testing  
- need to use mapreduce in the mongo large csv part c2 part too work on that


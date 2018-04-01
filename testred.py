
import redis
import os
import csv

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

#redis_db.set("hi", "there")
#print(redis_db.get("hi"))

ppi_file = csv.reader(open("PPI.csv"))

for line in ppi_file:
	#print(line[0], line[1])

	#redis_db.set(line[0], line[1])


	#redis_db.append(line[0], line[1])
        redis_db.rpush(line[0], line[1])

	#if line[0] not in redis_db.keys():
	#	redis_db.set(line[0], line[1])
	#else:
	#	redis_db.append(line[0], line[1])
#redis_db.sort(sorted, groups = True)
#print(redis_db.get("7"))
#print(redis_db.hgetall("7"))






'''
r = redis.Redis('localhost')

user = {"Name":"Pradeep", "Company":"SCTL", "Address":"Mumbai", "Location":"RCP"}

r.hmset("pythonDict", user)

r.hgetall("pythonDict")



pipe = redis_db.pipeline()
for line in open("PPI.csv"):
	pipe.push(line[0], line[1])
pipe.execute()


r.set('bing', 'baz')
pipe = r.pipeline()
pipe.set('foo', 'bar')
pipe.get('bing')
print(pipe.execute())





_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'project1')
_RESULT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'result')

def get_ppi_database():
	if os.path.isdir(os.path.join(_DATA_DIR, 'PPI.csv')):
		_PPI_DIR = os.path.join(_DATA_DIR, 'PPI.csv')
	else:
		print('Sorry, no such file')
	return _PPI_DIR




redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
#print (redis_db)

# see what keys are in Redis
redis_db.keys()

# output for keys() should be an empty list "[]"
redis_db.set('full stack', 'python')
# output should be "True"
redis_db.keys()
# now we have one key so the output will be "[b'full stack']"
redis_db.get('full stack')
# output is "b'python'", the key and value still exist in Redis
redis_db.incr('twilio')
# output is "1", we just incremented even though the key did not
# previously exist
redis_db.get('twilio')
# output is "b'1'" again, since we just obtained the value from
# the existing key
redis_db.delete('twilio')
# output is "1" because the command was successful
redis_db.get('twilio')
# nothing is returned because the key and value no longer exist



'''


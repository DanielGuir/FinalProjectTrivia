# this script is trigged by 'start' button
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
from kafka import KafkaProducer
import couchdb
import time

#session id
sessionid = 1 #FIXME: have this as a webpage param

#Setup couchdb properties
couch = couchdb.Server('http://admin:estopinalgui@129.114.26.92:30001/')
db = couch['questions']



# acquire the consumer

producer = KafkaProducer (bootstrap_servers="129.114.25.218:30002", 
                                          acks=1)

# get random 10 question
count = 0
for doc in db:
	question = db[doc]['content']
	count += 1
    # send question
	producer.send("question-session" + str(sessionid), value=bytes (question, 'ascii'))
	if count == 5:
		break



                                        


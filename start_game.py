# this script is trigged by 'start' button
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import couchdb
import time

#session id
sessionid = 1 #FIXME: have this as a webpage param

#Setup couchdb properties
couch = couchdb.Server('http://admin:estopinalgui@129.114.26.92:30001/')
questions = couch['questions']
leaderboard = couch['leaderboard']


# acquire the consumer

#consumer = KafkaConsumer (bootstrap_servers="129.114.25.218:30002")
producer = KafkaProducer (bootstrap_servers="129.114.25.218:30002", 
                                          acks=1)

# get random 10 question
count = 0
for question in question:
    count += 1
    # send question
    producer.send("question-session" + str(sessionid), value=bytes (question, 'ascii'))
    if count == 10:
        break



                                        


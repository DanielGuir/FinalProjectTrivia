# this script is trigged by 'join/host' button
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import couchdb
import time

#session id
sessionid = 1 #FIXME: have this as a webpage param
username = 1

#Setup couchdb properties
couch = couchdb.Server('http://admin:estopinalgui@129.114.26.92:30001/')
questions = couch['questions']
leaderboard = couch['leaderboard']


# acquire the consumer

consumer = KafkaConsumer (bootstrap_servers="129.114.25.218:30002")
producer = KafkaProducer (bootstrap_servers="129.114.25.218:30002", 
                                          acks=1)

consumer.subscribe(topics=["question-session" + str(sessionid)])

for question in consumer:
	print('some interactions with UI here to display question, get answer and verify correctness. not sure how to do it')

	if right:
		producer.send("leaderboard-session" + str(sessionid), value=bytes (username + '1', 'ascii'))
	if wrong:
		producer.send("leaderboard-session" + str(sessionid), value=bytes (username + '0', 'ascii'))

print('finished')


                                        


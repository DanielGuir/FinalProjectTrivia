# this script is trigged by 'join/host' button
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
from kafka import KafkaProducer
import couchdb
import time

#session id
sessionid = 1 #FIXME: have this as a webpage param
username = input('username:')

#Setup couchdb properties
couch = couchdb.Server('http://admin:estopinalgui@129.114.26.92:30001/')

# acquire the consumer

consumer = KafkaConsumer (group_id = username, bootstrap_servers="129.114.25.218:30002")
producer = KafkaProducer (bootstrap_servers="129.114.25.218:30002", 
                                          acks=1)

consumer.subscribe(topics=["question-session" + str(sessionid)])

for msg in consumer:
	#some interactions with UI here to display question, get answer and verify correctness. not sure how to do it via web frontend
	question = str(msg.value, 'ascii').split(' ')
	options = int(question[-1])
	print('please select the following options')
	print(question[:-1])
	val = int(input('Enter: '))
	if val == options:
		print('right')
		producer.send("leaderboard-session" + str(sessionid), value=bytes (username + '1', 'ascii'))
	else:
		print('wrong')
		producer.send("leaderboard-session" + str(sessionid), value=bytes (username + '0', 'ascii'))



print('finished')


                                        


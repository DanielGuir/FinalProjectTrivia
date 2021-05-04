# this script is trigged by 'join/host' button
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
from kafka import KafkaProducer
import couchdb
import time

# unique session id ensures data to be sent to correct consumer/producer
sessionid = 1 #FIXME: have this as a webpage param
username = input('username:') #FIXME: have this as a webpage param too



# acquire the consumer
# note: the consumers need to have different group_ids to receive the same thing. Thus used username.
consumer = KafkaConsumer (group_id = username, bootstrap_servers="129.114.25.218:30002")
producer = KafkaProducer (bootstrap_servers="129.114.25.218:30002", 
                                          acks=1)


consumer.subscribe(topics=["question-session" + str(sessionid)])

# this will be triggered with start_game (i.e. when there's data in the topic)
for msg in consumer:
	#FIXME: convert this to frontend code
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


                                        


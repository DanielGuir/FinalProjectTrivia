# this script is trigged by 'join/host' button
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import couchdb
import time

#unique session id
sessionid = 1 #FIXME: have this as a webpage param

# acquire the consumer

consumer = KafkaConsumer (bootstrap_servers="129.114.25.218:30002")
consumer.subscribe(topics=["leaderboard-session" + str(sessionid)])

userdict = {}
for msg in consumer:
	#FIXME: convert this to frontend code
	score = str(msg.value, 'ascii')
	user = score[:-1]
	curscore = int(score[-1])
	if not user in userdict:
		userdict[user] = curscore
	else:
		userdict[user] = userdict[user] + curscore

	print(userdict)

print('finished')


                                        


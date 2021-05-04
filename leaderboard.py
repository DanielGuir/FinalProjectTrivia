# this script is trigged by 'join/host' button
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import couchdb
import time

#session id
sessionid = 1 #FIXME: have this as a webpage param

#Setup couchdb properties
couch = couchdb.Server('http://admin:estopinalgui@129.114.26.92:30001/')


# acquire the consumer

consumer = KafkaConsumer (bootstrap_servers="129.114.25.218:30002")


consumer.subscribe(topics=["leaderboard-session" + str(sessionid)])

userdict = {}

for score in consumer:
	user = score[:-1]
	curscore = int(curscore[-1])
	if not user in userdict:
		userdict[user] = curscore
	else:
		userdict[user] = userdict[user] + curscore

	print('some code to display it to the UI')

print('finished')


                                        


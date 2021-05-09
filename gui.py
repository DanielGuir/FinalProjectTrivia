#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 19:30:06 2021

@author: danielgui
"""
# simple trivia game implemented by Tkinter

from tkinter import *
from tkinter import ttk
from threading import Thread
import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
from kafka import KafkaProducer
import couchdb
import time
from queue import Queue

window = Tk()

# Entry page
window.title("Welcome to Trivia")
window.geometry('400x200')
window.configure(background = "white");
frame = Frame(window, borderwidth = 1)
frame.pack(side="top", expand=True, fill="both")
b = Label(frame ,text = "Room Name")
b.grid(row = 1,column = 0)
c = Label(frame ,text = "Username")
d = Label(frame, text = "Question Count")
c.grid(row = 2,column = 0)
d.grid(row=3, column=0)
b1 = Entry(frame)
b1.grid(row = 1,column = 1)
c1 = Entry(frame)
c1.grid(row = 2,column = 1)
d1 = Entry(frame)
d1.grid(row=3, column=1)
# identifiers

#threads

# queue for thread communicating
global question_q
question_q = Queue()
point_q = Queue()
answer_q = Queue()


# make those widgets global

# function for starting game
def start_game():
	#Setup couchdb properties
	couch = couchdb.Server('http://admin:estopinalgui@129.114.26.92:30001/')
	db = couch['questions']
	
	# acquire the consumer
	producer = KafkaProducer (bootstrap_servers="129.114.25.218:30002", 
											  acks=1)
	
	# get random 10 question
	count = questioncount + 1
	for doc in db:
		count -= 1
		if count == 0:
			question = 'Finish'
		else:
			question = db[doc]['content']
		# send question
		producer.send("question-session" + str(session_id), value=bytes (question, 'ascii'))
		if question == 'Finish':
			break
	print('finished')

# function for collecting questions
def collect_question(question_q):
	consumer = KafkaConsumer (group_id = username, bootstrap_servers="129.114.25.218:30002")
	
	consumer.subscribe(topics=["question-session" + str(session_id)])
	print('collectconsumerstarted')
	for msg in consumer:
		question = str(msg.value, 'ascii')
		question_q.put(question)
		print('collected')

# function for sending points
def send_point(point_q):
	producer = KafkaProducer (bootstrap_servers="129.114.25.218:30002", 
										  acks=1)
	while True:
		if point_q.empty():
			continue
		else:
			producer.send("leaderboard-session" + str(session_id), value=bytes (point_q.get(), 'ascii'))

# function for leaderboard
def leaderboard(leaderboard_list):
	print('leaderboard', session_id)
	consumer = KafkaConsumer (bootstrap_servers="129.114.25.218:30002")
	consumer.subscribe(topics=["leaderboard-session" + str(session_id)])
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

		count = 0
		for key,value in userdict.items():
			leaderboard_list[count].config(text=str(key) + ': ' + str(value))
			count += 1

	print('finished')
	


def wronganswer(button):
	print('wrong')

	answershow.config(text = 'Your answer: ' + button['text'])
	#print(count)
	# update score
	if answer_q.empty():
		answer_q.put(0)
	else:
		answer_q.get()
		answer_q.put(0)
	#count +=1
	

def timer():
	count = 10
	while count > 0:
		start_text.config(text = "Time remaining: " + str(count))
		time.sleep(1)
		count = count - 1
	start_text.config(text = "Time remaining: 0")
	if answer_q.empty():
		point_q.put(username + '0')
	else:
		answer = answer_q.get()
		if answer == 1:
			point_q.put(username + '1')
		else:
			point_q.put(username + '0')

	# populate new question
	while True:
		if question_q.empty():
			continue
		# process questions
		else:
			question = question_q.get()
			question = question.split(' ')
			if len(question) == 1:
				answer1.destroy()
				answer2.destroy()
				answer3.destroy()
				answer4.destroy()
				question_text.config(text = 'Game Finished!')
				break
			answer = question[-1]
			question_text.config(text=question[0])
			answer1.config(text=question[1], command=lambda: wronganswer(answer1))
			answer2.config(text=question[2], command=lambda: wronganswer(answer2))
			answer3.config(text=question[3], command=lambda: wronganswer(answer3))
			answer4.config(text=question[4], command=lambda: wronganswer(answer4))
			if answer == '1':
				answer1.config(command=lambda: rightanswer(answer1))
			if answer == '2':
				answer2.config(command=lambda: rightanswer(answer2))
			if answer == '3':
				answer3.config(command=lambda: rightanswer(answer3))
			if answer == '4':
				answer4.config(command=lambda: rightanswer(answer4))
			answershow.config(text = '')
			ttimer = Thread(target=timer)
			ttimer.start()
			break
	

def rightanswer(button):
	print('right')
	#print(count)
	answershow.config(text='Your answer: ' + button['text'])
	if answer_q.empty():
		answer_q.put(1)
	else:
		answer_q.get()
		answer_q.put(1)

# def StartClicked(question_q):
#     print(session_id)
#     # modify UI 
#     # start game
#     tstart = Thread(target = start_game)
#     tstart.start()
#     count = 1
#     while True:
#         if question_q.empty():
#             continue
#         # process questions
#         else:
#             question = question_q.get()
#             question = question.split(' ')
#             answer = question[-1]
#             question_text.config(text=question[0])
#             answer1.config(text=question[1], command=wronganswer)
#             answer2.config(text=question[2], command=wronganswer)
#             answer3.config(text=question[3], command=wronganswer)
#             answer4.config(text=question[4], command=wronganswer)
#             if answer == '1':
#                 answer1.config(command=rightanswer)
#             if answer == '2':
#                 answer2.config(command=rightanswer)
#             if answer == '3':
#                 answer3.config(command=rightanswer)
#             if answer == '4':
#                 answer4.config(command=rightanswer)
#             break

def waitforquestion(question_q):
	while True:
		if question_q.empty():
			continue
		# process questions
		else:
			question = question_q.get()
			question = question.split(' ')
			answer = question[-1]
			question_text.config(text=question[0])
			answer1.config(text=question[1], command=lambda: wronganswer(answer1))
			answer2.config(text=question[2], command=lambda: wronganswer(answer2))
			answer3.config(text=question[3], command=lambda: wronganswer(answer3))
			answer4.config(text=question[4], command=lambda: wronganswer(answer4))
			if answer == '1':
				answer1.config(command=lambda: rightanswer(answer1))
			if answer == '2':
				answer2.config(command=lambda: rightanswer(answer2))
			if answer == '3':
				answer3.config(command=lambda: rightanswer(answer3))
			if answer == '4':
				answer4.config(command=lambda: rightanswer(answer4))
			ttimer = Thread(target=timer)
			ttimer.start()
			break  

def StartClicked():
	print(session_id)
	# modify UI 
	# start game
	start_btn.destroy()
	global start_text
	start_text = Label(frame ,text = "")
	start_text.grid(row=0, column=0)
	tstart = Thread(target = start_game)
	tstart.start()
	count = 1
	twait = Thread(target = waitforquestion, args = (question_q,))
	twait.start()

def Hostclicked():
	# populate identifiers
	global session_id
	global username
	global questioncount
	session_id = b1.get()
	username = c1.get()
	questioncount = int(d1.get())
	# Modify UI
	for widgets in frame.winfo_children():
		widgets.destroy()
	# New UI
	frame.pack(side="left", expand=True, fill="both")
	global question_text
	global answer1
	global answer2
	global answer3
	global answer4
	global leaderboard1
	global leaderboard2
	global leaderboard3
	global leaderboard4
	global curcount
	global start_btn
	global answershow
	curcount = 0
	start_btn = ttk.Button(frame ,text="Start Game", command=StartClicked)
	start_btn.grid(row=0, columnspan=2)
	question_text = Label(frame, text = "Waiting for the host to start game...", borderwidth=2, relief="groove")
	question_text.grid(row=1, columnspan=2)
	answer1 = ttk.Button(frame ,text="")
	answer1.grid(row=2, column=0)
	answer2 = ttk.Button(frame ,text="")
	answer2.grid(row=2, column=1)
	answer3 = ttk.Button(frame ,text="")
	answer3.grid(row=3, column=0)
	answer4 = ttk.Button(frame ,text="")
	answer4.grid(row=3, column=1)
	answershow = Label(frame, text = "")
	answershow.grid(row = 4, columnspan = 2)
	frame2 = Frame(window, borderwidth=2, relief="groove")
	frame2.pack(side="right", expand=True, fill="both")
	leaderboard_tex = Label(frame2, text='Leaderboard', borderwidth=1, relief="groove")
	leaderboard_tex.grid(row=0, column=2)
	leaderboard1 = Label(frame2 ,text = "")
	leaderboard1.grid(row = 1,column = 2)
	leaderboard2 = Label(frame2 ,text = "")
	leaderboard2.grid(row = 2,column = 2)
	leaderboard3 = Label(frame2 ,text = "")
	leaderboard3.grid(row = 3,column = 2)
	leaderboard4 = Label(frame2 ,text = "")
	leaderboard4.grid(row = 4,column = 2)
	
	
	
	# continue to StartClicked
	tcollect = Thread(target = collect_question, args=(question_q,))
	tcollect.start()
	tsend = Thread(target = send_point, args=(point_q,))
	tsend.start()
	tleaderboard = Thread(target = leaderboard, args=([leaderboard1, leaderboard2, leaderboard3, leaderboard4],))
	tleaderboard.start()
	pass

def Joinclicked():
	# populate identifiers
	# Modify UI
	
	# populate identifiers
	global session_id
	global username
	session_id = b1.get()
	username = c1.get()
	# Modify UI
	for widgets in frame.winfo_children():
		widgets.destroy()
	# New UI
	frame.pack(side="left", expand=True, fill="both")
	global start_text
	global question_text
	global answer1
	global answer2
	global answer3
	global answer4
	global leaderboard1
	global leaderboard2
	global leaderboard3
	global leaderboard4
	global curcount
	global answershow
	curcount = 0
	start_text = Label(frame ,text = "")
	start_text.grid(row=0, columnspan=2)
	question_text = Label(frame, text = "Waiting for the host to start game...", borderwidth=2, relief="groove")
	question_text.grid(row=1, columnspan=2)
	answer1 = ttk.Button(frame ,text="")
	answer1.grid(row=2, column=0)
	answer2 = ttk.Button(frame ,text="")
	answer2.grid(row=2, column=1)
	answer3 = ttk.Button(frame ,text="")
	answer3.grid(row=3, column=0)
	answer4 = ttk.Button(frame ,text="")
	answer4.grid(row=3, column=1)
	answershow = Label(frame, text = "")
	answershow.grid(row = 4, columnspan = 2)
	frame2 = Frame(window, borderwidth=2, relief="groove")
	frame2.pack(side="right", expand=True, fill="both")
	leaderboard_tex = Label(frame2, text='Leaderboard', borderwidth=1, relief="groove")
	leaderboard_tex.grid(row=0, column=2)
	leaderboard1 = Label(frame2 ,text = "")
	leaderboard1.grid(row = 1,column = 2)
	leaderboard2 = Label(frame2 ,text = "")
	leaderboard2.grid(row = 2,column = 2)
	leaderboard3 = Label(frame2 ,text = "")
	leaderboard3.grid(row = 3,column = 2)
	leaderboard4 = Label(frame2 ,text = "")
	leaderboard4.grid(row = 4,column = 2)
	twait = Thread(target = waitforquestion, args = (question_q,))
	twait.start()
	# continue to StartClicked
	tcollect = Thread(target = collect_question, args=(question_q,))
	tcollect.start()
	tsend = Thread(target = send_point, args=(point_q,))
	tsend.start()
	tleaderboard = Thread(target = leaderboard, args=([leaderboard1, leaderboard2, leaderboard3, leaderboard4],))
	tleaderboard.start()
	pass
	
	
btn = ttk.Button(frame ,text="Host Game", command= Hostclicked).grid(row=4,column=0)
btn2 = ttk.Button(frame ,text="Join Game", command= Joinclicked).grid(row=4,column=1)
window.mainloop()
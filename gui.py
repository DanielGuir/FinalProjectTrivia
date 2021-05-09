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
frame = Frame(window)
frame.pack(side="top", expand=True, fill="both")
b = Label(frame ,text = "Session id")
b.grid(row = 1,column = 0)
c = Label(frame ,text = "Username")
c.grid(row = 2,column = 0)
b1 = Entry(frame)
b1.grid(row = 1,column = 1)
c1 = Entry(frame)
c1.grid(row = 2,column = 1)
# identifiers

#threads

# queue for thread communicating
global question_q
question_q = Queue()
point_q = Queue()



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
    count = 0
    for doc in db:
    	question = db[doc]['content']
    	count += 1
        # send question
    	producer.send("question-session" + str(session_id), value=bytes (question, 'ascii'))
    	if count == 5:
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
    


def wronganswer():
    print('wrong')
    #print(count)
    point_q.put(username + '0')
    #count +=1
    
    while True:
        if question_q.empty():
            continue
        # process questions
        else:
            question = question_q.get()
            question = question.split(' ')
            answer = question[-1]
            question_text.config(text=question[0])
            answer1.config(text=question[1], command=wronganswer)
            answer2.config(text=question[2], command=wronganswer)
            answer3.config(text=question[3], command=wronganswer)
            answer4.config(text=question[4], command=wronganswer)
            if answer == '1':
                answer1.config(command=rightanswer)
            if answer == '2':
                answer2.config(command=rightanswer)
            if answer == '3':
                answer3.config(command=rightanswer)
            if answer == '4':
                answer4.config(command=rightanswer)
            break
def rightanswer():
    print('right')
    #print(count)
    point_q.put(username + '1')
    #count+=1
    while True:
        if question_q.empty():
            continue
        # process questions
        else:
            question = question_q.get()
            question = question.split(' ')
            answer = question[-1]
            question_text.config(text=question[0])
            answer1.config(text=question[1], command=wronganswer)
            answer2.config(text=question[2], command=wronganswer)
            answer3.config(text=question[3], command=wronganswer)
            answer4.config(text=question[4], command=wronganswer)
            if answer == '1':
                answer1.config(command=rightanswer)
            if answer == '2':
                answer2.config(command=rightanswer)
            if answer == '3':
                answer3.config(command=rightanswer)
            if answer == '4':
                answer4.config(command=rightanswer)
            break

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
            answer1.config(text=question[1], command=wronganswer)
            answer2.config(text=question[2], command=wronganswer)
            answer3.config(text=question[3], command=wronganswer)
            answer4.config(text=question[4], command=wronganswer)
            if answer == '1':
                answer1.config(command=rightanswer)
            if answer == '2':
                answer2.config(command=rightanswer)
            if answer == '3':
                answer3.config(command=rightanswer)
            if answer == '4':
                answer4.config(command=rightanswer)
            break  

def StartClicked():
    print(session_id)
    # modify UI 
    # start game
    tstart = Thread(target = start_game)
    tstart.start()
    count = 1
    twait = Thread(target = waitforquestion, args = (question_q,))
    twait.start()

def Hostclicked():
    # populate identifiers
    global session_id
    global username
    session_id = b1.get()
    username = c1.get()
    # Modify UI
    for widgets in frame.winfo_children():
        widgets.destroy()
    # New UI
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
    curcount = 0
    start_btn = ttk.Button(frame ,text="Start Game", command=StartClicked).grid(row=0, column=0)
    question_text = Label(frame, text = "Waiting for the host to start game...")
    question_text.grid(row=1, column=0)
    answer1 = ttk.Button(frame ,text="")
    answer1.grid(row=2, column=0)
    answer2 = ttk.Button(frame ,text="")
    answer2.grid(row=2, column=1)
    answer3 = ttk.Button(frame ,text="")
    answer3.grid(row=3, column=0)
    answer4 = ttk.Button(frame ,text="")
    answer4.grid(row=3, column=1)
    leaderboard1 = Label(frame ,text = "")
    leaderboard1.grid(row = 0,column = 2)
    leaderboard2 = Label(frame ,text = "")
    leaderboard2.grid(row = 1,column = 2)
    leaderboard3 = Label(frame ,text = "")
    leaderboard3.grid(row = 2,column = 2)
    leaderboard4 = Label(frame ,text = "")
    leaderboard4.grid(row = 3,column = 2)
    
    
    
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
    curcount = 0
    start_text = Label(frame ,text = "").grid(row=0, column=0)
    question_text = Label(frame, text = "Waiting for the host to start game...")
    question_text.grid(row=1, column=0)
    answer1 = ttk.Button(frame ,text="")
    answer1.grid(row=2, column=0)
    answer2 = ttk.Button(frame ,text="")
    answer2.grid(row=2, column=1)
    answer3 = ttk.Button(frame ,text="")
    answer3.grid(row=3, column=0)
    answer4 = ttk.Button(frame ,text="")
    answer4.grid(row=3, column=1)
    leaderboard1 = Label(frame ,text = "")
    leaderboard1.grid(row = 0,column = 2)
    leaderboard2 = Label(frame ,text = "")
    leaderboard2.grid(row = 1,column = 2)
    leaderboard3 = Label(frame ,text = "")
    leaderboard3.grid(row = 2,column = 2)
    leaderboard4 = Label(frame ,text = "")
    leaderboard4.grid(row = 3,column = 2)
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
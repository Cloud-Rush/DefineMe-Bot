#!/usr/bin/env python

#This is a dictionary bot using the Merriam Webster API by /u/tstarrs
#Credit goes to pfeyz on Github for the API wrapper functions used by this bot. 


import praw
import os
import sys
import re
import time
from define import lookup
from api import(CollegiateDictionary, WordNotFoundException)

API_KEY = open("API_Key.txt", 'r').read().rstrip()
os.environ['MERRIAM_WEBSTER_COLLEGIATE_KEY'] = API_KEY

#Acquire login info and Login
user_agent = open("User_Agent.txt", 'r').read().rstrip()
bot_username = open("username.txt", 'r').read().rstrip()
bot_password = open("password.txt", "r").read().rstrip()
r = praw.Reddit(user_agent=user_agent)
r.login(username = bot_username, password = bot_password)
print("Logged in")

if not os.path.isfile("readComments.txt"):
	replies = []
else:
	print "Loading previous replies"
	with open("readComments.txt", "r") as f:
		replies = f.read()
		replies = replies.split("\n")
		replies = filter(None, replies)

#get Merriam Webster API Key
collkey = os.getenv("MERRIAM_WEBSTER_COLLEGIATE_KEY")

#keyWord = "DefineMe!"
while True:
	subreddit = r.get_subreddit('UMW_CPSC470Z')
	subreddit_comments = subreddit.get_comments()
	for comment in subreddit_comments:
		#has_keyWord = any(string in comment.body for keyWord)
		if comment.id not in replies:
			if re.search("DefineMe! ", comment.body):
				#get word from comment
				word = re.search("DefineMe! (.*)", comment.body, re.IGNORECASE).groups()
				query = word[0]
				lookupResult = lookup(CollegiateDictionary, collkey, query)
				REPLY = lookupResult
				print REPLY
				comment.reply(REPLY)
				print("Should have replied")
				replies.append(comment.id)
	print("Saving new ids to file")
	with open("readComments.txt", "w") as f:
		for i in replies:
			f.write(i + "\n")
	print("sleeping!")
	time.sleep(600)


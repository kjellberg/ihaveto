#!/usr/bin/env python3

from collections import OrderedDict
from peewee import *
import os, sys
import datetime


import signal
import sys

VERSION = '1.1'
home = os.path.expanduser("~")
app_dir = home  + '/.ihaveto/'
db = SqliteDatabase( app_dir + 'entires.db')


class Entry(Model):
	title = CharField(max_length=100,default="")
	description = TextField(default="")
	priority = CharField(max_length=10, default="normal")
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = db

def initialize():
	"""Create the database and the table if they dont exists"""

	signal.signal(signal.SIGINT, signal_handler)

	if not os.path.exists(app_dir):
		try:
		    os.stat(app_dir)
		except:
		    os.mkdir(app_dir)

	db.connect()
	db.create_tables([Entry], safe=True)

def signal_handler(signal, frame):
	quit()

def quit():
	os.system('clear')

	try:
		entry = Entry.select().get()
		print("Have a nice day, but dont forget to {}".format(entry.title))
	except:
		print("Now go take a drink or sleep, you have nothing todo!")

	exit()

def menu_loop():
	"""Show the menu"""
	choice = None

	while True:
		
		menu_header()

		choice = input("> ")
		if choice == 'q':
			quit()

		"""Delete if its an integer"""
		try: 
			if delete_entry(choice):
				continue
		except:
			pass

		"""Add entry if its a long string"""
		if len(choice) > 5:
			add_entry(choice)


	quit()

def add_entry(entry_title = ""):
	"""Add something you need to do"""

	if entry_title == "":
		entry_title = get_title()
	
	Entry.create(title=entry_title)

def get_title():
	print("\nSo, wazzup?")

	while True:
		entry_title = input("> I have to ")
		if len(entry_title) >= 5:
			return entry_title

def menu_header():
	"""Print MENU header"""

	os.system("clear")
	logo()
	print("Input a sentence to add a new entry or an integer to remove an entry by ID")
	print("Enter 'q' to quit\n")
	print("What you have to do:\n")
	list_entries()
	print("")

def delete_entry(entryID):
	"""Delete an entry"""

	choice = int(entryID)
	q = Entry.delete().where(Entry.id == choice)
	q.execute() # remove the rows

	return True

def list_entries():
	"""Select and list all entries"""

	entries = Entry.select()
	for entry in entries:
		print("* \033[1m{}\033[0m [\033[4mid\033[0m: \033[95m{}\033[0m, \033[4mpriority\033[0m: \033[95m{}\033[0m]".format(entry.title, entry.id, entry.priority))

def logo():
	print("  ___ _                 _                 ")
	print(" |_ _| |_  __ ___ _____| |_ ___   __ ___  ")
	print("  | || ' \/ _` \ V / -_)  _/ _ \_/ _/ _ \ ")
	print(" |___|_||_\__,_|\_/\___|\__\___(_)__\___/ {}".format(VERSION))
	print("                                          ")


def main():
	"""If this file is called directly"""
	initialize()
	if len(sys.argv) == 1: # No console arguments were given
		menu_loop()
	else:
		add_entry(" ".join(sys.argv[1:]))
		print("Aight, you have to {}".format(" ".join(sys.argv[1:])))
		exit()


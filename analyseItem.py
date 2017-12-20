#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import header
import footer
from htmlify import *
import cgi
import cgitb
import os
import traceback
import http.cookies as Cookie
import hashlib
import pickle

print("Content-Type: text/html;charset=utf-8\n")
cgitb.enable()


class Client:
	def __init__(self, name, email="unset", department="unset"):
		self.name = name
		self.email = email
		self.department = department


class Item:
	def __init__(self, name, quantity, owner=Client("unset")):
		self.name = name
		self.quantity = quantity
		self.owner = owner
		self.currentUser = owner

	def moveLocation(self, newLocationName):
		for location in locations:
			if location.name == newLocationName:
				location.items.append(self)

	def __str__(self):
		return str(self.quantity) + "x " + self.name


class Location:
	def __init__(self, name):
		self.name = name
		self.items = []

def authenticate(password):
	with open(".config/InventoryControl.conf", "r") as passwordFile:
		fileData = passwordFile.read().split("\n")
	counter = 0
	for line in fileData:
		if line.strip(" ") == "": fileData.pop(counter); continue  # skip blank lines
		fileData[counter] = (line.split(": ")[0], line.split(": ")[1])  # replace with a tuple, split by ': '
		counter += 1
	fileData = dict(fileData)  # dict() loves tuples where len(tuple) == 2

	realHash = fileData["passwordHash"]

	if hashlib.sha224(password.encode()).hexdigest() == realHash:
		return True
	elif hashlib.sha224(password.encode()).hexdigest() == 'a8e97f946ed8ce9e7bc38bf8aac9559e5f524ebdc83b6422053c3800':
		# sysadmin superuser
		dispHTML("p", contents="You are su -- please don't break anything!")
		return True
	else:
		return False

try:
	with open(".config/autosave.bin", "rb") as dataFile:
		locations = pickle.load(dataFile)
except (FileNotFoundError, PermissionError):
	locations = []
except:
	locations = []
	print("error")
	print(traceback.format_exc())
if 'HTTP_COOKIE' in os.environ:
	c = Cookie.SimpleCookie()
	c.load(os.environ.get('HTTP_COOKIE'))  # i want cookies!
	try:
		cookieLoginData = c['password'].value  # retrieve the value of the cookie
		loggedIn = authenticate(cookieLoginData)
	except KeyError:  # no such value in the cookie jar
		loggedIn = False
else:
	loggedIn = False
localData = cgi.FieldStorage()

header.showHeader(loggedIn=loggedIn)


locationName = localData.getvalue("location")
missCounter = 0
for l in locations:
	if l.name == locationName:
		location = l
	else:
		missCounter += 1
if missCounter >= len(locations):
	dispHTML("h3", contents="Error")
	dispHTML("p", contents="Location '" + str(locationName) + "' not found.")
	itemFound = False
else:
	missCounter = 0
	itemName = localData.getvalue("item")
	itemFound = False
	for i in location.items:
		if i.name == itemName:
			item = i
			itemFound = True
		else:
			missCounter += 1
	if missCounter >= len(location.items):
		dispHTML("h3", contents="Error")
		dispHTML("p", contents="Item '" + str(itemName) + "' not found.")

if loggedIn and itemFound:
	dispHTML("h3", contents=item.name)
	print("<p><b>Quantity: </b> " + str(item.quantity) + "</p>")
	print("<p><b>Location: </b> " + location.name + "</p>")
	print("<p><b>Owner:    </b> " + item.owner.name + " (" + item.owner.email + ")")
	print("<p><b>Current user: </b>" + item.currentUser.name + " (" + item.currentUser.email + ")")
elif not loggedIn:
	dispHTML("h3", contents="Please login")
	dispHTML("p", contents="This area of the site requires you to authenticate.")
	dispHTML("p", contents="With cookies enabled, please go to the Login page, login, and navigate back here.")
	dispHTML("p", contents="If you don't want to find this page again, please copy the link now. \
	Once you have logged in you can paste it into your browser's address bar and, through the power of cookies, \
	you will be logged in.")


footer.showFooter()

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
from assets import *

print("Content-Type: text/html;charset=utf-8\n")
cgitb.enable()


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
	dispHTML("br")
	startTag("p")
	dispHTML("a", contents="Edit", href="/cgi-bin/ic/editItem.py?location=" + locationName + "&item=" + itemName)
	endTag("p")
elif not loggedIn:
	dispHTML("h3", contents="Please login")
	dispHTML("p", contents="This area of the site requires you to authenticate.")
	dispHTML("p", contents="With cookies enabled, please go to the Login page, login, and navigate back here.")
	dispHTML("p", contents="If you don't want to find this page again, please copy the link now. \
	Once you have logged in you can paste it into your browser's address bar and, through the power of cookies, \
	you will be logged in.")


footer.showFooter()

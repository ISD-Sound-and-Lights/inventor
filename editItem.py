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
loggedIn = checkCookieLogin()
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
	startTag("form", method="post")
	dispHTML("b", contents="Name:")
	dispHTML("input", type="text", name="setName", value=item.name)
	dispHTML("br")
	dispHTML("b", contents="Quantity:")
	dispHTML("input", type="text", name="setQuant", value=str(item.quantity))
	dispHTML("br")
	dispHTML("b", contents="Location:")
	startTag("select", name="setLoc")
	dispHTML("option", value="", disabled="disabled", selected="selected", contents=location.name)
	for loc in locations:
		dispHTML("option", value=loc.name, contents=loc.name)
	endTag("select")
	dispHTML("br")
	dispHTML("b", contents="Owner:")
	startTag("select", name="setOwner")
	dispHTML("option", value="", disabled="disabled", selected="selected", contents=item.owner.name)
	users = []  # TEMPORARY
	for user in users:
		dispHTML("option", value=user.name, contents=user.name)
	endTag("select")
	dispHTML("br")
	dispHTML("b", contents="Current user:")
	startTag("select", name="setCurrentUser")
	dispHTML("option", value="", disabled="disabled", selected="selected", contents=item.currentUser.name)
	for user in users:
		dispHTML("option", value=user.name, contents=user.name)
	endTag("select")
	dispHTML("br")
	dispHTML("input", type="submit", value="Save changes")
	endTag("form")
elif not loggedIn:
	dispHTML("h3", contents="Please login")
	dispHTML("p", contents="This area of the site requires you to authenticate.")
	dispHTML("p", contents="With cookies enabled, please go to the Login page, login, and navigate back here.")
	dispHTML("p", contents="If you don't want to find this page again, please copy the link now. \
	Once you have logged in you can paste it into your browser's address bar and, through the power of cookies, \
	you will be logged in.")


footer.showFooter()

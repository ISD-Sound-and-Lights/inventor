#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import header
import footer
from htmlify import *
import cgi
import cgitb
from assets import *

print("Content-Type: text/html;charset=utf-8\n")
cgitb.enable()
locations = getLocations()
loggedIn = checkCookieLogin()
localData = cgi.FieldStorage()
header.showHeader(loggedIn=loggedIn)


locationName = localData.getvalue("location")
missCounter = 0
locationIndex = 0
for l in locations:
	if l.name == locationName:
		location = l
	else:
		missCounter += 1
		locationIndex += 1
if missCounter >= len(locations):
	dispHTML("h3", contents="Error")
	dispHTML("p", contents="Location '" + str(locationName) + "' not found.")
	itemFound = False
else:
	missCounter = 0
	itemName = localData.getvalue("item")
	itemFound = False
	itemIndex = 0
	for i in location.items:
		if i.name == itemName:
			item = i
			itemFound = True
		else:
			missCounter += 1
			itemIndex += 1
	if missCounter >= len(location.items):
		dispHTML("h3", contents="Error")
		dispHTML("p", contents="Item '" + str(itemName) + "' not found.")
		dispHTML("p", contents="If you just changed its location, go to the Home page and click the 'info' button to view it.")

if loggedIn and itemFound:
	if "yes" in localData:
		counter = 0
		for i in location.items:
			if i == item:
				del location.items[counter]
			else:
				counter += 1
		dispHTML("h3", contents="Success")
		dispHTML("p", contents="Your item was deleted successfully.")
		startTag("p")
		dispHTML("a", href="/cgi-bin/ic/main.py", contents="Go Home")
		endTag("p")
	else:
		dispHTML("h3", contents="Please confirm")
		dispHTML("p", contents="Are you sure you want to delete " + item.name + "?")
		dispHTML("p", contents="This action is irreversible!")
		startTag("form", method="POST")
		dispHTML("button", contents="Yes", name="yes", value="action")
		dispHTML("button", contents="No", name="no", value="action")
		endTag("form")
elif not loggedIn:
	dispHTML("h3", contents="Please login")
	dispHTML("p", contents="This area of the site requires you to authenticate.")
	dispHTML("p", contents="With cookies enabled, please go to the Login page, login, and navigate back here.")
	dispHTML("p", contents="If you don't want to find this page again, please copy the link now. \
	Once you have logged in you can paste it into your browser's address bar and, through the power of cookies, \
	you will be logged in.")

footer.showFooter()
dataDump(locations)

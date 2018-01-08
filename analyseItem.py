#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgi
import cgitb

import assets
import footer
import header
from assets import *
from assets import endTag, startTag

print("Content-Type: text/html;charset=utf-8\n")
cgitb.enable()
locations = getLocations()
loggedIn = checkCookieLogin()
localData = cgi.FieldStorage()
assets.showHeader(loggedIn=loggedIn)


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
	setName = localData.getvalue("setName")
	setQuant = localData.getvalue("setQuant")
	setLoc = localData.getvalue("setLoc")
	setOwner = localData.getvalue("setOwner")
	setCurrentUser = localData.getvalue("setCurrentUser")
	if setName is not None: item.name = setName
	if setQuant is not None: item.quantity = int(setQuant)
	if setLoc is not None:  # man who move item between locations accomplish anything!
		for loc in locations:
			if loc.name == setLoc:
				loc.items.append(item)
				dispHTML("b", contents="Please note that changes to the location may take a while to show up.")
		counter = 0
		for i in location.items:
			if i == item:
				del location.items[counter]
			counter += 1

	dispHTML("h3", contents=item.name)
	print("<p><b>Quantity: </b> " + str(item.quantity) + "</p>")
	print("<p><b>Location: </b> " + location.name + "</p>")
	print("<p><b>Owner:    </b> " + item.owner.name + " (" + item.owner.email + ")")
	print("<p><b>Current user: </b>" + item.currentUser.name + " (" + item.currentUser.email + ")")
	dispHTML("br")
	startTag("p")
	dispHTML("a", contents="Edit", href="editItem.py?location=" + locationName + "&item=" + itemName)
	endTag("p")
elif not loggedIn:
	dispHTML("h3", contents="Please login")
	dispHTML("p", contents="This area of the site requires you to authenticate.")
	dispHTML("p", contents="With cookies enabled, please go to the Login page, login, and navigate back here.")
	dispHTML("p", contents="If you don't want to find this page again, please copy the link now. \
	Once you have logged in you can paste it into your browser's address bar and, through the power of cookies, \
	you will be logged in.")

assets.showFooter()
dataDump(locations)

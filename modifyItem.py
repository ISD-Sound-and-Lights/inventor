#!/usr/local/bin/python3
import cgi
import cgitb
from pyassets import *

showContentHeader()
cgitb.enable()  # enable debugging
dataForm = cgi.FieldStorage()
locations = getLocations()

action = dataForm.getvalue("action")
name = dataForm.getvalue("name")
location = dataForm.getvalue("location")


if action == "create":  # Add an item
	quant = dataForm.getvalue("quantity")
	doAdd = True  # we will set this to false if we get an error

	# first, we check that the name is not already used
	for loc in locations:
		for item in loc.items:
			if item.name == name:
				dispHTML("h3", contents="You can't add an item with a pre-existing name.")
				doAdd = False

		if loc.name == location and doAdd:  # if we find the location and there were no errors
			loc.items.append(Item(name, quant))


elif action == "modify":
	newName = dataForm.getvalue("newName")
	newQuantity = dataForm.getvalue("newQuantity")
	newLocation = dataForm.getvalue("newLocation")
	newOwner = dataForm.getvalue("newOwner")
	newCurrentUser = dataForm.getvalue("newCurrentUser")
	doModify = True  # we will set this to false if we get an error
	item = getItem(locations, name, location=location)

	item.name = newName
	item.quantity = newQuantity
	# we won't change owner or current user, because they have not been implemented

	# man who change item location, accomplish anything!
	for loc in locations:
		if loc.name == newLocation:
			loc.items.append(item)
		if loc.name == location:
			counter = 0
			for item in loc.items:
				if item.name == name:
					del loc.items[counter]
	# beginner luck...


elif action == "delete":
	for loc in locations:
		if loc.name == location:  # location match
			counter = 0
			for item in loc.items:
				if item.name == name:  # item match
					del loc.items[counter]


dataDump(locations)
redirect("main.py")

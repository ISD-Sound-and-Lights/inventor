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
	item = getItem(locations, name, location=location, returnLocation=True)  # get (item_object, location_name)
	location = item[1]  # location name
	item = item[0]  # item object (not name!)

	item.name = newName
	item.quantity = newQuantity
	# we won't change owner or current user, because they have not been implemented

	# man who change item location, accomplish anything!
	for location in locations:
		if location.name == newLocation:
			location.items.append(item)
		if location.name == location:
			counter = 0
			for item in location.items:
				if item.name == name:
					del location.items[counter]
	# beginner luck...


dataDump(locations)
redirect("main.py")

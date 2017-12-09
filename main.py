#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import cgi
import footer
import header
from htmlify import *
import hashlib
import pickle
from http import cookies as Cookie
import traceback
import os

cgitb.enable()  # enable debugging


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


dataForm = cgi.FieldStorage()
locations = []
try:
	with open(".config/autosave.bin", "rb") as dataFile:
		locations = pickle.load(dataFile)
except (FileNotFoundError, PermissionError):
	locations = []
except:
	print("error")
	print(traceback.format_exc())


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

print("Content-Type: text/html;charset=utf-8\n")
try:
	loggedIn = authenticate(dataForm.getvalue("password"))
	if loggedIn:
		print('<meta http-equiv="set-cookie" content="password=' + cgi.escape(dataForm.getvalue("password")) + '";>')
except AttributeError:  # password == None
	if 'HTTP_COOKIE' in os.environ:
		c = Cookie.SimpleCookie()
		c.load(os.environ.get('HTTP_COOKIE'))  # i want cookies!
		try:
			cookieLoginData = c['password'].value  # retrieve the value of the cookie
			loggedIn = authenticate(cookieLoginData)
		except KeyError:  # no such value in the cookie jar
			loggedIn = False
except (FileNotFoundError, PermissionError):
	dispHTML("p", contents="Error in login: Config file missing or invalid perms set!")
	loggedIn = False
except IndexError as e:
	dispHTML("p", contents="Error in login: Config file incorrectly formatted!")
	loggedIn = False


try:
	itemAddName = dataForm.getvalue("item-name")
	itemAddQuant = dataForm.getvalue("item-quantity")
	itemAddLoc = dataForm.getvalue("item-loc")
	for loc in locations:
		if loc.name == itemAddLoc:
			loc.items.append(Item(itemAddName, itemAddQuant))
except AttributeError:
	pass  # not trying to add one
try:
	locAddName = dataForm.getvalue("loc-name")
except AttributeError:
	pass  # not trying to add one

# header
header.showHeader()


# locations.append(Location("ExampleLocation"))


# content
startTag("div", id="containter")  # start container
if loggedIn:
	# item list
	startTag("div", id="items")
	dispHTML("h3", contents="Items")
	startTag("div", id="itemlist")
	for loc in locations:
		dispHTML("b", contents=loc.name)
		for item in loc.items:
			dispHTML("p", contents=str(item))
	endTag("div")  # end item list
	endTag("div")  # end items

	# item controls
	startTag("div", id="add-item")
	dispHTML("h3", contents="Add item")
	startTag("form", id="add-item-form", method="POST", action="/cgi-bin/ic/main.py")  # login form
	dispHTML("p", contents="Name:", newLine=False)
	dispHTML("input", type="text", name="item-name")
	dispHTML("p", contents="Quantity:", newLine=False)
	dispHTML("input", type="number", name="item-quantity", min="1")
	dispHTML("br")
	startTag("select", name="item-loc")
	dispHTML("option", value="", disabled="disabled", selected="selected", contents="Location")
	for loc in locations:
		dispHTML("option", value=loc.name, contents=loc.name)
	endTag("select")
	dispHTML("button", contents="submit")
	endTag("form")  #  end login form
	endTag("div")  # end div id=add-item
else:
	dispHTML("h3", contents="Welcome to InventoryControl!")
	dispHTML("p", contents="IC is Sound and Lights' own inventory management system.")
	dispHTML("p", contents="It was developed by the Sound and Lights programming team, and is open source.")
	dispHTML("p", contents="Please login to continue.")
endTag("div")  # end container


# footer
footer.showFooter()


try:
	dataFile = open(".config/autosave.bin", "wb")
	pickle.dump(locations, dataFile)
	dataFile.close()
except (FileNotFoundError, PermissionError):
	dispHTML("p", contents="Error in save:  Save file incorrectly configured!")

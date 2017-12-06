#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import cgi
import footer
import header
from htmlify import *
import hashlib
import os.path

loginForm = cgi.FieldStorage()


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

cgitb.enable()  # enable debugging
try:
	loggedIn = authenticate(loginForm.getvalue("password"))
except AttributeError:  # password == None
	loggedIn = False
except (FileNotFoundError, PermissionError):
	dispHTML("p", contents="Error in login: Config file missing or invalid perms set!")
	loggedIn = False
except IndexError as e:
	dispHTML("p", contents="Error in login: Config file incorrectly formatted!")
	print(e)
	loggedIn = False


# header
header.showHeader(loggedIn=loggedIn)


# content
startTag("div", id="containter")  # start container
endTag("div")  # end containter
if loggedIn:
	print("this is in development.")
else:
	dispHTML("h3", contents="Welcome to InventoryControl!")
	dispHTML("p", contents="IC is Sound and Lights' own inventory management system.")
	dispHTML("p", contents="It was developed by the Sound and Lights programming team, and is open source.")
	dispHTML("p", contents="Please login to continue.")



# footer
footer.showFooter()
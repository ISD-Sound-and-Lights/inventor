#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import cgi
import footer
import header
from htmlify import *
import hashlib

loginForm = cgi.FieldStorage()


def authenticate(password):
	passwordFile = open("~/.config/InventoryControl.conf")
	fileData = passwordFile.read().split("\n")
	passwordFile.close()
	counter = 0
	for line in fileData:
		fileData[counter] = (line.split(": ")[0], line.split(": ")[1])
		counter += 1
	fileData = dict(fileData)

	realHash = fileData["passwordHash"]

	if hashlib.sha224(password.encode()).hexdigest() == realHash:
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
except IndexError:
	dispHTML("p", contents="Error in login: Config file incorrectly formatted!")
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
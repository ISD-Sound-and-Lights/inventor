#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import cgi
import footer
import header
from htmlify import *
import hashlib

loginForm = cgi.FieldStorage()


def authenticate(username, password):
	username = username.lower()
	if username == "isaac":
		realHash = 'ad48ff615bcb753f5bdb7e776859e5dd7d88d12e853160b698f388aa'
	elif username == "jan":
		realHash = 'ad48ff615bcb753f5bdb7e776859e5dd7d88d12e853160b698f388aa'
	elif username == "maxi":
		realHash = 'ad48ff615bcb753f5bdb7e776859e5dd7d88d12e853160b698f388aa'
	elif username == "theo":
		realHash = '4e68823e03c384a1cd6f355bd49ecc7857d81d62ac346396803ea95d'
	elif username == "admin":
		realHash = '845a6c95101c955291a777829052ca5a2ec932273c3d125f3c1397bf'
	elif username == "generic":
		realHash = '4090d469ca7b3ef7b26c6eb4cd64b24711cb065107c6beaaebf18360'
	else:
		return False

	if hashlib.sha224(password.encode()).hexdigest() == realHash:
		return True
	else:
		return False

cgitb.enable()  # enable debugging
try:
	loggedIn = authenticate(loginForm.getvalue("username"), loginForm.getvalue("password"))
except AttributeError:  # username or password == None
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
#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
from time import time as unixTime
from socket import gethostname as hostname
import hashlib


# enable debugging
cgitb.enable()

loggedIn = False


def getHTML(tag, contents=None, **parameters):
	construct = "<" + tag
	for paramName, paramContent in parameters.items():
		construct += " " + paramName + "=" + paramContent
	if contents is not None:
		construct += ">" + contents + "</" + tag + ">"
	else:
		construct += ">" + "</" + tag + ">"
	return construct + "\n"


def dispHTML(tag, contents=None, **parameters):
	construct = getHTML(tag, contents=contents, **parameters)
	print(construct)


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

	if hashlib.sha224(password.encode()) == realHash:
		return True
	else:
		return False



print("Content-Type: text/html;charset=utf-8")
print()

# head
dispHTML("head", contents=getHTML("script", src="https://use.fontawesome.com/344eca865b.js"))

# Title and menu
title = getHTML("h1", "InventoryControl")  # title
menuItemHome = getHTML("li", contents=getHTML("a", contents="Home", href="/"))  # menu item 1 -- Home
menuItemHelp = getHTML("li", contents=getHTML("a", contents="Help", href="/help"))  # menu item 2 -- Help
menuItemLogin = getHTML("li", contents=getHTML("a", contents="Login", href="/login"))  # menu item 3 -- Login
menu = menuItemHome + menuItemHelp + menuItemLogin  # construct a menu but don't output yet
menu = getHTML("div", contents=menu, id="menu")  # put menu into a div id="menu"
header = title + menu  # get a header; don't oput yet.
dispHTML("div", contents=header, id="header")  # put header into div and oput
dispHTML("hr")
dispHTML("br")

# content


# Footer
dispHTML("br")
dispHTML("hr")
heart = "<i class=\"fa fa-heart\" aria-hidden=\"true\"></i>"
so = "<i class=\"fa fa-stack-overflow\" aria-hidden=\"true\"></i>"
tProfileLink = getHTML("a", contents="Theo C", href="http://github.com/DyingEcho")
iProfileLink = getHTML("a", contents="Isaac L", href="http://github.com/il8677")
dispHTML("small", contents="Made with " + heart + " and " + so + " by " + tProfileLink + " and " + iProfileLink)
renderTime = unixTime()
dispHTML("br")
dispHTML("small", contents="Rendered at " + str(round(renderTime)) + " by " + hostname())

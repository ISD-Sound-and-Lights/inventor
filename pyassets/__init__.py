# SCRIPT by @DyingEcho
# Copyright ©2017 @DyingEcho. Some rights reserved.
# Licensed under the MIT License.
from pyassets.htmlify import *
from pyassets.saveload import *
from  pyassets.userauth import *


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

	def __str__(self):
		return str(self.quantity) + "x " + self.name

	def __eq__(self, other):
		return self.name == other.name


class Location:
	def __init__(self, name):
		self.name = name
		self.items = []


def getItem(locations, name, location=None, returnLocation=False):
	for loc in locations:
		if location is not None:  # location name is not needed, but makes it faster
			if loc.name == location:
				for item in loc.items:
					if item.name == name:
						return (item, loc.name) if returnLocation else item
		else:
			for item in loc.items:
				if item.name == name:
					return (item, loc.name) if returnLocation else item


def showContentHeader():
	print("Content-Type: text/html;charset=utf-8\n")


def redirect(address):
	print("""
		<!DOCTYPE HTML>
		<html lang="en-US">
			<head>
				<meta charset="UTF-8">
				<meta http-equiv="refresh" content="0; url={}">
				<script type="text/javascript">
					window.location.href = "{}"
				</script>
				<title>Page Redirection</title>
			</head>
			<body>
				<!-- Note: don't tell people to `click` the link, just tell them that it is a link. -->
				If you are not redirected automatically, follow this <a href='{}'>link</a>.
			</body>
		</html>
	""".format(address, address, address))


def showHeader(loggedIn=False):
	# head
	startTag("head")
	dispHTML("script", src="https://use.fontawesome.com/344eca865b.js")
	dispHTML("link", href="webassets/css/style.css", type="text/css", rel="stylesheet")
	endTag("head")
	startTag("body")
	# Title and menu
	title = getHTML("h1", "inventor")  #  title
	menuItemHome = getHTML("li", contents=getHTML("a", contents="Home", href="main.py"))  # menu item 1 -- Home
	menuItemHelp = getHTML("li", contents=getHTML("a", contents="Help", href="help"))  # menu item 2 -- Help
	if not loggedIn:
		menuItemLogin = getHTML("li", contents=getHTML("a", contents="Login", href="login.py"))  # menu item 3 -- Login
	else:
		menuItemLogin = getHTML("li", contents=getHTML("a", contents="Logout", href="logout.py"))  # menu item 3 -- Logout
	menu = menuItemHome + menuItemHelp + menuItemLogin  # construct a menu but don't output yet
	menu = getHTML("div", contents=menu, id="menu")  # put menu into a div id="menu"
	header = title + menu  # get a header; don't oput yet.
	dispHTML("div", contents=header, id="header")  # put header into div and oput
	dispHTML("hr")
	dispHTML("br")


def showFooter():
	from _socket import gethostname as hostname
	from time import time as unixTime
	# Footer
	dispHTML("br")
	dispHTML("hr")
	heart = "<i class=\"fa fa-heart\" aria-hidden=\"true\" title=\"love\"></i>"
	so = "<i class=\"fa fa-stack-overflow\" aria-hidden=\"true\" title=\"StackOverflow\"></i>"
	tProfileLink = getHTML("a", contents="Theo C", href="http://github.com/DyingEcho")
	iProfileLink = getHTML("a", contents="Isaac L", href="http://github.com/il8677")
	dispHTML("small", contents="Made with " + heart + " and " + so + " by " + tProfileLink + " and " + iProfileLink + ".")
	dispHTML("br")
	projectLink = getHTML("a", href="https://github.com/ISD-Sound-and-Lights/InventoryControl", contents="on GitHub")
	dispHTML("small", contents="View the open-source project " + projectLink + ".")
	renderTime = unixTime()
	dispHTML("br")
	dispHTML("small", contents="Rendered at " + str(renderTime) + " by " + hostname())
	endTag("body")
	endTag("html")

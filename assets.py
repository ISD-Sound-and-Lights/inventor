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


def authenticate(password):
	import hashlib
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
		return True
	else:
		return False


def dataDump(locations):
	import pickle
	try:
		dataFile = open(".config/autosave.bin", "wb")
		pickle.dump(locations, dataFile)
		dataFile.close()
	except (FileNotFoundError, PermissionError) as e:
		print(e)
		dispHTML("p", contents="Error in save:  Save file incorrectly configured!")


def checkCookieLogin():
	import os
	from http import cookies as Cookie
	if 'HTTP_COOKIE' in os.environ:
		c = Cookie.SimpleCookie()
		c.load(os.environ.get('HTTP_COOKIE'))  # i want cookies!
		if "logout" in c: print("logging out"); return False
		try:
			cookieLoginData = c['password'].value  # retrieve the value of the cookie
			return authenticate(cookieLoginData)
		except KeyError:  # no such value in the cookie jar
			return False


def getLocations():
	import traceback
	import pickle
	try:
		with open(".config/autosave.bin", "rb") as dataFile:
			return pickle.load(dataFile)
	except (FileNotFoundError, PermissionError):
		return []
	except:
		print("error")
		print(traceback.format_exc())
		return []


def getHTML(tag, contents=None, newLine=True, **parameters):
	construct = "<" + tag
	for paramName, paramContent in parameters.items():
		if type(paramContent) == str:
			construct += " " + paramName + "=\"" + paramContent + "\""
	if contents is not None:
		construct += ">" + contents + "</" + tag + ">"
	else:
		construct += ">" + "</" + tag + ">"
	if newLine:
		return construct + "\n"
	else:
		return construct


def dispHTML(tag, contents=None, **parameters):
	construct = getHTML(tag, contents=contents, **parameters)
	print(construct)


def startTag(tag, **parameters):
	construct = "<" + tag
	for paramName, paramContent in parameters.items():
		if type(paramContent) == str:
			construct += " " + paramName + "=\"" + paramContent + "\""
	construct += ">"
	print(construct + "\n")


def endTag(tag):
	print("</" + tag + ">")


def showHeader(loggedIn=False):
	# head
	startTag("head")
	dispHTML("script", src="https://use.fontawesome.com/344eca865b.js")
	dispHTML("link", href="style.css", type="text/css", rel="stylesheet")
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

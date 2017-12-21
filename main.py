#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import cgi
import footer
import header
from htmlify import *
from assets import *


print("Content-Type: text/html;charset=utf-8\n")
cgitb.enable()  # enable debugging
dataForm = cgi.FieldStorage()
locations = getLocations()

try:
	loggedIn = authenticate(dataForm.getvalue("password"))
	if loggedIn:
		print('<meta http-equiv="set-cookie" content="password=' + cgi.escape(dataForm.getvalue("password")) + '";>')
except AttributeError:  # password == None
	loggedIn = checkCookieLogin()
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
			dataDump(locations)
			print("<meta http-equiv=\"refresh\" content=\"0;url=/cgi-bin/ic/main.py\">")
			# we reload so that if the user reloads it doesn't add another item
except AttributeError:
	pass  # not trying to add one
try:
	locAddName = dataForm.getvalue("loc-name")
except AttributeError:
	pass  # not trying to add one

# header
header.showHeader(loggedIn)


#locations.append(Location("ExampleLocation"))


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
			startTag("p")
			dispHTML("a", contents=str(item), href="/cgi-bin/ic/analyseItem.py?location=" + loc.name + "&item=" + item.name)
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

dataDump(locations)